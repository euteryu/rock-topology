# Lab notebook

Dated log of what ran, what happened and what was decided. Newest entries at the bottom.
Gate approvals are written here by the owner.

## 2026-11-12

- Project chosen: port the method of arXiv 2607.28327 (coronary connectedness metric and
  FFR-CT agreement) to digital rock, with permeability in place of FFR.
- First literature review completed (docs/gate0-review.md). Verdict: Q2 open at moderate
  confidence, Q1 and Q3 partly done. Only two papers were read in full.
- Decision: the perturbation study (Phase 3) is the core of the paper. The trained-model
  comparison (Phase 4) is a slim second part.
- Decision: primary metrics are Dice, porosity error, Euler-number error, Betti error,
  clDice and throat-level error.
- Decision: no local job over 1 hour; heavy runs go to Kaggle.
- Gate 0: NOT yet approved. Remaining reading is listed in CLAUDE.md, Phase 0.

## 2026-11-12 (Claude Code session 1: Phases 0-2)

Setup
- `rock-topology.zip` was not present; the folder was already extracted, so it was used as is.
  `git init` run. Python 3.12 venv in `.venv` (managed with uv); PoreSpy 3.3, OpenPNM 3.6,
  torch 2.15 CPU, scikit-image 0.26. Package installed editable from `pyproject.toml`.

Phase 0 (literature)
- Two background passes: the listed papers (`docs/lit/notes-listed.md`, 18 items: 12 full
  text, 5 abstract only, Saxena 2017 and Andrä 2013 not accessed) and a fresh search
  (`docs/lit/notes-search.md`, 72 queries plus OpenAlex citation sweeps).
- Hard-stop check (a): **no paper found answers Q2 or the core perturbation question.**
  Closest: Eshimiakhe et al. 2026 TGRS (abstract only, medium threat until read),
  Fernandes et al. 2024 Sci. Rep. (permeability-surrogate loss for super-resolution, not
  segmentation), Hayatdavoudi et al. 2025/2026 (DRP-317, BCE loss, no correlation analysis).
- Wrote `docs/novelty.md` (draft for Gate 0) and `docs/refs.bib` (54 entries, each with a
  "Verified:" note; entries marked not accessed must not be cited).
- Corrections to the brief logged in `CLAUDE.md` section 8.

Phase 1 (data, pre-registration)
- `data/MANIFEST.md` written from source pages. DRP-317 segmentation settled: IsoData.
  DRP-317 licence ODC-BY 1.0; 11 binary volumes 10.2 GiB (under the 20 GB stop); all 33
  volumes 30.7 GiB (over it, so a hard stop if the greyscale volumes of all samples are needed).
- `docs/prereg.md` drafted (for Gate 1).
- Decision: Phase 3 reference permeability is the simulated k of the same crop, not lab k
  (Neumann et al. show lab k is reached only at the full 1000³ cube).
- Decision: test-sample rule for Phase 4 proposed (lab-porosity ranks 2, 6, 10), to be
  confirmed by the owner at Gate 1.
- Download of the Gate 2 benchmark (Fontainebleau, 1 MB) and Berea (2 x 954 MiB) was
  **blocked by the session's permission settings** (curl denied). Not worked around.

Phase 2 (CPU pipeline)
- `src/rocktopo/`: io, metrics (primary tier), network (SNOW2), flow (LBM + PNM), degrade,
  segment (Otsu, IsoData, watershed), pipeline. Tests in `tests/` (31 tests).
- Decision: voxel solver = own D3Q19 TRT lattice-Boltzmann in linear Stokes form, sparse
  (pore voxels only), torch, so the same code runs on a Kaggle GPU. Reason: no maintained
  pip-installable Stokes/LBM solver for binary images; the TRT "magic" scheme gives
  viscosity-independent k and an exactly placed wall, both checkable by analytic tests.
- Decision: inlet/outlet = 3 fluid buffer layers each end ("buffer"), not mirroring.
  Mirroring doubles the length and converges about 4x slower; the two differ by about 1%
  on a synthetic medium (to be quantified on real crops in `analysis/solver_uncertainty.py`).
- Decision: lattice viscosity 0.1 (fastest convergence in a small trial; k does not depend
  on it, which is tested).
- Decision: convergence by Aitken extrapolation of the geometric tail, with the remaining
  tail reported per run. Checked against a long run in
  `results/solver_verification_synthetic/`.
- Decision: topology uses 6-connected pore / 26-connected grain (fluid needs a face to
  pass). Euler number computed directly (V - E + F - C); matches scikit-image in a test.
- Decision: throat matching = one-to-one minimum-distance assignment, pair allowed if
  distance <= max(reference throat radius, 2 voxels).
- Bug found and fixed: SNOW2 throats can be wider than an adjacent pore; OpenPNM's
  sphere-and-cylinder conduit refuses this, so such throats are clipped to 0.99 x the
  smaller pore and the count is reported.
- Bug found and fixed: OpenPNM's default PyPardiso solver loads a second Intel OpenMP
  runtime next to torch's and aborts the process; the PNM now uses SciPy's direct solver.
- Ad hoc trial (not a reported result, no results/ file): grid refinement on a voxelised
  tube of radius 5 voxels changed k by about 4% (x1 to x2) and 1.7% (x2 to x4), so lattice
  error is not negligible for narrow throats. This is why
  the refinement study on real crops matters (prereg section 6).
- Gate 2 NOT reached: the benchmark reproduction needs the Fontainebleau download.
- Ran `analysis/solver_verification_synthetic.py` -> `results/solver_verification_synthetic/`.
  Plates exact, tube -2.7%, viscosity-independent, Aitken within 0.03% of the long run,
  mirror vs buffer +1.05%, PNM/LBM 0.43. Grid refinement x1 -> x2 on a synthetic medium with
  1-2-voxel throats changed k by -34%.
- Decision (prereg section 6, before any real data): all masks are solved on a refined
  lattice whose factor is fixed from the real-data refinement study.
- Decision: label resampling candidates extended with "majority_tie_pore" and
  "porosity_matched", because plain majority sends ties to grain and so biases towards
  closing throats (seen on a synthetic trial). The choice rule in prereg is unchanged.
- Gate reports written: docs/gates/gate0-report.md, gate1-report.md, gate2-report.md
  (Gate 2 not reached: data download blocked).
- Waiting on the owner: download permission or manual download; Gate 0 and Gate 1 sign-off;
  download scope for greyscale volumes (hard stop b).
