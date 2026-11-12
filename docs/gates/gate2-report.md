# Gate 2 report: CPU pipeline (2026-11-12): NOT YET REACHED

Report-and-continue gate. **Status: pipeline built and verified on synthetic geometry; the
benchmark reproduction that defines Gate 2 has not run**, because the download of the
benchmark image was blocked by this session's permission settings.

## Five-line summary

1. Library `src/rocktopo/` is built: SNOW2 networks, LBM and PNM permeability, the
   primary-tier metrics, degradation, label resampling and the three baselines. All 31 tests pass.
2. The voxel solver matches theory: parallel plates to machine precision, a voxelised
   tube within 2.7%, with no viscosity dependence.
3. Lattice error is large when throats are only 1–2 voxels wide (about 34% from ×1 to ×2 on a
   synthetic medium), so the pre-registration now requires solving on a refined lattice.
4. PNM gave 0.43× the LBM permeability on the synthetic medium. This will be measured on real crops.
5. Next: download Fontainebleau (1 MB) and Berea (954 MiB), run `analysis/gate2_benchmark.py`
   and `analysis/solver_uncertainty.py`.

## Numbers (all from `results/solver_verification_synthetic/metrics.json`)

| Check | Result |
|---|---|
| Parallel plates, gap 4/10/20 voxels, vs discrete exact profile | rel. error ≤ 1e-10 |
| Same, vs continuum h³/12 | 3.1%, 0.50%, 0.13% (midpoint-rule effect, 1/(2h²)) |
| Straight tube, R_eq = 10.03 voxels, vs πR⁴/(8L²) | −2.70% |
| Viscosity independence (ν = 1/6, 0.1, 0.5, 1) | spread 3.7e-7 |
| Aitken extrapolation vs run converged to 1e-7 | +0.03% (1300 vs 6200 steps) |
| Inlet/outlet "mirror" vs "buffer" | +1.05% |
| Grid refinement ×1 → ×2, synthetic 48³ medium (1–2-voxel throats) | −33.8% |
| PNM / LBM, synthetic 64³ medium | 0.427 (60 of 774 throats clipped) |
| Cost | 0.25 µs per pore voxel per step (measured while the test suite was also running) |

## Batch planning implication

At about 0.2 to 0.25 µs per pore voxel per step and about 1,300 to 1,800 steps, a 256³ crop
at 20% porosity is about 15–20 minutes per flow direction on the owner's PC, before any
lattice refinement. That is acceptable for checks, but the Phase 3 batch belongs on Kaggle
(the same torch code runs on GPU). An exact estimate comes with the benchmark before Phase 3
(hard stop d).

## To finish Gate 2

1. `data/raw/andra2013_fontainebleau/segmented-exxon.raw.gz` (1 MB), then
   `python analysis/gate2_benchmark.py --axis 0` (then 1 and 2, then `--pnm`, then `--summary`).
   Pass criterion: the mean of the x, y, z permeabilities lies within the published 1503 (LBM)
   to 1914 (EJ-Stokes) mD range. The local runtime estimate is about 20–30 minutes per axis.
2. Berea binary volume (954 MiB): `analysis/solver_uncertainty.py` on 3 crops, and
   `analysis/label_resampling.py`.
