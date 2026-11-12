"""Phase 2 solver checks on real sub-volumes (CLAUDE.md Phase 2).

1. Grid refinement: each crop is solved on its own lattice and on a lattice refined x2
   (geometry unchanged). The relative change is the solver's discretisation error; the
   median over crops is delta_solver in docs/prereg.md section 6.
2. Boundary-condition sensitivity: "buffer" versus "mirror" inlet/outlet.
3. PNM versus LBM on the same crops.

DRP-317 binary volumes: uint8, 1000^3, little-endian, 0 = pore, 2.25 um (data/MANIFEST.md).
Per the manifest, the published DRP-317 masks include isolated pores; the solvers here
remove non-spanning clusters themselves.

Run one crop per invocation so every local job stays under the 1-hour cap, e.g.
    python analysis/solver_uncertainty.py --raw data/raw/drp317_berea/Berea_2d25um_binary.raw \
        --name berea --crop 0 --size 96
Then: python analysis/solver_uncertainty.py --summary --name berea
"""
import argparse
import json
from pathlib import Path

import numpy as np

from rocktopo import flow, io, network
from rocktopo.pipeline import Run

VOXEL = 2.25e-6
SHAPE = (1000, 1000, 1000)
# Three crop origins on a diagonal, away from the edges; fixed before looking at results.
ORIGINS = [(150, 150, 150), (450, 450, 450), (700, 700, 700)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw")
    ap.add_argument("--name", required=True)
    ap.add_argument("--crop", type=int)
    ap.add_argument("--size", type=int, default=96)
    ap.add_argument("--axis", type=int, default=0)
    ap.add_argument("--summary", action="store_true")
    args = ap.parse_args()
    out = f"solver_uncertainty_{args.name}_{args.size}"

    if args.summary:
        d = Path("results") / out
        rows = [json.loads(p.read_text()) for p in sorted(d.glob("crop*.json"))]
        ref = [r["refinement_rel_change"] for r in rows]
        bc = [r["bc_rel_diff"] for r in rows]
        ratio = [r["pnm_over_lbm"] for r in rows if r.get("pnm_over_lbm")]
        s = dict(n=len(rows), refinement_rel_change=ref, delta_solver_median=float(np.median(ref)),
                 bc_rel_diff=bc, pnm_over_lbm=ratio)
        (d / "summary.json").write_text(json.dumps(s, indent=2))
        print(json.dumps(s, indent=2))
        return

    vol = io.read_raw(args.raw, SHAPE, "uint8")
    mask = io.crop(vol, args.size, ORIGINS[args.crop]) == 0
    del vol
    run = Run(out, dict(raw=args.raw, crop=args.crop, origin=ORIGINS[args.crop], size=args.size,
                        axis=args.axis, voxel_size=VOXEL))
    run.log(f"crop {args.crop}: porosity {mask.mean():.4f}")
    rows, rel = flow.grid_refinement(mask, axis=args.axis, voxel_size=VOXEL, factors=(1, 2),
                                     max_seconds=1500)
    for r in rows:
        run.log(f"refine x{r['factor']}: k = {r['k_m2'] / flow.MILLIDARCY:.2f} mD, "
                f"{r['steps']} steps, {r['seconds']:.0f} s, converged {r['converged']}")
    mir = flow.lbm_permeability(mask, axis=args.axis, voxel_size=VOXEL, mode="mirror", max_seconds=900)
    kb = rows[0]["k_m2"] / flow.MILLIDARCY
    bc = abs(mir["k_mD"] - kb) / kb if kb else float("nan")
    run.log(f"mirror BC: k = {mir['k_mD']:.2f} mD (buffer {kb:.2f}); rel diff {bc:.3%}")
    net = network.extract(mask, voxel_size=VOXEL)
    pnm = flow.pnm_permeability(net, mask.shape, axis=args.axis, voxel_size=VOXEL)
    ratio = pnm["k_mD"] / kb if kb else None
    run.log(f"PNM: k = {pnm['k_mD']:.2f} mD; PNM/LBM = {ratio}")
    run.save(dict(crop=args.crop, porosity=float(mask.mean()), refinement=rows,
                  refinement_rel_change=rel, k_buffer_mD=kb, k_mirror_mD=mir["k_mD"],
                  bc_rel_diff=bc, pnm=pnm, pnm_over_lbm=ratio,
                  n_throats=network.throat_count(net)), f"crop{args.crop}.json")


if __name__ == "__main__":
    main()
