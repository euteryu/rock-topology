"""Single-phase permeability: voxel solver (lattice-Boltzmann) and pore-network model.

Permeability claims rest on the voxel solver (`lbm_permeability`). The pore network
(`pnm_permeability`) is a second estimate.

Voxel solver
------------
D3Q19 two-relaxation-time (TRT) lattice-Boltzmann in its linear (Stokes) form:
the equilibrium has no u^2 term, so inertia is removed exactly and the computed
permeability does not depend on the forcing magnitude. Walls use halfway bounce-back.
With the "magic" parameter Lambda = 3/16 the wall sits halfway between a pore and a grain
voxel and the permeability does not depend on the chosen viscosity (standard TRT result;
the primary reference is still to be opened and added to docs/refs.bib before citing).
Both properties are verified by unit tests here (tests/test_flow.py).

Only pore voxels are stored (sparse layout), so memory and time scale with porosity.
Pore clusters that do not span the sample carry no net flow and are removed first.
Populations are stored as deviations from the rest state, so float32 is accurate.

Boundary conditions (choice logged in docs/lab-notebook.md, 2026-11-12):
 - flow driven by a uniform body force g along the flow axis in a periodic domain,
   equivalent to a uniform mean pressure gradient;
 - inlet/outlet, mode "buffer" (default): `n_buffer` layers of open fluid are added at each
   end, acting as reservoirs, so the periodic wrap does not join unmatched faces.
   Mode "mirror": the sample is mirrored along the flow axis (continuous but twice as long,
   so about 4x slower to converge). Mode "periodic": no change (only for periodic test
   geometries);
 - the four side faces are closed by one layer of grain (no-flow sides), unless
   side_walls=False.
Permeability from Darcy's law over the sample: k = nu * q * L_s / (g * L_tot), with q the
superficial (Darcy) velocity, L_s the sample length and L_tot the periodic length.

Convergence: the slowest mode (pressure equilibration along the sample) decays
geometrically. We stop when k changes by less than `tol` per check interval, or when an
Aitken extrapolation of the geometric tail is stable to `tol_extrap` and the remaining
tail is below `max_tail`; the extrapolated value is then reported with the tail size as
part of the numerical error.
"""
from __future__ import annotations

import time

import numpy as np
from scipy import ndimage as ndi

DARCY = 9.869233e-13  # m^2
MILLIDARCY = DARCY * 1e-3

# D3Q19 lattice, ordered: rest, 9 "positive" directions, their 9 opposites in same order.
_EP = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 0], [1, -1, 0],
                [1, 0, 1], [1, 0, -1], [0, 1, 1], [0, 1, -1]], dtype=np.int64)
_E = np.concatenate([np.zeros((1, 3), np.int64), _EP, -_EP])
_W = np.array([1 / 3] + [1 / 18] * 3 + [1 / 36] * 6 + [1 / 18] * 3 + [1 / 36] * 6)
_OPP = np.array([0] + list(range(10, 19)) + list(range(1, 10)))
assert (_E[_OPP] == -_E).all()

S6 = ndi.generate_binary_structure(3, 1)


def spanning_pores(mask, axis):
    """Pore voxels belonging to 6-connected clusters touching both faces normal to axis."""
    lab, n = ndi.label(mask, structure=S6)
    if n == 0:
        return np.zeros_like(mask, bool)
    a = np.unique(np.take(lab, 0, axis=axis))
    b = np.unique(np.take(lab, -1, axis=axis))
    keep = np.intersect1d(a, b)
    keep = keep[keep > 0]
    return np.isin(lab, keep)


def _prepare_domain(mask, axis, mode, n_buffer, side_walls):
    """Returns (domain with flow along axis 0, sample length, periodic length)."""
    m = np.moveaxis(np.asarray(mask, bool), axis, 0)
    L = m.shape[0]
    if mode == "mirror":
        m = np.concatenate([m, m[::-1]], axis=0)
        Ls = 2 * L
    elif mode == "buffer":
        m = np.pad(m, ((n_buffer, n_buffer), (0, 0), (0, 0)), constant_values=True)
        Ls = L
    elif mode == "periodic":
        Ls = L
    else:
        raise ValueError(mode)
    Ltot = m.shape[0]
    if side_walls:
        m = np.pad(m, ((0, 0), (0, 1), (0, 1)), constant_values=False)
    return m, Ls, Ltot


def _stream_index(dom):
    """For every (pore node, direction q) the flat index into f_post that streams into it.

    Node n receives direction q from its neighbour at x - e_q (periodic wrap). If that
    neighbour is grain, the population bounces back: it comes from node n itself,
    direction opp(q), post-collision (halfway bounce-back).
    """
    shape = np.array(dom.shape)
    nodes = np.flatnonzero(dom)
    lookup = -np.ones(dom.size, np.int64)
    lookup[nodes] = np.arange(len(nodes))
    zyx = np.stack(np.unravel_index(nodes, dom.shape), 1)
    Q = len(_E)
    idx = np.empty((len(nodes), Q), np.int64)
    self_i = np.arange(len(nodes))
    for q in range(Q):
        src = (zyx - _E[q]) % shape
        s = lookup[np.ravel_multi_index(src.T, dom.shape)]
        idx[:, q] = np.where(s >= 0, s * Q + q, self_i * Q + _OPP[q])
    return nodes, idx.reshape(-1)


def _aitken(hist):
    """Extrapolate a geometrically converging sequence from its last three values."""
    if len(hist) < 3:
        return None, None
    k1, k2, k3 = hist[-3], hist[-2], hist[-1]
    d1, d2 = k2 - k1, k3 - k2
    if d1 == 0:
        return k3, 0.0
    r = d2 / d1
    if not 0 < r < 0.999:
        return None, r
    return k3 + d2 * r / (1 - r), r


def lbm_permeability(mask, axis=0, voxel_size=None, nu=0.1, magic=3 / 16, g=1e-4,
                     tol=1e-6, tol_extrap=1e-4, max_tail=0.05, check_every=100,
                     max_steps=200_000, max_seconds=None, mode="buffer", n_buffer=3,
                     side_walls=True, device="cpu", dtype="float32", verbose=False,
                     return_field=False, extrapolate=True):
    """Permeability of a binary mask (True = pore) along `axis` by TRT lattice-Boltzmann.

    Returns a dict with k_vox2 (lattice units, voxel^2; extrapolated if that is how it
    converged), k_raw_vox2 (last iterate), tail (relative size of the extrapolated tail),
    k_m2 / k_mD if voxel_size (metres) is given, steps, converged, how ('delta', 'aitken',
    'max_steps' or 'max_seconds'), seconds, n_fluid, history.
    """
    import torch

    t0 = time.time()
    span = spanning_pores(mask, axis)
    out = dict(axis=axis, n_fluid=int(span.sum()), nu=nu, magic=magic, mode=mode)
    if span.sum() == 0:
        out.update(k_vox2=0.0, k_raw_vox2=0.0, tail=0.0, steps=0, converged=True, how="no_path",
                   seconds=time.time() - t0, percolates=False, history=[])
        if voxel_size:
            out.update(k_m2=0.0, k_mD=0.0)
        return out
    shape = np.moveaxis(np.asarray(mask), axis, 0).shape
    A = shape[1] * shape[2]
    dom, Ls, Ltot = _prepare_domain(span, axis, mode, n_buffer, side_walls)
    nodes, sidx = _stream_index(dom)
    N = len(nodes)

    tdt = getattr(torch, dtype)
    dev = torch.device(device)
    EP = torch.tensor(_EP, dtype=tdt, device=dev)            # 9 x 3
    WP = torch.tensor(_W[1:10], dtype=tdt, device=dev)       # 9
    w0 = float(_W[0])
    sidx_t = torch.tensor(sidx, device=dev)
    gvec = torch.tensor([g, 0.0, 0.0], dtype=tdt, device=dev)

    w_plus = 1.0 / (3.0 * nu + 0.5)
    w_minus = 1.0 / (magic / (1.0 / w_plus - 0.5) + 0.5)
    Fm = (1.0 - 0.5 * w_minus) * 3.0 * WP * (EP @ gvec)       # antisymmetric forcing

    f = torch.zeros((N, 19), dtype=tdt, device=dev)
    hist, k_ext_prev = [], None
    steps, converged, how, k_ext, r = 0, False, "max_steps", None, None
    with torch.no_grad():
        while steps < max_steps:
            for _ in range(check_every):
                f0, a, b = f[:, :1], f[:, 1:10], f[:, 10:]
                rho = f.sum(1, keepdim=True)
                j = (a - b) @ EP + 0.5 * gvec
                fp = 0.5 * (a + b)
                fm = 0.5 * (a - b)
                fp = fp - w_plus * (fp - WP * rho)
                fm = fm - w_minus * (fm - 3.0 * WP * (j @ EP.T)) + Fm
                fpost = torch.cat([f0 - w_plus * (f0 - w0 * rho), fp + fm, fp - fm], 1)
                f = torch.take(fpost, sidx_t).view(N, 19)
            steps += check_every
            jz = float(((f[:, 1:10] - f[:, 10:]) @ EP[:, 0]).double().sum()) + 0.5 * g * N
            q = jz / (A * Ltot)
            k = nu * q * Ls / (g * Ltot)
            hist.append(k)
            if verbose:
                print(f"step {steps:7d}  k = {k:.6e} vox^2", flush=True)
            if len(hist) >= 2 and abs(hist[-1] - hist[-2]) <= tol * abs(k):
                converged, how, k_ext = True, "delta", k
                break
            if extrapolate:
                k_ext, r = _aitken(hist)
                if (k_ext is not None and k_ext_prev is not None and k_ext > 0
                        and abs(k_ext - k_ext_prev) <= tol_extrap * k_ext
                        and abs(k - k_ext) <= max_tail * k_ext):
                    converged, how = True, "aitken"
                    break
                k_ext_prev = k_ext
            if max_seconds and time.time() - t0 > max_seconds:
                how = "max_seconds"
                break
    k_final = k_ext if (converged and k_ext is not None) else k
    out.update(k_vox2=k_final, k_raw_vox2=k, tail=abs(k - k_final) / k_final if k_final else 0.0,
               ratio=r, steps=steps, converged=converged, how=how, seconds=time.time() - t0,
               percolates=True, history=hist, n_nodes=N)
    if voxel_size:
        out["k_m2"] = k_final * voxel_size ** 2
        out["k_mD"] = out["k_m2"] / MILLIDARCY
    if return_field:
        u = np.zeros(dom.shape + (3,), np.float32)
        jj = ((f[:, 1:10] - f[:, 10:]) @ EP + 0.5 * gvec).cpu().numpy()
        u.reshape(-1, 3)[nodes] = jj
        out["velocity"] = u
    return out


def refine(mask, factor=2):
    """Nearest-neighbour upsampling of a mask (each voxel -> factor^3 voxels). Used for
    grid-refinement studies: the geometry is unchanged, only the lattice is finer."""
    m = np.asarray(mask, bool)
    for a in range(3):
        m = np.repeat(m, factor, axis=a)
    return m


def grid_refinement(mask, axis=0, voxel_size=1.0, factors=(1, 2), **kw):
    """Permeability (physical units) of the same geometry on successively finer lattices.

    Returns a list of dicts and the relative change between the two finest levels, which
    is our estimate of the solver's discretisation error for this sub-volume.
    """
    rows = []
    for f in factors:
        r = lbm_permeability(refine(mask, f), axis=axis, voxel_size=voxel_size / f, **kw)
        r.pop("history", None)
        rows.append(dict(factor=f, k_m2=r["k_m2"], steps=r["steps"], seconds=r["seconds"],
                         converged=r["converged"]))
    rel = abs(rows[-1]["k_m2"] - rows[-2]["k_m2"]) / rows[-1]["k_m2"] if len(rows) > 1 and rows[-1]["k_m2"] else np.nan
    return rows, rel


# ---------------------------------------------------------------- pore network
def pnm_permeability(net, shape, axis=0, voxel_size=1.0, mu=1e-3):
    """Permeability from an extracted network (rocktopo.network.extract) with OpenPNM.

    Conduits are spheres and cylinders sized by the inscribed diameters from SNOW2.
    Inlet / outlet pores are those whose region touches the two faces normal to `axis`.
    Only the cluster(s) connecting inlet to outlet are kept. Returns k in m^2 and mD.
    """
    import openpnm as op
    from scipy.sparse import coo_matrix
    from scipy.sparse.csgraph import connected_components

    pn = op.network.Network()
    pn.update({k: v for k, v in net.items() if k.startswith(("pore.", "throat."))})
    pn["pore.coords"] = np.asarray(net["pore.coords"])
    pn["throat.conns"] = np.asarray(net["throat.conns"])
    inlet = np.asarray(net[f"pore.inlet{axis}"])
    outlet = np.asarray(net[f"pore.outlet{axis}"])
    Np = pn.Np
    L = shape[axis] * voxel_size
    A = np.prod([s for i, s in enumerate(shape) if i != axis]) * voxel_size ** 2
    res = dict(axis=axis, k_m2=0.0, k_mD=0.0, n_pores=Np, n_throats=pn.Nt)
    if not inlet.any() or not outlet.any() or pn.Nt == 0:
        return res
    c = pn["throat.conns"]
    g = coo_matrix((np.ones(len(c)), (c[:, 0], c[:, 1])), shape=(Np, Np))
    _, lab = connected_components(g, directed=False)
    good = np.intersect1d(lab[inlet], lab[outlet])
    keep = np.isin(lab, good)
    if not keep.any():
        return res
    op.topotools.trim(network=pn, pores=np.where(~keep)[0])
    inlet, outlet = inlet[keep], outlet[keep]
    pn["pore.diameter"] = pn["pore.inscribed_diameter"]
    # SNOW2 can report a throat wider than one of its pores; the sphere-and-cylinder
    # conduit needs throat < pore, so clip to 0.99 x the smaller pore (count reported).
    dmin = pn["pore.diameter"][pn["throat.conns"]].min(1)
    td = np.asarray(pn["throat.inscribed_diameter"], float)
    clipped = td >= dmin
    pn["throat.diameter"] = np.where(clipped, 0.99 * dmin, td)
    res["n_throats_clipped"] = int(clipped.sum())
    pn.add_model(propname="throat.hydraulic_size_factors",
                 model=op.models.geometry.hydraulic_size_factors.spheres_and_cylinders,
                 pore_diameter="pore.diameter", throat_diameter="throat.diameter")
    pn.regenerate_models()
    ph = op.phase.Phase(network=pn)
    ph["pore.viscosity"] = mu
    ph.add_model(propname="throat.hydraulic_conductance",
                 model=op.models.physics.hydraulic_conductance.generic_hydraulic)
    ph.regenerate_models()
    sf = op.algorithms.StokesFlow(network=pn, phase=ph)
    dP = 1.0
    sf.set_value_BC(pores=np.where(inlet)[0], values=dP)
    sf.set_value_BC(pores=np.where(outlet)[0], values=0.0)
    # SciPy's direct solver, not OpenPNM's default PyPardiso: PyPardiso loads Intel's
    # OpenMP runtime a second time next to torch's and aborts the process (seen 2026-11-12).
    sf.run(solver=op.solvers.ScipySpsolve())
    Q = abs(float(sf.rate(pores=np.where(inlet)[0])[0]))
    k = Q * mu * L / (A * dP)
    res.update(k_m2=k, k_mD=k / MILLIDARCY, Q=Q)
    return res
