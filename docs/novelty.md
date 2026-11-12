# Novelty statement (DRAFT for Gate 0, owner sign-off required)

Status: **draft, 2026-11-12. Not approved.** Per `CLAUDE.md` rule 3, this file is the only
place novelty is stated, and nothing here counts until the owner signs it off in
`docs/lab-notebook.md`. No "first to do this" wording is used anywhere until then.

Sources: `docs/gate0-review.md` (first pass), `docs/lit/notes-listed.md` (the papers listed in
`CLAUDE.md`, 18 items), `docs/lit/notes-search.md` (fresh search, 72 queries plus OpenAlex
citation sweeps of Wang 2021, clDice, Skeleton Recall and Krygier 2021). Every paper named
below is in `docs/refs.bib`, with its access level.

Rock terms: *permeability* = how easily fluid flows through the rock; *throat* = narrow neck
between two pore bodies; *percolation threshold* = porosity below which no connected path
crosses the sample; *LBM* = lattice-Boltzmann voxel flow solver. See `docs/glossary.md`.

## Hard-stop check (CLAUDE.md 2.1a)

**No paper found answers Q2 or the core perturbation question.** Both literature passes
checked this explicitly. The verdict still rests on absence of evidence: two close abstracts
(Eshimiakhe 2026, Li/Aslam/Yan 2025) have not been read in full. See "Open checks" below.

## Origin of the idea (cite always)

Wang, Shabaninejad, Armstrong & Mostaghimi 2021 (Applied Soft Computing 104:107185; arXiv
2002.05322; full text read by the first review) showed rock segmentations with over 95% voxel
accuracy whose permeability and connectivity were badly wrong. One model had the best Euler
match yet zero permeability. They suggested using connectivity or approximate flow "directly
as a loss function". This project tests that suggestion systematically. It does not propose a
new idea.

## Q1: which segmentation metric best predicts permeability error?

**Closest prior work**
- Wang et al. 2021: anecdotal disagreement between voxel accuracy, Euler number and LBM
  permeability. One test volume, four architectures, no correlation analysis.
- Hongsheng Wang et al. 2024, SPE J. 29:5779 (full text): five U-Net variants. "The higher
  pixel-wise metrics do not necessarily correlate with better performance in physics-based
  metrics". BCE loss, no metric ranking.
- Hayatdavoudi et al. 2025 Sci. Rep. and 2026 JPEPT (full text): on **our primary dataset**
  (DRP-317), 12 CNNs plus Otsu, with LBM/PNM permeability and Euler number per model. No
  perturbations, no correlation analysis.
- Leu et al. 2014 TiPM (full text): threshold sweeps on Berea move permeability between 600
  and 1000 mD while porosity stays at 16–19%, because "pore throats were found to be open
  for flow at large thresholds but closed for smaller thresholds". Global sweeps only.
- Garfi et al. 2020 TiPM (full text): permeability is the property most sensitive to the
  processing pipeline, tracking throat-radius shifts. Two pipelines only.
- Gärttner et al. 2023 Comput. Geosci. (full text): graph max-flow tracks permeability
  (log R² 0.87) on Bentheimer at 2.25 µm; segmentation is taken as ground truth.
- Eshimiakhe et al. 2026 IEEE TGRS (**abstract only**): high Dice but lost percolating
  connectivity after synthetic-to-real transfer; a new "Connectivity Domain Gap" metric.
- Owusu-Ansah et al. 2026 (arXiv 2607.28327, full text): the source method, in coronary CT.
  Breaks versus narrowing perturbations; rank regression, a clustered GEE joint model and a
  clustered bootstrap. Not rock.

**Exact gap.** No paper found applies controlled, error-type-specific perturbations to rock
masks (throat-only versus body-only errors, single-throat closures, false bridges, and a
crossed closure × narrowing factorial at matched porosity change) and then ranks Dice,
clDice, Betti-0/1 error, Euler error, porosity error and a one-to-one throat-matching error
against permeability error. In particular, nobody has reported partial correlations that
control for porosity error, or a joint model with all metrics entered together.

**Status: partly done** (the motivating observation is established; the systematic test is not).

## Q2: do topology-aware losses reduce permeability error at matched Dice?

**Closest prior work**
- Wang et al. 2021: the suggestion, not executed.
- Fernandes et al. 2024 Sci. Rep. (full text): back-propagates a permeability loss through a
  frozen permeability-predicting CNN to fine-tune a **super-resolution** network. Not
  segmentation, no topology loss, no matched-overlap comparison. The authors note that the
  flow-proxy loss adds artefacts and small pores.
- Owusu-Ansah et al. 2026 (coronary): Skeleton Recall improved FFR-CT agreement by about
  10 points; clDice did not.
- Acebes et al. 2026, STACOM 2025 (abstract only): topology losses gave "limited benefits"
  on primary coronary segments; label noise dominated elsewhere. A prior that favours a null
  result.
- Kirchhoff et al. 2024 (Skeleton Recall) and Shit et al. 2021 (clDice), full text: no
  porous media, no flow evaluation. clDice explicitly assumes tubular structures.
- Tang et al. 2026 Energy & Fuels (abstract only): the only porous-media paper among the 71
  works citing Skeleton Recall. 2D shale fractures, no flow; whether a topology loss is used
  is not stated in the abstract.
- Marfo et al. 2026 review: none of its 154 references trains a topology-aware loss.

**Exact gap.** No paper found trains clDice, soft-clDice, Skeleton Recall, Betti or Euler
losses for rock or porous-media micro-CT segmentation and scores them by simulated
permeability at matched Dice.

**Status: open (moderate confidence; absence of evidence).**

## Q3: does the answer depend on resolution and porosity?

**Closest prior work**
- Saxena et al. 2018 AWR (abstract only): "at least 10 voxels are needed to sufficiently
  resolve pore throats for single phase fluid flow simulations".
- Saxena et al. 2017 Mar. Pet. Geol.: **not accessed at all**. The "2, 4 and 8 µm, five
  sandstones" details in `CLAUDE.md` are unverified and must not be cited until the owner
  provides the paper.
- Tavakkoli et al. 2026, SCA2026-037 (full text): binary and greyscale LBM diverge by 93%
  at coarse resolution.
- Li, Yang & Zhang 2024 WRR (abstract only): recovering partial-volume throats improves
  permeability accuracy at coarse resolution.
- Robins et al. 2016 WRR (abstract only): persistence analysis estimates the critical
  percolating radius.
- Jacob et al. 2021 Solid Earth (abstract): in tight sandstone, unresolved pores dominate the
  error. This limits what a binary label can mean at low porosity.

**Exact gap.** The interaction is untested: whether topological errors (closed throats)
dominate permeability error near the percolation threshold and at coarse voxels, while
throat-calibre errors dominate in well-connected, well-resolved rock, as separated by a
factorial perturbation design.

**Status: partly done** (resolution effects are known; error-type × regime interaction is not).

## Draft novelty statement (for the owner to edit)

> Segmentations of rock micro-CT can reach high voxel accuracy while giving permeability and
> connectivity that are badly wrong (Wang et al. 2021), and connectivity- or flow-based
> training objectives have been suggested but, to our knowledge, not tested for
> segmentation. Using public sandstone micro-CT with laboratory permeability (DRP-317), we
> (i) apply controlled, error-type-specific perturbations to reference segmentations
> (throat closures, throat narrowing, pore-body errors, false bridges) and test which
> evaluation metric best predicts permeability error after controlling for porosity
> error; (ii) test whether this depends on porosity and resolution, especially near the
> percolation threshold; and (iii) in a smaller second part, test whether a topology-aware
> loss developed for vessels (Skeleton Recall) reduces permeability error at matched Dice.
> We adapt a one-to-one throat-matching metric from bifurcation-level scoring in coronary
> CT (Owusu-Ansah et al. 2026). Our search covered the main digital-rock venues and citation
> lists of the key papers, but some conference and non-English work may have been missed.

The phrase "to our knowledge" stays only if the owner approves it at Gate 0.

## Open checks before the owner signs off

1. **Eshimiakhe et al. 2026 (IEEE TGRS), full text.** Check whether they use a connectivity
   loss, whether permeability is simulated, and whether the Connectivity Domain Gap is
   correlated with permeability across models. It is listed as hybrid open access (CC BY), but
   the page did not render for the automated fetch. *Owner: please open it in a browser.*
2. **Li, Aslam & Yan 2025 (SPE J. 226188-PA)**, "physics-constrained" segmentation plus
   upscaling: the loss type is unknown.
3. **Saxena et al. 2017 (Mar. Pet. Geol.)**: needed to support the degradation design.
4. Optional: Callow et al. 2020 GJI (resolution and connectivity), Andrä 2013 parts I and II
   (to confirm the benchmark permeabilities used at Gate 2), Robins 2016 (open ANU PDF).

## Essential reading for the owner (priority order)

1. Wang et al. 2021: the origin.
2. Owusu-Ansah et al. 2026 (arXiv 2607.28327): the method being ported.
3. Leu et al. 2014: throats versus porosity, in plain numbers.
4. Kirchhoff et al. 2024 (Skeleton Recall).
5. Gärttner et al. 2023: max-flow as a connectivity descriptor.
6. Eshimiakhe et al. 2026: the closest recent paper (pending full text).
