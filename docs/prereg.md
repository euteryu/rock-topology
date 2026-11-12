# Pre-registration (DRAFT for Gate 1)

Status: **draft, 2026-11-12, not yet approved by the owner.** Nothing in this file may be
changed after Gate 1 approval without a dated entry in `docs/lab-notebook.md` saying what
changed and why, made before the affected analysis is run. Rock terms are defined in
`docs/glossary.md`.

## 1. Questions and hypotheses

- **Q1 (metrics, Phase 3, core of the paper).** Across controlled perturbations of
  reference masks, which primary-tier metric best predicts permeability error?
  - H1a: Dice is a weak predictor of |log10(k_pred/k_ref)| once porosity error is
    controlled for (partial Spearman |ρ| < 0.3).
  - H1b: at least one topology or throat metric (Euler, Betti-1, clDice or throat
    metrics) has a larger partial |ρ| than Dice.
  - H1c (topology versus geometry, the headline factorial): at matched porosity change,
    *narrowing* throats causes a larger permeability error than *closing* the same
    fraction of throats in the high-porosity regime, and the reverse holds near the
    percolation threshold (low porosity, coarse voxels). An interaction term in the
    factorial model tests this.
- **Q3 (regime).** The effects in H1 depend on porosity and on voxel size relative to
  throat radius (interaction terms below).
- **Q2 (losses, Phase 4, secondary part).** At matched Dice, Dice+CE+Skeleton Recall
  gives lower |log10(k_pred/k_ref)| than Dice+CE. Predicted: no difference (null) in the
  high-porosity full-resolution regime; a reduction only at the coarsest degradation.

The working hypothesis in `CLAUDE.md` (loops make single breaks matter less) is tested,
not assumed. A null or reversed result on any hypothesis is reported in full.

## 2. Data and splits

- Primary data: 11 Sandstones (Digital Rocks Portal project 317), details in
  `data/MANIFEST.md`. Reference labels are the published segmented volumes.
- Sub-volumes: 256³ voxels (400³ if resources allow), non-overlapping, taken on a
  regular grid inside the scanned cylinder. The exact crop origins are written to
  `experiments/` before any metric is computed.
- **Splits are by rock sample, never by patch.** For Phase 4: at least 3 samples held out
  for test, chosen before training so that the lowest-porosity samples appear in both
  train and test (rule: rank samples by lab porosity, put ranks 2, 6 and 10 in test).
  Phase 3 uses all samples (no training is involved).
- REV check: on each sample, permeability of 128³, 192³ and 256³ crops from the same
  centre. If the 256³ value differs from the 192³ value by more than 25 %, that sample is
  flagged and analysed at 400³ (or excluded from per-sub-volume claims, with the reason
  logged).

## 3. Degradation (Phase 1 / Phase 4 input)

From `src/rocktopo/degrade.py`: Gaussian blur σ = 0.5 × factor (fine voxels), block-mean
downsampling by factor 2 and 4 (2.25 → 4.5 and 9 µm), additive Gaussian noise of
standard deviation 0.05 × (grain − pore median grey value). Labels are brought to the
coarse grid by the resampling method chosen in the label-resampling check (Section 6);
the choice rule is fixed now: the method with the smallest median absolute relative
change in permeability across samples, ties broken by the smallest change in Betti-1
density.

## 4. Perturbations (Phase 3)

Applied to reference masks, each at several magnitudes, three random seeds per
configuration where randomness is involved:

1. global erosion / dilation by 1, 2, 3 voxel layers;
2. throat-only errors: erosion or dilation restricted to voxels within the throat
   regions identified by SNOW2 (throat = voxels within 1 inscribed radius of the
   region-region interface);
3. body-only errors: the same restricted to pore-body voxels away from throats;
4. random closure of single throats: fractions 1, 2, 5, 10, 20 % of throats closed
   (throat interface voxels set to grain), widths elsewhere untouched;
5. false bridges: grain contacts thinner than 2 voxels opened, fractions as in 4.
6. **Factorial (headline):** factor A = fraction of throats closed {0, 2, 5, 10 %};
   factor B = throat narrowing {0, 1, 2 voxel layers on throat regions only};
   crossed fully, at each porosity level (native, and eroded towards percolation: the
   native mask eroded until porosity drops to 75 % and 50 % of native) and each
   resolution (2.25, 4.5, 9 µm labels). Matched porosity change is checked and reported;
   where it cannot be matched, porosity error enters as a covariate.

The exact magnitude grid and the run count will be written to `experiments/phase3.yaml`
with a timing benchmark before the batch, which is a hard stop for owner approval.

## 5. Outcome and metrics

**Primary outcome:** e = log10(k_pred / k_ref), with k from the lattice-Boltzmann solver
(`flow.lbm_permeability`), mean over the three flow axes (geometric mean of k). We report
|e| (magnitude) and e (signed bias). If k_pred = 0 (no spanning path), e is set to
log10(k_min / k_ref) with k_min = 10⁻³ × k_ref (a floor of −3) and the case is also
counted separately as "disconnection".

**Primary-tier metrics** (hypothesis tests; all computed by `src/rocktopo/metrics.py`):

| # | Metric | Definition |
|---|---|---|
| 1 | Dice | 2|P∩R| / (|P|+|R|) |
| 2 | Porosity error | φ(P) − φ(R) |
| 3 | Euler error | |Δχ| per mm³ (6-connected pore) |
| 4 | Betti-0 error | |Δβ0| per mm³ |
| 5 | Betti-1 error | |Δβ1| per mm³ |
| 6 | clDice | hard clDice, 3D skeletons by scikit-image `skeletonize` |
| 7 | Throat miss rate | unmatched reference throats / reference throats |
| 8 | Throat false rate | unmatched predicted throats / predicted throats |
| 9 | Throat radius error | mean |r_P − r_R| / r_R over matched throats |

Throat matching: SNOW2 networks of P and R (σ = 0.4, r_max = 4), throat position =
`throat.global_peak`, radius = `throat.inscribed_diameter`/2; one-to-one minimum-cost
matching with a pair allowed only if distance ≤ max(r_R, 2 voxels).

**Secondary tier** (reported, no headline claims): IoU, connected-porosity error,
Wasserstein-1 distance between pore-radius and between throat-radius distributions,
signed versions of metrics 3 to 5, throat F1, PNM permeability error.

**Exploratory tier** (appendix, labelled exploratory): surface area and integrated mean
curvature errors, graph max-flow (after Gärttner, Alpak et al. 2023), formation factor.

## 6. Solver checks fixed in advance (Phase 2)

- Analytic tests (parallel plates, straight tube, viscosity independence) must pass
  (`tests/test_flow.py`).
- Grid-refinement study on ≥ 3 sub-volumes (lattice refined ×2 with the geometry
  unchanged). The median relative change δ_solver is the solver's numerical error.
  **Any effect with |e| < log10(1 + δ_solver) is not reported as a finding.**
- **Lattice resolution rule (added 2026-11-12, before any real data was seen).** On a
  synthetic medium with 1–2-voxel throats, refining the lattice ×2 changed k by about a
  third (`results/solver_verification_synthetic/metrics.json`). Therefore every mask,
  including degraded ones, is solved on a lattice refined by an integer factor r (nearest-
  neighbour upsampling, geometry unchanged). r is chosen from the real-data refinement study
  as the smallest factor at which a further ×2 changes k by less than 5 % on all three crops;
  it is then fixed for each resolution level before the Phase 3 batch. The cost of r enters
  the batch time estimate (hard stop d).
- LBM convergence: relative change of k below 10⁻⁶ per 100 steps, or a stable Aitken
  extrapolation of the geometric tail (tail size recorded per run).
- PNM versus LBM disagreement is reported for every reference sub-volume.

## 7. Statistical analysis (Phase 3)

Unit of resampling is the **rock sample** (bootstrap over samples, 2000 resamples,
percentile 95 % CI).

1. Spearman rank correlation of each primary metric with |e|.
2. Partial Spearman correlation of each metric with |e| controlling for |porosity error|
   (rank-based partial correlation via residuals of rank regressions).
3. Joint regression: |e| ~ all nine primary metrics entered together (standardised),
   ordinary least squares with sample-clustered bootstrap CIs; and, as a robustness check,
   the same with a random intercept per sample.
4. Factorial (H1c): e ~ A × B × porosity level × resolution, with sample as a random
   intercept; the A×B×regime interaction is the test of H1c.
5. Multiple comparisons: Holm correction across the nine primary metrics, for each of
   analyses 1 and 2 separately; α = 0.05 family-wise.

**What counts as support.**
- H1a: upper 95 % CI bound of |partial ρ(Dice)| below 0.3.
- H1b: for at least one topology/throat metric, the bootstrap CI of
  |partial ρ(metric)| − |partial ρ(Dice)| excludes 0, Holm-adjusted p < 0.05.
- H1c: the interaction term has Holm-adjusted p < 0.05 and the sign pattern predicted
  (throat narrowing dominates in the native regime, closure near percolation). Any other
  pattern is reported as found.
- Q2: difference in mean |e| between losses, paired by test sub-volume, with a
  sample-level bootstrap CI excluding 0, after confirming the two models' mean Dice
  differ by less than 0.01. Three seeds per configuration; mean and spread reported.

## 8. What is not allowed

- Looking at Phase 4 test samples before the split and this plan are approved.
- Adding or dropping metrics from the primary tier after seeing Phase 3 results.
- Re-tuning perturbation magnitudes to obtain significance.
- Reporting effects below the solver-error floor as findings.

## 9. Open items to settle before approval

- Confirm the DRP-317 segmentation method and file format (`data/MANIFEST.md`).
- Benchmark the time per mask end to end, and the batch total, before Phase 3 (hard stop).
- Owner to confirm the test-sample rule in Section 2 once lab porosities are tabulated.
