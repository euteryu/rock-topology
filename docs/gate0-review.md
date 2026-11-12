# Gate 0 literature review and novelty statement

Produced 12 November 2026 by an automated research task. It is a FIRST PASS, not a
sign-off: only two papers were read in full (see section I). Phase 0 of `CLAUDE.md`
lists what still has to be opened before Gate 0 can close.

## A. Verdict

**The planned paper looks partly novel. Q2 (topology-aware training losses judged by
permeability error) appears open. Q1 (which segmentation metric best predicts permeability
error) and Q3 (dependence on resolution and porosity) are partly done.** Confidence is
moderate: about 70% that no paper already does Q2 for rock micro-CT, and lower for Q1 and
Q3, because much of the relevant rock literature sits behind paywalls and was seen only as
abstracts.

The verdict rests on four observations.

1. The "high Dice, wrong permeability" finding is already established in rock. Wang,
   Shabaninejad, Armstrong and Mostaghimi showed networks with 95%+ voxelwise accuracy
   giving permeabilities and connectivities "orders of magnitude off", and those authors
   already proposed, as future work, using connectivity or an approximate flow measure
   "directly as a loss function". So the idea is at least six years old; what is missing
   is the execution.
2. The most comprehensive 2026 review (Marfo et al., MDPI *Advances in Carbon Neutrality*)
   recommends "using metrics that account for topology" but cites no topology-aware
   training loss and runs no experiments.
3. A dedicated hunt across rock, soil, battery-electrode, gas-diffusion-layer and fracture
   micro-CT found no paper that trains with clDice, Skeleton Recall, persistent-homology /
   Betti or Euler losses and reports permeability or flow error.
4. No paper found ranks clDice, Betti error, Euler error, porosity error and throat-level
   matching error against permeability error under controlled perturbations.

The defensible contribution is therefore a systematic, controlled TEST of an idea the rock
community has floated but not executed. It is not a new idea.

### Rock terms

- *Pore* = void space; *grain* = solid mineral.
- *Pore body* = a wide void region; *throat* = the narrow neck joining two bodies, which
  controls flow.
- *Permeability* = how easily fluid flows through the rock (the analogue of FFR-CT's flow
  quantity).
- *Pore-network model (PNM)* = the pore space reduced to a graph of bodies (nodes) and
  throats (edges), the analogue of a vessel centreline graph.
- *LBM* = lattice-Boltzmann method, a voxel-level flow solver.
- *Percolation threshold* = the porosity below which the pore space stops forming a
  connected path across the sample.
- *Euler characteristic* χ = β0 − β1 + β2 (components minus loops plus cavities).
- *Minkowski functionals* = volume, surface area, integrated mean curvature and Euler
  characteristic: the standard rock morphology set.
- *Formation factor* = a measure of electrical resistivity of the brine-filled pore
  space, a second transport check.
- *Sub-resolution porosity* = pores smaller than a voxel.

### What was read in full

In full: Wang et al. (arXiv 2002.05322 v2) and the main text of the MDPI review. For the
review's references, body citations were seen directly and entries 135–141 and 148–152
came from Crossref. Everything else was seen only as abstracts, search snippets or
secondary descriptions (section I).

## B. Per-question findings

### Q1: metric versus permeability error — PARTLY DONE

Closest prior work:

- **Wang et al. 2021 (full text read).** Trained SegNet, U-Net, ResNet and U-ResNet in 2D
  and 3D on Mt. Simon sandstone. Labels came from converging-active-contour segmentation
  guided by QEMSCAN mineral maps. Reported voxel accuracy, Euler number per phase, LBM
  permeability and two-phase Euler evolution. Euler errors reached "1000% in some cases".
  The U-ResNet-2D (UW) model had the BEST pore-space Euler match yet ZERO permeability,
  because of a disconnection "at a tight pore throat junction". The authors conclude "the
  Euler number is not entirely sufficient". All evaluation is on one 512×512×768 test
  volume.
- **Scientific Reports 2025 (s41598-025-07211-2; snippets only).** Compared CNN segmenters
  against Otsu using pixelwise metrics plus permeability (LBM, CFD, PNM) and formation
  factor; PNM permeability was lower, attributed to "loss of connectivity".
- **Phan, Ruspini & Lindseth 2021 (snippets).** 3-phase 3D tool reporting IoU, phase
  fractions, Euler number and connected-component counts.
- **Leu et al. 2014 (via the review).** Threshold and seed changes alter Berea throat
  connectivity and permeability.

Remaining gap: nobody has done controlled, error-type-specific perturbations (throat-only
versus body-only, single-throat closures, false bridges) or ranked Dice, clDice, Betti
error, Euler error, porosity error and one-to-one throat matching by rank correlation or
joint regression against permeability error.

### Q2: topology-aware losses — OPEN (moderate confidence)

Nothing found in rock or adjacent porous media. Nearest neighbours:

- **Wang et al. 2021** proposed physical-accuracy losses as future work.
- **Gärttner, Alpak et al. 2023** (Comput. Geosci.; arXiv 2109.01818) fed a graph max-flow
  value into a CNN that PREDICTS permeability; it does not segment.
- **Skeleton Recall** (Kirchhoff et al., arXiv 2404.03010) was tested on 2D concrete
  cracks and in 3D CT (ToothFairy, TopCoW), but never on porous media and with no flow
  evaluation.
- An MDPI crack paper used clDice-type losses only on 2D road cracks, with no CT and no
  flow.
- **Topological Filtering / PerSplat** (arXiv 2104.13430) is a persistence-based
  PRE-segmentation filter, not a loss, evaluated on tortuosity and Minkowski functionals
  of synthetic microstructures.
- **Geometrical-based GAN (2021)** uses persistent homology for image ENHANCEMENT, not
  segmentation (not verified beyond its abstract).

Remaining gap: topology-aware losses, trained in 3D on rock micro-CT and judged by
permeability error at matched Dice, appear untested.

### Q3: regime dependence — PARTLY DONE

- **Saxena et al. 2017** (Mar. Pet. Geol. 86:972; secondary descriptions only). Five
  sandstones imaged at 2, 4 and 8 µm: the uncertainty caused by threshold choice INCREASES
  as voxels coarsen; coarsening "led to rounding and smoothing of pore throats and a sharp
  decline in specific surface area which increased the computed permeability"; porosity
  changed little while flow and electrical properties changed a lot.
- **Saxena et al. 2018** (AWR, "operating envelope of DRP"; title only).
- **Robins et al. 2016** (WRR) linked persistent homology to the critical
  percolating-sphere radius in sandstones and bead packs.
- **Wang et al. 2021** found the zero-permeability failure in a "heterogeneous" sample
  whose flow path is "particularly tight".

Remaining gap: the INTERACTION is untested. Whether topological errors dominate near
percolation (low porosity, coarse voxels) while throat-calibre errors dominate elsewhere
has not been shown with error-type-separated perturbations.

## C. Papers that could kill this

None found substantially overlaps. The real threats, in order:

1. **Wang, Shabaninejad, Armstrong, Mostaghimi (arXiv 2002.05322; Applied Soft Computing
   104:107185).** Pre-empts the motivating headline and explicitly floats the Q2 idea in
   its conclusion: "certain measures of physical accuracy such as connectivity or an
   approximation of flow may be calculable or estimated in an efficient manner that is
   conducive to use directly as a loss function". Cite it as the origin of the idea and
   frame this paper as the first systematic test. It does not kill the paper: it compares
   architectures, not losses or metrics; it uses one test volume; and it never correlates
   metrics with permeability error.
2. **Marfo et al. 2026 review (MDPI Adv. Carbon Neutrality 1(2):6; preprints.org
   202608.0963).** Proposes a seven-dimension framework (class accuracy, boundary
   fidelity, topology, morphology, calibrated uncertainty, physical-property sensitivity,
   decision consequence) and a "property impact index" that multiplies per-voxel entropy
   by the permeability change from flipping that voxel's label. It states "No
   dataset-based ranking or expected-loss calibration is performed in this review". The
   idea of localised throat errors is pre-empted conceptually ("visually similar
   segmentations can yield substantially different predictions of permeability … when
   errors occur at critical pore throats"); the empirical test is not. In the text read,
   the review cites NO topology-aware training loss. Its topology content is
   evaluation-only: Euler characteristic, Betti numbers, connected components and
   percolation, plus Purswani et al., where threshold choice and small-cluster removal
   "could change the sign of the Euler characteristic".
   On "reference 138": in the published MDPI version, ref. 138 is Roy et al., Bayesian
   QuickNAT (NeuroImage 2019), an uncertainty paper. The graph connectivity / maximum-flow
   sentence cites ref. 152, Gärttner/Alpak et al. 2023. Numbering presumably differs in
   the preprints.org version, which was not opened.
3. **Enninful, "Topology-aware AI for porous materials" (Research Square rs-10932955,
   Sept 2026; snippet only).** A perspective proposing "counterfactual topology twins":
   descriptor-matched structures with deliberately different networks. Conceptually close
   to the perturbation design. Appears to target materials design (MOFs, adsorbents), not
   segmentation. Cite it, and frame the perturbations as concrete instances of such twins.
4. **Krygier et al. 2021 (Nat. Commun. 12:5414).** Propagates segmentation uncertainty via
   probability maps into physics quantities. Exemplars are woven composites, battery
   electrodes and a human torso; the woven-composite exemplar computes Stokes fluid
   permeability, but it is not rock and does not rank segmentation metrics. A baseline
   framing, not a competitor.
5. **Gärttner/Alpak et al. 2023.** Not a competitor, but reviewers will ask why max-flow
   is not used as a cheap connectivity metric. Include it in Q1.

## D. Why the gap exists

Partly overlooked and partly hard:

- **Communities do not overlap.** The topology-loss literature (clDice, Skeleton Recall,
  Betti matching) targets thin tubular structures in medical, road and neuron images. The
  digital-rock ML literature compares architectures and judges them by "physical
  accuracy", not by loss functions.
- **The tubularity assumption breaks.** clDice's homotopy guarantee is stated for tubular
  structures. Pore space is blobs joined by necks, so the soft skeleton of a large pore
  body is dominated by the body's medial surface, not by throats. A body-heavy skeleton
  loss may reward the wrong voxels. Skeleton Recall's tubed skeleton is similarly tuned
  for constant-calibre tubes.
- **The reference topology is uncertain.** Throats near voxel size are partial-volume
  voxels. A conservative threshold classifies mixed voxels as solid, while a liberal one
  creates false connections. The high-resolution-label / degraded-input design partly
  solves this, but the high-resolution labels still have their own sub-resolution throats.
- **Memory.** Kirchhoff et al. report that, averaged over five datasets, clDice loss adds
  "approximately 88% additional training time and 52% more VRAM" over plain nnU-Net,
  whereas Skeleton Recall adds "only an additional 8% training time and 2% higher VRAM
  consumption". Skeleton Recall is the practical 3D choice. Persistent-homology losses on
  128³ patches are likely prohibitive (inference, not measured).
- **Patch topology ≠ sample topology.** Permeability is a global, sample-spanning
  property. Patch-wise losses cannot see a break that only matters at the outlet; Wang et
  al.'s failure was exactly a disconnection near the outlet.
- **Easy rocks.** Clean quartz sandstones have well-separated histograms that support
  reproducible thresholding, so Otsu may already be near-optimal.
- **Looped networks.** Sandstone pore networks are highly looped. A single throat closure
  redistributes flow rather than amputating a subtree. This weakens the direct coronary
  analogy.

## E. Recommended sharpening

1. **Reframe Q2.** Ask whether topology losses reduce log-permeability error at matched
   Dice, and in which regime. Predict a null result in high-porosity clean sandstone and a
   positive effect only near percolation. A pre-registered null is publishable.
2. **Metric set reviewers will expect.** Dice/IoU; porosity and connected porosity; the
   four Minkowski functionals (especially Euler characteristic); Betti β0/β1; clDice;
   pore- and throat-size distributions; max-flow following Gärttner/Alpak; formation
   factor; throat-level matching. Report |log10(k_pred/k_ref)|, signed bias, and partial
   correlations controlling for porosity error.
3. **Baselines.** Otsu or IsoData thresholding; watershed; 3D U-Net with weighted CE and
   Dice+CE; nnU-Net defaults. For losses, prioritise Skeleton Recall and soft-clDice. Add
   a post-hoc connectivity filter that keeps the largest spanning cluster.
4. **Flow solvers.** Use one voxel solver (LBM or Stokes) and one PNM. Throat matching is
   done on the PNM, but permeability claims should rest on the voxel solver.
5. **Regime design.** Degrade 2.25 µm DRP-317 scans to roughly 4.5 and 9 µm, mirroring
   Saxena's 2/4/8 µm. Validate degradation realism on the MRCCM real paired carbonate data
   if usable. Include low-porosity members of the eleven sandstones, and erode to approach
   percolation. Report voxel size relative to throat radius.
6. **Statistics.** Sample-level splits, not slices. Multiple sub-volumes per rock, with
   permeability computed on REV-sized (representative elementary volume) domains.

## F. Datasets (details NOT yet verified unless stated)

| Dataset | Access | Size / voxel | Reference segmentation | Lab permeability | Notes |
|---|---|---|---|---|---|
| 11 Sandstones (Neumann, Andreeta, Lucas-Oliveira), DRP project 317 | Digital Rocks Portal, doi 10.17612/f4h1-w124 | 11 samples, 1000³ voxels, 2.25 µm (Bruker Skyscan 1272) | Yes: raw, filtered, segmented. Dataset authors say IsoData; a later user says Otsu + watershed | Yes: connected porosity 14–27%, permeability 9–386 mD | Best primary dataset |
| IBM microCT-Dataset (Esteves Ferreira et al., Sci. Data 2023) | figshare.plus doi 10.25452/figshare.plus.21375565; github.com/IBM/microCT-Dataset | 18 sandstone and carbonate plugs, full-plug tomographies | Binary volumes included | Yes, same plugs, 0.4 mD to above 5 D | Carbonate / low-permeability regime |
| MRCCM (Alqahtani et al.) | Noted in Alqahtani et al. TiPM 2022; URL not verified | Paired low/high resolution, 4× ratio; low-res pixel 10.72 µm | Processed volumes | Not verified | Only real paired source found; carbonate |
| DeepRock-SR (DRP 215), DRSRD1 (DRP 211) | Digital Rocks Portal | Not verified | Not verified | Not verified | Synthetic low-res via downsampling |
| Imperial College micro-CT images and networks | Imperial College collection | Roughly 300³–400³ crops | Binary images plus networks | Image-based only | Pore-network cross-checks |
| Krygier et al. data | Mendeley Data doi 10.17632/g3hr4rkb48.3 | Probability maps | Probability maps | Not rock | Uncertainty baselines |

Licences were not verified for any dataset.

**Pretrained weights:** none verified as downloadable. Phan et al.'s tool appears
commercial (SmartRocks). Wang et al. released code (github.com/yingDaWang-UNSW/SegNets-3D);
weights not verified. SAMamba3D and fine-tuned SAM for digital rock were not checked.

## G. Draft novelty statement

Deep-learning segmentation of rock micro-CT can reach over 95% voxelwise accuracy while
yielding permeabilities and connectivities that are orders of magnitude off. Use of
connectivity- or flow-based training objectives has been suggested, and recent reviews
call for topology-aware evaluation. To our knowledge, however, no study has (i)
systematically tested which segmentation evaluation metric best predicts permeability
error under controlled, error-type-specific perturbations, or (ii) evaluated
topology-aware training losses developed for vascular segmentation, such as soft-clDice
and Skeleton Recall, by their effect on simulated permeability at matched overlap
accuracy. We address both questions on public sandstone micro-CT data with laboratory
permeability. We introduce a one-to-one throat-matching metric adapted from
bifurcation-level connectedness scoring in coronary CT angiography. We also examine how
the answers depend on image resolution and porosity, with particular attention to
proximity to the percolation threshold, where highly looped pore networks may become as
sensitive to single broken connections as branching vascular trees. Our literature search
covered the main digital-rock venues, but some conference and non-English work may have
been missed.

## H. Reading list for the owner (priority order)

1. Wang, Shabaninejad, Armstrong & Mostaghimi 2021 (arXiv 2002.05322): closest
   predecessor; the zero-permeability / Euler counter-example and the loss suggestion.
2. Marfo et al. 2026 MDPI review: current framing of the field.
3. Saxena et al. 2017 (Mar. Pet. Geol.): core evidence on voxel size × threshold ×
   permeability.
4. Kirchhoff et al. 2024, Skeleton Recall (arXiv 2404.03010): the only topology loss
   practical at 3D rock patch sizes.
5. Gärttner, Alpak et al. 2023 (arXiv 2109.01818): max-flow as a connectivity descriptor.
6. Krygier et al. 2021 (Nat. Commun.): framing segmentation uncertainty propagation.
7. Robins et al. 2016 (WRR), "Percolating length scales from topological persistence".
8. Owusu-Ansah et al. 2026 (arXiv 2607.28327): the source method.

## I. What could NOT be verified

- **Abstracts or snippets only:** Leu et al. 2014; Saxena et al. 2017; Krygier 2021;
  Topological Filtering 2104.13430; Research Square rs-10932955; Phan et al. 2021;
  Sci. Rep. 2025 s41598-025-07211-2; PMC13402792; Alqahtani et al. 2022; clDice;
  arXiv 2607.28327.
- **Not accessed at all:** "A topological and manifold framework for porous media
  modeling" (ScienceDirect S3050724326000045); Springer s13202-026-02139-3; Wang et al.
  SPE Journal microfractures; the geometrical-based GAN; Andrä et al. 2013 parts I and II;
  the STACOM 2025 coronary benchmark; SAMamba3D; SAM-for-digital-rock; Imperial College
  repository pages; InterPore, SCA, EGU and AGU abstracts; Chinese-language journals.
- **MDPI review:** reference list only partly retrieved; not all 154 references checked.
- **Datasets:** licences, download sizes and weight availability not verified.
- **Search budget:** about 25 web searches. Q2's "open" status is an absence-of-evidence
  finding.

## Key source links

- Wang et al. 2021: https://arxiv.org/html/2002.05322v2
- Marfo et al. 2026 review: https://www.mdpi.com/3043-0100/1/2/6
- Sci. Rep. 2025 comparison: https://www.nature.com/articles/s41598-025-07211-2
- Phan et al. 2021: https://www.nature.com/articles/s41598-021-98697-z
- Gärttner/Alpak 2023: https://arxiv.org/pdf/2109.01818
- Topological Filtering: https://arxiv.org/pdf/2104.13430
- Robins et al. 2016: https://agupubs.onlinelibrary.wiley.com/doi/10.1002/2015WR017937
- Skeleton Recall: https://www.alphaxiv.org/zh/abs/2404.03010
- clDice: https://openaccess.thecvf.com/content/CVPR2021/papers/Shit_clDice_-_A_Novel_Topology-Preserving_Loss_Function_for_Tubular_Structure_CVPR_2021_paper.pdf
- Same Branches, Different Trees: https://arxiv.org/abs/2607.28327
- 11 Sandstones data descriptor: https://www.sciencedirect.com/science/article/pii/S2352340922001056
- IBM microCT dataset: https://github.com/IBM/microCT-Dataset and https://pmc.ncbi.nlm.nih.gov/articles/PMC10247717
- Alqahtani et al. 2022: https://link.springer.com/article/10.1007/s11242-022-01781-9
- Krygier et al. 2021: https://arxiv.org/pdf/2012.09913
