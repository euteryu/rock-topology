"""Phase 1 label resampling check (CLAUDE.md Phase 1; docs/prereg.md section 3).

For each resampling method (majority, subsample, any, all) and factor (2, 4), measure the
change in Betti numbers, throat count and LBM permeability of the label alone, relative to
the fine label. The choice rule is fixed in docs/prereg.md: smallest median absolute
relative change in permeability across samples, ties broken by Betti-1 density.

One sample, crop and factor per call (stays under the 1-hour local cap), e.g.
    python analysis/label_resampling.py --raw data/raw/drp317_berea/Berea_2d25um_binary.raw \
        --name berea --factor 2
"""
import argparse

from rocktopo import degrade, io
from rocktopo.pipeline import Run

VOXEL = 2.25e-6
SHAPE = (1000, 1000, 1000)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", required=True)
    ap.add_argument("--name", required=True)
    ap.add_argument("--factor", type=int, default=2)
    ap.add_argument("--size", type=int, default=192)
    ap.add_argument("--origin", type=int, nargs=3, default=None)
    args = ap.parse_args()
    vol = io.read_raw(args.raw, SHAPE, "uint8")
    mask = io.crop(vol, args.size, args.origin) == 0
    del vol
    run = Run(f"label_resampling_{args.name}_x{args.factor}_{args.size}", vars(args))
    rows = degrade.label_resampling_check(mask, args.factor, VOXEL, lbm_kw=dict(max_seconds=600))
    for r in rows:
        run.log(", ".join(f"{k}={v:.4g}" if isinstance(v, float) else f"{k}={v}" for k, v in r.items()))
    run.save(dict(rows=rows))


if __name__ == "__main__":
    main()
