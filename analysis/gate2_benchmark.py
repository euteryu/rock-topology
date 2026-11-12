"""Gate 2: reproduce published permeability on a benchmark sample.

Fontainebleau (Andra et al. 2013 benchmark repository, file segmented-exxon.raw.gz):
uint8 288 x 288 x 300 (nx, ny, nz), 7.5 um voxels, published porosity 0.147.
Published permeability (repository spreadsheet results/simulations.ods, see data/MANIFEST.md
section 6): EJ-Stokes 1914 mD and LBM 1503 mD (mean of x, y, z). Paper values NOT yet
checked against Andra et al. 2013 part II (not opened).

One flow axis per invocation, so each local job stays well under the 1-hour cap
(CLAUDE.md section 6). Example:
    python analysis/gate2_benchmark.py --axis 0
    python analysis/gate2_benchmark.py --axis 1
    python analysis/gate2_benchmark.py --axis 2
    python analysis/gate2_benchmark.py --pnm
    python analysis/gate2_benchmark.py --summary
"""
import argparse
import gzip
import json
from pathlib import Path

import numpy as np

from rocktopo import flow, metrics, network
from rocktopo.pipeline import Run, geometric_mean_k

RAW = Path("data/raw/andra2013_fontainebleau/segmented-exxon.raw.gz")
OUT = "gate2_fontainebleau"
VOXEL = 7.5e-6
SHAPE = (300, 288, 288)  # (nz, ny, nx), x fastest in the file
PUBLISHED = {"EJ-Stokes": 1914.0, "LBM": 1503.0}


def load():
    with gzip.open(RAW, "rb") as f:
        a = np.frombuffer(f.read(), np.uint8)
    if a.size != np.prod(SHAPE):
        raise ValueError(f"unexpected size {a.size}")
    a = a.reshape(SHAPE)
    vals, counts = np.unique(a, return_counts=True)
    # Label convention is not documented: pick the value whose fraction is nearest 0.147.
    frac = counts / a.size
    pore_value = vals[np.argmin(np.abs(frac - 0.147))]
    return a == pore_value, dict(zip(vals.tolist(), frac.tolist())), int(pore_value)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--axis", type=int)
    ap.add_argument("--pnm", action="store_true")
    ap.add_argument("--summary", action="store_true")
    ap.add_argument("--max-seconds", type=float, default=3300)
    args = ap.parse_args()

    if args.summary:
        d = Path("results") / OUT
        ks = []
        for a in range(3):
            p = d / f"lbm_axis{a}.json"
            if p.exists():
                ks.append(json.loads(p.read_text())["k_mD"])
        res = dict(k_lbm_axes_mD=ks, published_mD=PUBLISHED)
        if len(ks) == 3:
            # Published values are arithmetic means of x, y, z, so compare like with like.
            res["k_lbm_mean_mD"] = float(np.mean(ks))
            res["k_lbm_geomean_mD"] = geometric_mean_k(ks)
            lo, hi = min(PUBLISHED.values()), max(PUBLISHED.values())
            res["within_published_range"] = bool(lo <= res["k_lbm_mean_mD"] <= hi)
            res["rel_to_published"] = {k: res["k_lbm_mean_mD"] / v - 1 for k, v in PUBLISHED.items()}
        (d / "summary.json").write_text(json.dumps(res, indent=2))
        print(json.dumps(res, indent=2))
        return

    mask, fractions, pv = load()
    run = Run(OUT, dict(sample="Fontainebleau (Andra 2013)", file=str(RAW), voxel_size=VOXEL,
                        shape=SHAPE, pore_value=pv, value_fractions=fractions))
    run.log(f"porosity {metrics.porosity(mask):.4f} (pore value {pv}); fractions {fractions}")
    if args.axis is not None:
        r = flow.lbm_permeability(mask, axis=args.axis, voxel_size=VOXEL,
                                  max_seconds=args.max_seconds)
        hist = r.pop("history")
        run.log(f"axis {args.axis}: k = {r['k_mD']:.1f} mD, {r['how']}, steps {r['steps']}, "
                f"tail {r['tail']:.3%}, {r['seconds']:.0f} s")
        run.save(dict(r, history=hist), f"lbm_axis{args.axis}.json")
    if args.pnm:
        net = network.extract(mask, voxel_size=VOXEL)
        pnm = {a: flow.pnm_permeability(net, mask.shape, axis=a, voxel_size=VOXEL) for a in range(3)}
        for a, r in pnm.items():
            run.log(f"PNM axis {a}: k = {r['k_mD']:.1f} mD")
        run.save(dict(pnm=pnm, n_throats=network.throat_count(net),
                      snow2_seconds=net["param.seconds"]), "pnm.json")


if __name__ == "__main__":
    main()
