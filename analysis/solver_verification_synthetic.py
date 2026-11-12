"""Phase 2 solver verification on synthetic geometry (no downloaded data needed).

Writes results/solver_verification_synthetic/metrics.json with:
  - parallel plates and straight tube against theory;
  - viscosity independence;
  - Aitken-extrapolated k versus a run converged to 1e-7 per 100 steps;
  - buffer versus mirror inlet/outlet;
  - grid refinement (x1, x2) of a synthetic porous medium;
  - PNM / LBM ratio;
  - cost per pore voxel per step, for batch planning.
Runtime about 10 minutes on the owner's PC.
"""
import numpy as np
import porespy as ps

from rocktopo import flow, network
from rocktopo.pipeline import Run


def main():
    run = Run("solver_verification_synthetic", dict(script=__file__))
    res = {}

    rows = []
    for h in (4, 10, 20):
        m = np.zeros((8, 4, h + 2), bool)
        m[:, :, 1:1 + h] = True
        r = flow.lbm_permeability(m, axis=0, side_walls=False, mode="periodic", tol=1e-9, dtype="float64")
        Lx = h + 2
        rows.append(dict(h=h, k=r["k_vox2"], k_discrete=(h ** 3 + h / 2) / (12 * Lx),
                         k_continuum=h ** 3 / (12 * Lx)))
        run.log(f"plates h={h}: k/k_discrete-1 = {r['k_vox2'] / rows[-1]['k_discrete'] - 1:.2e}, "
                f"k/k_continuum-1 = {r['k_vox2'] / rows[-1]['k_continuum'] - 1:.2e}")
    res["plates"] = rows

    R, L = 10.0, 24
    yy, xx = np.mgrid[:L, :L]
    disc = (yy - (L - 1) / 2) ** 2 + (xx - (L - 1) / 2) ** 2 < R ** 2
    tube = np.repeat(disc[None], 6, axis=0)
    r = flow.lbm_permeability(tube, axis=0, mode="periodic", tol=1e-9, dtype="float64")
    R_eq = np.sqrt(disc.sum() / np.pi)
    kt = np.pi * R_eq ** 4 / (8 * L ** 2)
    res["tube"] = dict(R_eq=R_eq, k=r["k_vox2"], k_theory=kt, rel_err=r["k_vox2"] / kt - 1)
    run.log(f"tube R_eq={R_eq:.2f}: rel err {res['tube']['rel_err']:.3%}")

    ks = [flow.lbm_permeability(tube, axis=0, nu=nu, mode="periodic", tol=1e-9, dtype="float64")["k_vox2"]
          for nu in (1 / 6, 0.1, 0.5, 1.0)]
    res["viscosity_spread"] = float(np.ptp(ks) / np.mean(ks))
    run.log(f"viscosity independence: relative spread {res['viscosity_spread']:.2e}")

    im = ps.generators.blobs(shape=[64, 64, 64], porosity=0.35, blobiness=1, seed=1)
    a = flow.lbm_permeability(im, axis=0)
    b = flow.lbm_permeability(im, axis=0, tol=1e-7, extrapolate=False, max_steps=60_000)
    res["aitken"] = dict(k_aitken=a["k_vox2"], steps_aitken=a["steps"], k_long=b["k_vox2"],
                         steps_long=b["steps"], long_converged=b["converged"],
                         rel_diff=a["k_vox2"] / b["k_vox2"] - 1)
    run.log(f"Aitken vs long run: {res['aitken']['rel_diff']:.3%} ({a['steps']} vs {b['steps']} steps)")
    res["cost_us_per_node_step"] = 1e6 * a["seconds"] / (a["steps"] * a["n_nodes"])
    run.log(f"cost {res['cost_us_per_node_step']:.3f} us per pore voxel per step")

    mi = flow.lbm_permeability(im, axis=0, mode="mirror")
    res["bc_buffer_vs_mirror"] = dict(k_buffer=a["k_vox2"], k_mirror=mi["k_vox2"],
                                      rel_diff=mi["k_vox2"] / a["k_vox2"] - 1)
    run.log(f"mirror vs buffer: {res['bc_buffer_vs_mirror']['rel_diff']:.3%}")

    gr, rel = flow.grid_refinement(im[:48, :48, :48], axis=0, voxel_size=1.0, factors=(1, 2))
    res["grid_refinement"] = dict(rows=gr, rel_change=rel)
    run.log(f"grid refinement x1 -> x2: relative change {rel:.3%}")

    net = network.extract(im, voxel_size=1e-6)
    kp = flow.pnm_permeability(net, im.shape, axis=0, voxel_size=1e-6)
    res["pnm_over_lbm"] = kp["k_m2"] / (a["k_vox2"] * 1e-12)
    res["n_throats_clipped"] = kp["n_throats_clipped"]
    res["n_throats"] = kp["n_throats"]
    run.log(f"PNM/LBM = {res['pnm_over_lbm']:.3f} ({kp['n_throats_clipped']} of {kp['n_throats']} "
            f"throats clipped to pore size)")
    run.save(res)


if __name__ == "__main__":
    main()
