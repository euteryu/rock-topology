"""Segmentation metrics, primary tier (see docs/prereg.md).

Topology convention: the pore phase uses 6-connectivity (face neighbours), because fluid
can only pass between voxels that share a face. The grain phase then uses the dual
26-connectivity. Euler number, Betti numbers and connected components all follow this.

All functions take bool masks with True = pore.
"""
from __future__ import annotations

import numpy as np
from scipy import ndimage as ndi

S6 = ndi.generate_binary_structure(3, 1)
S26 = ndi.generate_binary_structure(3, 3)


# ---------------------------------------------------------------- overlap metrics
def dice(pred, ref):
    pred, ref = np.asarray(pred, bool), np.asarray(ref, bool)
    s = pred.sum() + ref.sum()
    return 1.0 if s == 0 else 2.0 * np.logical_and(pred, ref).sum() / s


def iou(pred, ref):
    pred, ref = np.asarray(pred, bool), np.asarray(ref, bool)
    u = np.logical_or(pred, ref).sum()
    return 1.0 if u == 0 else np.logical_and(pred, ref).sum() / u


def porosity(mask):
    return float(np.asarray(mask, bool).mean())


def porosity_error(pred, ref):
    """Signed porosity error, pred minus ref (absolute porosity units)."""
    return porosity(pred) - porosity(ref)


# ---------------------------------------------------------------- topology
def euler_number(mask):
    """Euler characteristic of the 6-connected pore phase.

    Built as a cubical complex on voxel centres: V voxels, E face-adjacent pairs, F 2x2
    squares, C 2x2x2 cubes; chi = V - E + F - C. Outside the box counts as grain.
    """
    m = np.asarray(mask, bool)
    V = int(m.sum())
    E = sum(int(np.logical_and(np.take(m, range(0, s - 1), a), np.take(m, range(1, s), a)).sum())
            for a, s in enumerate(m.shape))

    def sq(a, b):
        x = m
        x = np.logical_and(np.take(x, range(0, x.shape[a] - 1), a), np.take(x, range(1, x.shape[a]), a))
        x = np.logical_and(np.take(x, range(0, x.shape[b] - 1), b), np.take(x, range(1, x.shape[b]), b))
        return int(x.sum())

    F = sq(0, 1) + sq(0, 2) + sq(1, 2)
    c = m[:-1, :-1, :-1] & m[1:, :-1, :-1] & m[:-1, 1:, :-1] & m[:-1, :-1, 1:] \
        & m[1:, 1:, :-1] & m[1:, :-1, 1:] & m[:-1, 1:, 1:] & m[1:, 1:, 1:]
    C = int(c.sum())
    return V - E + F - C


def betti_numbers(mask):
    """(b0, b1, b2) of the pore phase.

    b0 = number of 6-connected pore clusters.
    b2 = number of grain clusters (26-connected) fully enclosed by pore, i.e. cavities.
         The box is padded with grain, so grains touching the box face are not cavities.
    b1 = number of independent loops (handles), from b1 = b0 + b2 - chi.
    """
    m = np.asarray(mask, bool)
    _, b0 = ndi.label(m, structure=S6)
    g = np.pad(~m, 1, constant_values=True)
    _, ng = ndi.label(g, structure=S26)
    b2 = ng - 1
    chi = euler_number(m)
    b1 = b0 + b2 - chi
    return int(b0), int(b1), int(b2)


def topology_summary(mask, voxel_size=None):
    """Euler number and Betti numbers, raw and as densities per unit volume.

    voxel_size in metres gives densities per mm^3 (rock convention), so sub-volumes of
    different size and resolution can be compared. voxel_size=None gives per voxel^3.
    """
    b0, b1, b2 = betti_numbers(mask)
    chi = b0 - b1 + b2
    vol_mm3 = float(mask.size) if voxel_size is None else mask.size * (voxel_size * 1e3) ** 3
    return dict(chi=chi, b0=b0, b1=b1, b2=b2, volume=vol_mm3,
                chi_density=chi / vol_mm3, b0_density=b0 / vol_mm3, b1_density=b1 / vol_mm3)


def topology_errors(pred, ref, voxel_size=None, ref_summary=None):
    """Euler and Betti errors of pred relative to ref.

    Reported as signed differences in density (per unit volume) and as relative errors
    |d| / max(|ref|, 1).
    """
    tr = ref_summary or topology_summary(ref, voxel_size)
    tp = topology_summary(pred, voxel_size)
    out = {}
    for k in ("chi", "b0", "b1"):
        d = tp[k] - tr[k]
        out[f"{k}_diff"] = d
        out[f"{k}_density_diff"] = d / tr["volume"]
        out[f"{k}_rel_err"] = abs(d) / max(abs(tr[k]), 1)
    out.update({f"pred_{k}": tp[k] for k in ("chi", "b0", "b1", "b2")})
    out.update({f"ref_{k}": tr[k] for k in ("chi", "b0", "b1", "b2")})
    return out


# ---------------------------------------------------------------- clDice
def skeleton(mask):
    from skimage.morphology import skeletonize

    return skeletonize(np.asarray(mask, bool)).astype(bool)


def cldice(pred, ref, skel_pred=None, skel_ref=None):
    """Hard clDice (Shit et al. 2021): harmonic mean of topology precision and sensitivity.

    Tprec = |S(pred) & ref| / |S(pred)|,  Tsens = |S(ref) & pred| / |S(ref)|.
    """
    pred, ref = np.asarray(pred, bool), np.asarray(ref, bool)
    sp = skeleton(pred) if skel_pred is None else skel_pred
    sr = skeleton(ref) if skel_ref is None else skel_ref
    if sp.sum() == 0 or sr.sum() == 0:
        return dict(cldice=float(sp.sum() == sr.sum()), tprec=np.nan, tsens=np.nan)
    tprec = np.logical_and(sp, ref).sum() / sp.sum()
    tsens = np.logical_and(sr, pred).sum() / sr.sum()
    cl = 0.0 if tprec + tsens == 0 else 2 * tprec * tsens / (tprec + tsens)
    return dict(cldice=float(cl), tprec=float(tprec), tsens=float(tsens))


# ---------------------------------------------------------------- throat matching
def match_throats(ref_xyz, ref_r, pred_xyz, pred_r, min_tol=2.0):
    """One-to-one matching of throats by position.

    A ref throat i and a pred throat j may be paired only if their distance is at most
    tol_i = max(ref_r[i], min_tol) (units of the coordinates, normally voxels). Within
    that constraint the total distance is minimised (Hungarian algorithm, solved per
    connected group of candidate pairs so it scales to thousands of throats).

    Returns dict with matched pairs, missed (ref unmatched), false (pred unmatched),
    and radius errors on matched pairs.
    """
    from scipy.optimize import linear_sum_assignment
    from scipy.sparse import coo_matrix
    from scipy.sparse.csgraph import connected_components
    from scipy.spatial import cKDTree

    ref_xyz, pred_xyz = np.atleast_2d(ref_xyz).astype(float), np.atleast_2d(pred_xyz).astype(float)
    ref_r, pred_r = np.asarray(ref_r, float), np.asarray(pred_r, float)
    nr, npd = len(ref_r), len(pred_r)
    pairs = []
    if nr and npd:
        tol = np.maximum(ref_r, min_tol)
        tree = cKDTree(pred_xyz)
        rows, cols, dists = [], [], []
        for i, cand in enumerate(tree.query_ball_point(ref_xyz, tol)):
            for j in cand:
                rows.append(i)
                cols.append(j)
                dists.append(np.linalg.norm(ref_xyz[i] - pred_xyz[j]))
        if rows:
            rows, cols, dists = map(np.asarray, (rows, cols, dists))
            g = coo_matrix((np.ones(len(rows)), (rows, cols + nr)), shape=(nr + npd, nr + npd))
            _, lab = connected_components(g, directed=False)
            comp = lab[rows]
            big = 1e9
            for c in np.unique(comp):
                sel = comp == c
                ri, ci = np.unique(rows[sel]), np.unique(cols[sel])
                cost = np.full((len(ri), len(ci)), big)
                cost[np.searchsorted(ri, rows[sel]), np.searchsorted(ci, cols[sel])] = dists[sel]
                a, b = linear_sum_assignment(cost)
                for x, y in zip(a, b):
                    if cost[x, y] < big:
                        pairs.append((ri[x], ci[y]))
    pairs = np.array(pairs, int).reshape(-1, 2)
    tp = len(pairs)
    out = dict(n_ref=nr, n_pred=npd, n_matched=tp, n_missed=nr - tp, n_false=npd - tp,
               miss_rate=(nr - tp) / nr if nr else 0.0,
               false_rate=(npd - tp) / npd if npd else 0.0,
               throat_f1=2 * tp / (nr + npd) if (nr + npd) else 1.0, pairs=pairs)
    if tp:
        rr, rp = ref_r[pairs[:, 0]], pred_r[pairs[:, 1]]
        rel = (rp - rr) / rr
        out.update(radius_rel_err=float(np.mean(np.abs(rel))), radius_rel_bias=float(np.mean(rel)))
    else:
        out.update(radius_rel_err=np.nan, radius_rel_bias=np.nan)
    return out


def throat_errors(net_pred, net_ref, min_tol=2.0):
    """Throat-level error between two extracted networks (see rocktopo.network).

    Positions are throat.global_peak (the voxel of largest inscribed radius on the
    throat surface) and radii are throat.inscribed_diameter / 2, both in voxels.
    """
    def get(n):
        vs = float(n.get("param.voxel_size", 1.0))
        return np.asarray(n["throat.global_peak"]) / vs, np.asarray(n["throat.inscribed_diameter"]) / (2 * vs)

    rx, rr = get(net_ref)
    px, pr = get(net_pred)
    out = match_throats(rx, rr, px, pr, min_tol=min_tol)
    out.pop("pairs")
    return out


# ---------------------------------------------------------------- one call for everything
def primary_metrics(pred, ref, voxel_size=None, net_pred=None, net_ref=None, cache=None):
    """All primary-tier metrics of pred against ref. `cache` may hold ref-side results
    (keys 'topo', 'skel') so they are computed once per reference mask."""
    cache = {} if cache is None else cache
    if "topo" not in cache:
        cache["topo"] = topology_summary(ref, voxel_size)
    if "skel" not in cache:
        cache["skel"] = skeleton(ref)
    out = dict(dice=dice(pred, ref), porosity_pred=porosity(pred), porosity_ref=porosity(ref),
               porosity_err=porosity_error(pred, ref))
    out.update(topology_errors(pred, ref, voxel_size, ref_summary=cache["topo"]))
    out.update(cldice(pred, ref, skel_ref=cache["skel"]))
    if net_pred is not None and net_ref is not None:
        out.update({f"throat_{k}" if not k.startswith("throat") else k: v
                    for k, v in throat_errors(net_pred, net_ref).items()})
    return out
