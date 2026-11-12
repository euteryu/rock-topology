# Phase 0 literature check: the listed papers

Written 12 Nov 2026 by an automated literature-check task. This supplements `docs/gate0-review.md`.
**Access levels:** *full text* = body text read; *abstract only* = abstract or metadata only;
*not accessed* = nothing beyond a title or citation record. Quotes are exact short phrases from
the source. Numbers are as the source reports them; none were computed in this repository.

Rock terms used below: *LBM* = lattice-Boltzmann flow solver; *PNM* = pore-network model;
*throat* = narrow neck between two pore bodies; *DRP-317* = Digital Rocks Portal project 317,
the "11 Sandstones" dataset (2.25 µm voxels), which is this project's primary dataset.

## HARD STOP CANDIDATE

**None found.** No opened paper trains a topology-aware loss on rock or porous-media micro-CT and
judges it by permeability or flow error (Q2). No opened paper applies controlled,
error-type-specific perturbations to rock masks and ranks segmentation metrics against
permeability error (the core perturbation question).

Closest items, none of which meets either criterion:
- **Leu et al. 2014.** Threshold sweeps, not error-type perturbations, and no metric ranking.
- **Hongsheng Wang et al. 2024 (SPE J.).** Finds pixel metrics and LBM permeability error
  disagree across 5 U-Nets. Uses BCE loss only, with no metric ranking.
- **Hayatdavoudi et al. 2025 (Sci. Rep.) and 2026 (JPEPT).** Use DRP-317 with BCE loss, and
  report LBM/PNM permeability and Euler number per architecture. No topology loss, no
  perturbations, no correlation analysis.
- **Acebes et al. 2026 (STACOM 2025).** Benchmarks topology-aware losses, but on coronaries
  only.

The search for this check was limited (see the end of this file). Q2 remains an
absence-of-evidence finding.

---

## 1. Leu et al. 2014, Transport in Porous Media

- **Citation:** Leu, L., Berg, S., Enzmann, F., Armstrong, R. T., Kersten, M. (2014). Fast X-ray
  micro-tomography of multiphase flow in Berea sandstone: a sensitivity study on image
  processing. *Transport in Porous Media* 105(2):451–469. doi:10.1007/s11242-014-0378-4.
  Open access.
- **URL opened:** https://link.springer.com/article/10.1007/s11242-014-0378-4 (via the Springer
  cookie redirect; first ~100k of 127k characters read, i.e. the body. The tail is references).
- **Access:** full text.
- **What it does:** Synchrotron fast micro-CT (TOMCAT) of a Berea core, 2.99 µm voxels. Threshold
  sensitivity is tested on a 750³ ROI. The maximum grey-value threshold is varied by ±1% of the
  mid value per step, giving 5 files from lowest to highest. Three segmentation methods are
  compared: global thresholding, watershed and hysteresis. Single-phase LBM permeability is
  computed with GeoDict (D3Q15, Darcy's law).
- **Verified numbers:**
  - Global threshold: permeability 600–1000 mD (about 28–32% variation), porosity 16–19%.
  - Watershed: permeability 680–780 mD (at most 8% variation), porosity 16–17%.
  - Hysteresis: permeability 520–730 mD (−16% to +19%).
  - Watershed-mid gives 722 mD against an experimental 700 mD. Porosity is 16.57% against an
    experimental 19.9%.
- **Verified quotes:** "Pore throats were found to be open for flow at large thresholds but closed
  for smaller thresholds". Porosity is "the least reliable quality criterion". In one example the
  flow field went from fully disconnected to fully connected between threshold files, and the
  throat was at least two voxels wider in the high-threshold file.
- **Q1:** This is direct evidence that a few-voxel change at throats moves permeability far more
  than porosity. The study is threshold-driven: it perturbs everything at once, not throats
  versus bodies, and computes no Dice, Betti or Euler metrics. This supports the porosity-confound
  framing and the throat-only perturbation arm.
- **Q2:** none. **Q3:** one sample and one resolution only.
- **Corrections to the brief:** The gate review called Leu "threshold and seed changes". The
  paper varies thresholds, and for watershed and hysteresis the seed thresholds, so the wording is
  acceptable. The voxel size is 2.99 µm (rounded to 3 µm in the abstract).

## 2. Saxena et al. 2017, Marine and Petroleum Geology 86:972

- **Citation (Crossref):** Saxena, N., Hofmann, R., Alpak, F. O., Dietderich, J., Hunter, S.,
  Day-Stirrat, R. J. (2017). Effect of image segmentation & voxel size on micro-CT computed
  effective transport & elastic properties. *Mar. Pet. Geol.* 86:972–990.
  doi:10.1016/j.marpetgeo.2017.07.004.
- **URLs tried:** ScienceDirect (HTTP 403), Semantic Scholar API (abstract elided by the
  publisher), OpenAlex (closed access, no abstract), web search for author copies (none found).
- **Access:** not accessed. Only the citation metadata was seen. **Not even the abstract.**
- **Unverified claims in the brief:** "five sandstones", "2, 4 and 8 µm", the uncertainty from
  threshold choice increasing with coarser voxels, and the quote "rounding and smoothing of pore
  throats ... increased the computed permeability". All of these come from secondary
  descriptions. A search for the exact phrase found nothing. **CLAUDE.md Phase 1 says it mirrors
  "the 2, 4 and 8 µm of Saxena et al. 2017". Do not cite these numbers until the owner fetches the
  paper.**
- **Correction:** The 2026 MDPI review does NOT cite this paper. Its only Saxena 2017 reference
  (ref. 125) is a different paper: Saxena et al. 2017, *Computers & Geosciences*, "Estimating
  permeability from thin sections without reconstruction", doi:10.1016/j.cageo.2017.02.014.
- **Owner action:** fetch the PDF through an institution or ask the authors (Shell).

## 3. Saxena et al. 2018, Advances in Water Resources ("operating envelope")

- **Citation:** Saxena, N., Hows, A., Hofmann, R., Alpak, F. O., Freeman, J., Hunter, S.,
  Appel, M. (2018). Imaging and computational considerations for image computed permeability:
  operating envelope of Digital Rock Physics. *Adv. Water Resour.* 116:127–144.
  doi:10.1016/j.advwatres.2018.04.001.
- **URL opened:** Semantic Scholar API record (abstract present). ScienceDirect itself was not
  accessible.
- **Access:** abstract only.
- **Verified quotes from the abstract:**
  - "We find that at least 10 voxels are needed to sufficiently resolve pore throats for single
    phase fluid flow simulations."
  - "If this ratio is greater than 5, the coefficient of variation for single-phase permeability
    simulations drops below 15%." Here the ratio is field of view to effective grain size.
  - "If this condition is not met, additional analyses and corrections may allow for meaningful
    comparisons."
- **Q3:** This gives a concrete, citable resolution criterion: about 10 voxels across a throat.
  Phase 1 should report voxel size relative to throat radius against this threshold. At 2.25 µm,
  and after 2× and 4× downsampling, many DRP-317 throats will fall below 10 voxels. That is
  exactly the regime the project means to test. The FOV/grain ratio > 5 gives a sub-volume size
  check (REV) for the 256³ and 400³ crops.
- **Correction:** The gate review listed this as "title only". The abstract has now been verified.

## 4. Topological filtering for 3D microstructure segmentation (arXiv 2104.13430)

- **Citation:** Patel, A. V., Hou, T., Beltran Rodriguez, J. D., Dey, T. K., Birnie, D. P. III
  (2022). Topological filtering for 3D microstructure segmentation. *Computational Materials
  Science* 202:110920. doi:10.1016/j.commatsci.2021.110920. arXiv:2104.13430.
- **URL opened:** https://ar5iv.labs.arxiv.org/html/2104.13430 (full HTML). The journal venue
  comes from Crossref.
- **Access:** full text.
- **What it does:** PerSplat is a persistence-based grey-scale filter applied BEFORE thresholding.
  It "splats" small low-persistence sublevel-set components and comes in per-slice (P) and
  volume (V) variants. Materials are a sugar-templated porous PDMS polymer and a commercial
  Li-ion graphite electrode. The synthetic test images are Otsu-binarised real XCT with added
  Gaussian, Poisson and averaging noise. It is compared with TV and NL-means filtering.
- **Verified numbers (Synth1):** ground-truth tortuosity 1.736. Tortuosity error: PerSplat-P
  +0.065, TV −0.144, no filter +0.274. Pixel accuracy: PerSplat-P 95.95%, TV 93.70%, no filter
  90.45%.
- **Q1/Q2/Q3:** not a loss, no deep learning, no permeability. It is a topology-aware
  pre-processing baseline at most.
- **Correction:** The gate review said "synthetic microstructures". The synthetics are derived
  from real polymer and electrode scans, not rock. A journal version exists (Comput. Mater. Sci.
  2022); cite that.

## 5. Enninful 2026, Research Square rs-10932955

- **Citation (Crossref):** Enninful, H. R. N. B. (Leipzig University) (2026, posted 28 Sep).
  Topology-aware AI for porous materials: from structural representation to counterfactual
  testing and inverse design. Research Square preprint. doi:10.21203/rs.3.rs-10932955/v1.
- **URLs opened:** https://www.researchsquare.com/article/rs-10932955 (JavaScript-rendered, title
  only) and the Crossref record (full abstract).
- **Access:** abstract only.
- **Verified:** It is a Perspective. It proposes "counterfactual topology twins—descriptor-matched
  structures with deliberately different networks" "as a unifying stress test". It surveys
  "adsorption-derived descriptors and pore-network models", persistent topology, geometric
  learning and "digital twins and multimodal structural inference". The abstract does not contain
  the words segmentation, imaging, tomography or permeability.
- **Q1:** This is the conceptual counterpart of the Phase 3 factorial design: same porosity,
  different connectivity. Cite it as the conceptual framing. It is not an empirical competitor.
- **Correction:** The gate review said it targets "MOFs, adsorbents". The abstract names no
  specific material class; only "adsorption-derived descriptors" appears.

## 6. Omrani & Omrani 2026, "A topological and manifold framework for porous media modeling" (ScienceDirect S3050724326000045)

- **Citation (Crossref):** Omrani, H., Omrani, H. (2026). A topological and manifold framework for
  porous media modeling: a review of engineering applications and mathematics. *Next Chemical
  Engineering* 2:100023. doi:10.1016/j.nxcen.2026.100023. CC BY-NC 4.0 (open access), 108
  references.
- **URLs:** ScienceDirect returned HTTP 403. The abstract was reconstructed from OpenAlex.
- **Access:** abstract only. The paper is open access, but the publisher blocked the fetch.
- **Verified (abstract):** A review/perspective on "Euler characteristics, Betti numbers,
  Minkowski functionals, Hadwiger's theorem, and manifold analysis". It claims topological
  invariants "can explain percolation thresholds, ganglion dynamics" and "integrates algebraic
  topology with digital rock physics". No segmentation, no losses, no experiments.
- **Q1:** Background citation for using Euler and Betti numbers as metrics. Not a competitor.

## 7. Hayatdavoudi et al. 2026, J. Petrol. Explor. Prod. Technol. (s13202-026-02139-3)

- **Citation:** Hayatdavoudi, M., Emami Niri, M., Kalhor, A. (2026). Designing a dilated
  multi-scale attention convolutional neural network to optimize rock micro computed tomography
  image segmentation. *J. Petrol. Explor. Prod. Technol.* 16:36. doi:10.1007/s13202-026-02139-3.
  Open access.
- **URL opened:** https://link.springer.com/article/10.1007/s13202-026-02139-3 (cookie redirect,
  full HTML).
- **Access:** full text.
- **What it does:** Proposes ARSNet, a 2D CNN with a dilated ResNet50 encoder and ASPP, FPA, SPP,
  SE and GAU modules. Trained on 5000 2D slices from 10 DRP-317 sandstones at 2.25 µm. The blind
  test is Buff Berea (1000×512×512). The **loss is binary cross-entropy**. Metrics are pixel
  metrics (F1, IoU), porosity, Euler number (scikit-image) and LBM permeability (MPLBM-UT).
- **Verified:** PSPNet gives low permeability, which the authors attribute to disconnected pore
  space. Its Euler error is about 75%. ARSNet's permeability match is "consistent with its
  highest F1-score". No formal metric-to-permeability analysis.
- **Internal inconsistencies noted by the reader:** The abstract gives test F1 99.3% and blind IoU
  99.0%, while the results text gives a test-set IoU of 96.7 and a blind-sample F1 of 99.5. The
  paper says it trains on "raw" data but also describes NLM filtering and IsoData thresholding.
- **Q1/Q2/Q3:** Same group and dataset as item 18a. It shows that DRP-317 + 2D CNN + LBM is a
  live line of work with no topology loss. Relevant for Phase 1: these authors treat the DRP-317
  segmentation as IsoData-based.

## 8. "Wang et al., SPE Journal, microfracture segmentation"

- **Finding:** I found no SPE Journal paper on microfracture segmentation by Ying Da Wang or the
  Mostaghimi group. The Mostaghimi-group SPE item is a conference paper:
  Ar Rushood et al. 2020, "Segmentation of X-ray images of rocks using deep learning",
  SPE-201282-MS (seen in the MDPI review's reference list, ref. 71; not opened). The SPE Journal
  microfracture paper is by a different Wang:
- **Citation:** Wang, Hongsheng, Guo, R., Dalton, L. E., Crandall, D., Hosseini, S. A., Fan, M.,
  Chen, C. (2024). Comparative assessment of U-Net-based deep learning models for segmenting
  microfractures and pore spaces in digital rocks. *SPE Journal* 29(11):5779–5791.
  doi:10.2118/215117-PA.
- **URL opened:** https://www.osti.gov/servlets/purl/2478352 (DOE accepted manuscript PDF, text
  extracted) and the ORNL record.
- **Access:** full text (accepted manuscript).
- **What it does:** 2.5D U-Net, attention U-Net, residual U-Net, U-Net++ and residual U-Net++,
  segmenting solid, pore and fracture networks (DFNs). Benchmark images are SYNTHESISED from
  labels by adding partial-volume blur, noise and ring artifacts (sandstone and artificial rocks).
  The loss is BCE: "the binary cross-entropy (BCE) loss function was utilized". 12 test volumes
  are scored with LBM permeability (ground truth 0.23–3.68 D).
- **Verified numbers:** permeability ARE (absolute relative error) U-Net 0.193, residual U-Net
  0.108, attention U-Net 0.090, U-Net++ 0.067, residual U-Net++ 0.059.
- **Verified quote:** "the higher pixel-wise metrics do not necessarily correlate with better
  performance in physics-based metrics". Residual U-Net had higher pixel accuracy than attention
  U-Net but larger permeability error, "indicating that the misclassification of residual U-Net
  happened on the critical flow paths". The authors suggest focal or Dice loss as future work; no
  topology losses.
- **Q1:** This is a second rock example of pixel metrics disagreeing with permeability error,
  alongside Wang et al. 2021. It is anecdotal (5 models, no correlation analysis). Its
  label-to-synthetic-greyscale benchmark design resembles this project's degradation design;
  cite it there.
- **Correction:** The brief's attribution to "Ying Da Wang / Mostaghimi group" is wrong. The
  paper is by Hongsheng Wang (UT Austin BEG) and Cheng Chen (Stevens). It is about fractures plus
  pores, not microfractures alone.

## 9. Andrä et al. 2013, Digital rock physics benchmarks, parts I and II

- **Citations (Crossref):** Andrä, H., Combaret, N., Dvorkin, J., Glatt, E., Han, J., Kabel, M.,
  Keehm, Y., Krzikalla, F., Lee, M., Madonna, C., Marsh, M., Mukerji, T., Saenger, E. H., Sain, R.,
  Saxena, N., Ricker, S., Wiegmann, A., Zhan, X. (2013).
  - Part I: Imaging and segmentation. *Computers & Geosciences* 50:25–32.
    doi:10.1016/j.cageo.2012.09.005.
  - Part II: Computing effective properties. *Computers & Geosciences* 50:33–43.
    doi:10.1016/j.cageo.2012.09.008.
- **URLs tried:** ScienceDirect (blocked), Semantic Scholar (abstract elided, and it mislabels the
  venue as "Computational Geosciences"), the ETH Research Collection (HTTP 500) and Fraunhofer
  Publica (connection refused).
- **Access to the papers:** not accessed. Abstract seen only as a search snippet.
- **What WAS opened:** the benchmark's official supplementary repository,
  https://github.com/fkrzikalla/drp-benchmarks. I parsed `results/simulations.xls`, which has
  Overview and Details sheets. These numbers come from the repository spreadsheet, NOT from the
  published tables. Check them against Part II before citing.
  - Samples: Fontainebleau 288×288×300 at 7.5 µm; Berea 1024³ at 0.74 µm; Grosmont carbonate 1024³
    at 2.02 µm; sphere pack 788×791×793 at 7.0 µm.
  - Porosity from segmentation by different groups: Berea 0.184–0.209, carbonate 0.195–0.271.
  - Permeability in mD, Overview sheet, EJ-Stokes (Fraunhofer) vs LBM (Kongju):
    - Fontainebleau: 1914 vs 1503 (±12%).
    - Berea 400³: 123.6 vs 113.4 (±4%).
    - Berea large: 138.9 vs 108.8 (±12%).
    - Carbonate 400³: 511.7 vs 353.5 (±18%).
    - Carbonate large: 1705.7 vs 772.9 (±38%).
    - Spheres: 270220 vs 221587.
    - "±" is the sheet's R/M, i.e. half-range over midrange.
  - **Caveats:**
    - The Berea 400³ and carbonate 400³ Overview entries equal the x-direction values in the
      Details sheet. The directional mean for Fraunhofer Berea 400³ is 105.6 mD.
    - The Overview sphere-pack EJ value (270220) is 10× the Details value for the same run
      (mean 27022). This looks like a typo in one of the two sheets.
    - Directional Berea permeabilities from Details range from about 68 to 161 mD across groups
      and segmentations.
- **Gate 2 relevance:** "within the range reported in the literature" can use these
  between-solver spreads, roughly ±4–38% depending on sample and domain size, once checked
  against Part II.
- **Correction:** The MDPI review's Crossref deposit lists refs 7 and 8 with first author
  "Combaret". The first author is Andrä.

## 10. STACOM 2025 coronary topology benchmark

- **Citation:** Acebes, C., Galdran, A., Moustafa, A. H., Clapers, M., Camara, O. (2026). A
  clinically-informed benchmark for topology-aware coronary artery segmentation. In *Statistical
  Atlases and Computational Models of the Heart (STACOM 2025)*, LNCS 16459, pp. 13–22. Springer.
  doi:10.1007/978-3-032-17734-6_2.
- **URL opened:** https://dsp.tecnalia.com/items/79a8afff-2afc-4c4e-8143-eba7e8c01da8 (repository
  record with abstract). No PDF.
- **Access:** abstract only.
- **Verified (abstract):** Benchmarks multiple topology-aware methods against a
  non-topology-aware baseline on ASOCA, with an expert-informed split into primary, secondary and
  tertiary segments. Topology-aware methods perform similarly on primary segments ("limited
  benefits"). Differences on secondary and tertiary segments are driven more by "annotation
  inconsistencies" and "dataset biases" than by the method.
- **Q2:** This is a useful prior for a null result. Even in tubular trees, topology losses add
  little where the structure is thick and well annotated. The finding that label noise outweighs
  the loss also matters for threshold-based rock labels.
- **Note:** arXiv 2607.28327 does NOT cite this benchmark. It cites TopCoW and CorSegRec.

## 11. Robins et al. 2016, WRR

- **Citation:** Robins, V., Saadatfar, M., Delgado-Friedrichs, O., Sheppard, A. P. (2016).
  Percolating length scales from topological persistence analysis of micro-CT images of porous
  materials. *Water Resour. Res.* 52(1):315–329. doi:10.1002/2015WR017937.
- **URLs:** Wiley returned 403. The ANU Open Research PDF
  (openresearch-repository.anu.edu.au/.../1c37461f-...) failed twice with ECONNRESET. The ANU
  research portal record (abstract) was opened.
- **Access:** abstract only.
- **Verified (abstract):** "We demonstrate how persistence information can be used to estimate
  the percolating sphere radius". Data are bead packs, sand, sandstones and a limestone.
- **Q3:** This supports using persistence and the critical radius as a percolation-proximity
  descriptor. **Owner action:** retry the ANU PDF in a browser; it is open.

## 12. Gärttner, Alpak et al. 2023 (arXiv 2109.01818)

- **Citation:** Gärttner, S., Alpak, F. O., Meier, A., Ray, N., Frank, F. (2023). Estimating
  permeability of 3D micro-CT images by physics-informed CNNs based on DNS. *Computational
  Geosciences* 27(2):245–262. doi:10.1007/s10596-022-10184-0. CC BY 4.0. A correction appears at
  27:263. arXiv:2109.01818.
- **URL opened:** https://ar5iv.labs.arxiv.org/html/2109.01818 (first 100k of 109k characters).
  The venue comes from Crossref.
- **Access:** full text.
- **Verified:**
  - Training data: Bentheimer, a 1000³ binary image at 2.25 µm, cut into 100³ subsamples, which
    the authors note are below REV. Validation: Berea and Castlegate. The reference list cites the
    11 Sandstones dataset (DRP-317).
  - Max-flow: every voxel is a graph node, face neighbours are unit-capacity edges, and source and
    sink nodes are attached to the inflow and outflow faces. By min-cut/max-flow, f_max equals the
    minimum number of edges whose removal disconnects inflow from outflow.
  - Fit: k ~ f_max^1.407, log R² = 0.869.
  - CNN with max-flow input, log R²: Bentheimer validation 93.22%, Berea 94.13%, Castlegate
    94.51%. Without physics input: 77.97% (Bentheimer validation).
  - "errors arising from imaging are neglected": segmentation is taken as ground truth.
- **Q1:** Max-flow is a cheap, global, throat-sensitive connectivity metric with known
  correlation to permeability on the same dataset family. Include it, as already planned
  (exploratory tier). The fact that it counts bottleneck faces suggests it may beat Betti and
  Euler. **Q2:** a permeability predictor, not segmentation.
- **Correction:** The first author is Gärttner. The MDPI review's Crossref deposit lists ref. 152
  under "Alpak", so cite it as "Gärttner et al.".

## 13. Krygier et al. 2021 (arXiv 2012.09913)

- **Citation:** Krygier, M. C., LaBonte, T., Martinez, C., Norris, C., Sharma, K., Collins, L. N.,
  Mukherjee, P. P., Roberts, S. A. (2021). Quantifying the unknown impact of segmentation
  uncertainty on image-based simulations. *Nature Communications* 12:5414.
  doi:10.1038/s41467-021-25493-8.
- **URL opened:** https://arxiv.org/pdf/2012.09913 (PDF saved by the fetch tool, text extracted
  locally).
- **Access:** full text.
- **Verified:** The EQUIPS workflow uses a Bayesian CNN (or MC-dropout for the torso) to produce
  probability maps, then samples segmentations and propagates them through physics. There are
  three exemplars:
  - Woven composite: fabric volume fraction, thermal conductivity and Stokes permeability.
  - Graphite electrodes E1 and E2: electrical conductivity and tortuosity.
  - Human torso: spine and aorta.
  - Permeability "is better approximated by a beta distribution". Tails are non-Normal, so
    bounding segmentation uncertainty "can fail".
  - No rock, and no ranking of Dice or other metrics against physics error.
- **Q1:** This is the framing for propagating segmentation uncertainty to permeability, and it
  says the permeability-error distribution can be skewed. That supports using rank and log-ratio
  statistics.

## 14. Skeleton Recall (arXiv 2404.03010)

- **Citation:** Kirchhoff, Y., Rokuss, M. R., Roy, S., Kovacs, B., Ulrich, C., Wald, T., Zenk,
  M., Vollmuth, P., Kleesiek, J., Isensee, F., Maier-Hein, K. (2024). Skeleton Recall Loss for
  connectivity conserving and resource efficient segmentation of thin tubular structures. ECCV
  2024. arXiv:2404.03010.
- **URL opened:** https://arxiv.org/html/2404.03010v2.
- **Access:** full text.
- **Verified quotes, Sec. 5.3, averaged over datasets and excluding multi-class TopCoW, relative
  to plain nnU-Net:**
  - clDice: "approximately 88% additional training time and 52% more VRAM consumption".
  - Skeleton Recall: "only an additional 8% training time and 2% higher VRAM consumption".
- **Datasets:** Roads, DRIVE and concrete Cracks (2D); ToothFairy and TopCoW (3D). No porous
  media, no flow evaluation. Metrics are Dice, clDice and Betti errors.
- **Check of the brief:** The CLAUDE.md numbers (8%/2% vs 88%/52%) are CORRECT. Both are
  overheads relative to the nnU-Net baseline, not a direct SR-vs-clDice ratio.

## 15. clDice (arXiv 2003.07311)

- **Citation:** Shit, S., Paetzold, J. C., Sekuboyina, A., Ezhov, I., Unger, A., Zhylka, A.,
  Pluim, J. P. W., Bauer, U., Menze, B. H. (2021). clDice: a novel topology-preserving loss
  function for tubular structure segmentation. CVPR 2021. doi:10.1109/CVPR46437.2021.01629.
- **URL opened:** https://ar5iv.labs.arxiv.org/html/2003.07311.
- **Access:** full text.
- **Verified:**
  - Corollary 1.1: if each mask's foreground skeleton lies within the other's foreground, the
    foregrounds and backgrounds are homotopy equivalent. It assumes masks "admitting foreground
    and background skeleta". The proof is for hard clDice, not soft-clDice.
  - Scope: "locally a tubular structure and 2) globally forms a network".
  - Soft-skeleton iterations k must be at least the maximum radius: "a too low k leads to
    incomplete skeletonization". They used k = 5–25.
  - Datasets: DRIVE, Roads, CREMI (2D); synthetic vessels, Vessap (3D).
- **Q2:** For rock, k must cover the largest pore-body radius in voxels, which raises cost. The
  tubularity assumption is explicit in the paper, which supports the gate review's "tubularity
  breaks" caveat.

## 16. Owusu-Ansah et al. 2026, "Same Branches, Different Trees" (arXiv 2607.28327)

- **Citation:** Owusu-Ansah, M., Lee, K., Venugopal, V., Jawaid, M. M., Duan, W., Brown, J.
  (2026). Same branches, different trees: a bifurcation connectedness metric for coronary artery
  segmentation and FFR-CT decision agreement. arXiv:2607.28327 (30 Jul 2026), accepted at STACOM
  2026.
- **URL opened:** https://arxiv.org/html/2607.28327v1.
- **Access:** full text.
- **Data:** ImageCAS (1000 CCTA volumes, 750 train / 250 test), ASOCA (N = 20) as an
  out-of-distribution calibre test, and an FFR-CT analysis on the 250 test cases.
- **Metrics:** BCS (bifurcation connectedness), soft-BCS, BCR, BER, β0, Dice, clDice, HD95.
- **Analysis methods (verified; this is the template for Phase 3):**
  1. **Independence from other metrics:** "regress rank-BCS on Dice, clDice, HD95, and β0". The
     paper reports 1 − R² and partial rank correlations (R² = 0.21; all partials < 0.30). The
     rank-correlation type (Spearman or Kendall) is NOT stated.
  2. **Joint model:** a "patient-clustered GEE (N=250)" with six metrics entered together (BCS,
     Dice, clDice, HD95, β0, BER), giving odds ratios per SD for FFR decision error. BCS OR 0.81
     per SD (p = 0.002); Dice OR 0.81 (p = 0.12). The link function is not stated, but odds
     ratios imply logistic.
  3. **Bootstrap:** "patient-clustered bootstrap confidence intervals (B=2,000, resampled by
     case)", explicitly preferred over row-level p-values. Wilson 95% CIs are used for
     proportions.
  4. **Training comparisons:** Wilcoxon signed-rank for continuous metrics and McNemar for
     decisions, with Holm correction and paired d_z effect sizes.
  5. **Perturbation check:** breaks vs connectedness-preserving narrowing. BCS separates them
     about 20×, against ≤5× for Dice, clDice and HD95. Narrowing leaves BCS essentially
     unchanged (|ΔBCS| = 0.004). Perturbation magnitudes and generation are not described in
     detail.
- **Training finding:** 3 backbones × 3 seeds, all topology losses at α = 0.05, with Dice within
  0.011 of baseline. Skeleton Recall and soft-BCS raise FFR-CT consistency by about 10 pp, and
  **clDice does not**. Skeleton Recall leaves more components (Δβ0 = +2.94).
- **Implications for this project:**
  - The brief's description (rank correlations, joint regression, bootstrap by sample) matches.
  - Make the rock version explicit on three points: (a) state Spearman; (b) because permeability
    error is continuous, the joint model is a linear model or GEE on |log10 k ratio| clustered by
    rock sample, not logistic; (c) bootstrap resampled by rock sample, B = 2000.
  - Note the paper's own caveat: it measures "geometric, not clinical, fidelity" because both
    decisions use the same solver. The rock analogue is simulated, not lab, permeability.
  - The paper's breaks-vs-narrowing perturbation is exactly the Phase 3 factorial design. Its
    coronary result (connectedness matters, calibre does not move BCS) is what the rock study
    tests in looped networks.

## 17. Marfo et al. 2026, MDPI review: full reference list

- **Citation:** Marfo, W. A., Ampomah, W., Rahnema, H., Oliva, C. R., Akpabli, G., Duartey, K. O.,
  Appiah, E. A., Agyei, S., Adjimah, J. M. (2026). Digital rock segmentation with uncertainty
  quantification for geological CO2 storage: from image accuracy to carbon storage reliability.
  *Advances in Carbon Neutrality* 1(2):6. doi:10.3390/acn1020006. 154 references.
- **URLs:** mdpi.com and preprints.org both returned HTTP 403. **The complete 154-entry reference
  list was read from the Crossref deposit** (https://api.crossref.org/works/10.3390/acn1020006).
  The main text was NOT re-read in this pass. The gate review read it.
- **Access:** reference list complete (Crossref); body text not re-accessed.
- **Screening result:** **No entry trains a topology-aware loss (clDice, Skeleton Recall, Betti
  or persistent-homology, Euler) for rock or porous media. No entry ranks segmentation metrics
  against permeability error.** No clDice, Skeleton Recall, Betti-matching or TopoLoss paper is
  cited at all. Entries flagged as nearest, by title or metadata only unless stated:
  - 58 Purswani et al. 2020, *J. Pet. Sci. Eng.* 195:107890, "Evaluation of image segmentation
    techniques for rock property estimation": segmentation choice vs properties. Not opened.
    Worth reading for Q1.
  - 59 Andrew 2018, *Comput. Geosci.* 22, "quantified study of segmentation on synthetic XRM and
    FIB-SEM": synthetic ground-truth segmentation study. Not opened.
  - 69 Niu et al. 2020, *WRR* 56, CNN segmentation with reduced user bias. Not opened.
  - 71 Ar Rushood et al. 2020, SPE-201282-MS, Mostaghimi group. Not opened.
  - 83 Mahmoudi et al. 2025, *Comput. Geosci.* 196:105853, pixel-level class weighting. Abstract
    not available on OpenAlex; the title suggests weighted CE, not topology.
  - 90 Sun et al. 2026, *Int. J. Coal Geol.* 315:104951, Swin-UNETR 3D pore segmentation.
    Keyword "pore connectivity"; loss and flow evaluation unknown. **Owner should check.**
  - 103 Nande 2024, *SPE J.*, carbonate segmentation. Not opened.
  - 110 Leu 2014: item 1 above.
  - 125 Saxena 2017, *Comput. Geosci.* (thin sections), NOT the Mar. Pet. Geol. paper.
  - 127 Krygier 2021: item 13 above.
  - 133 Zhao et al. 2020, *PRE* 102:023308, uncertainty quantification for permeability through
    image analysis. Not opened. Worth reading for Q1.
  - 134 Berg et al. 2018, *Leading Edge*, ground-truth images for validating micro-CT pipelines.
    Not opened. Relevant to the perturbation design.
  - 148 Wang, F. & Zai, Y. 2023, *Adv. Water Resour.* 172:104384, "Image segmentation and flow
    prediction of digital rock with U-net". From search snippets: U-Net segmentation plus a
    regression U-Net for flow. No topology loss indicated. Abstract not obtainable.
  - 152 Gärttner/Alpak 2023: item 12 above.
- **Observations:**
  - The review does NOT cite Wang, Shabaninejad, Armstrong & Mostaghimi 2021 (Applied Soft
    Computing), the brief's origin paper.
  - Refs 7 and 8 (Andrä 2013) are deposited under first author "Combaret".
  - The gate review's statement that ref. 138 is Bayesian QuickNAT and ref. 152 is Gärttner is
    confirmed.

## 18a. Hayatdavoudi et al. 2025, Scientific Reports (s41598-025-07211-2)

- **Citation:** Hayatdavoudi, M., Emami Niri, M., Kalhor, A. (2025). Comparative analysis of
  sandstone microtomographic image segmentation using advanced convolutional neural networks
  with pixelwise and physical accuracy evaluation. *Sci. Rep.* 15:22164.
  doi:10.1038/s41598-025-07211-2. PMC12218276.
- **URL opened:** Europe PMC full-text XML,
  https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12218276/fullTextXML (both halves read).
- **Access:** full text.
- **Verified:**
  - Data: 10 DRP-317 sandstones at 2.25 µm. The blind sample is Buff Berea, 1000×512×512, with
    ground-truth porosity 22.1%.
  - Methods: 12 2D CNNs (VGG16-Unet, EfficientNetB0-Unet, ENet, ..., PSPN, PAN) and Otsu.
    **BCE loss.**
  - Blind-sample results: VGG16-Unet IoU 99.5% and F1 99.7%; PSPN IoU 93.4% with porosity
    20.4%.
  - Permeability by LBM (MPLBM-UT), PNM and CFD (PerGeos), plus formation factor. Results are
    reported in figures; no numeric values appear in the text read.
  - PNM "tends to give lower predicted permeability values", attributed to "loss of connectivity
    in the pore space during the segmentation and prediction process".
  - The authors say high pixel accuracy "does not guarantee accurate physical metrics". Euler
    number is mentioned only in the introduction. No correlation analysis.
- **Q1:** Shows that sub-1% pixel differences between near-perfect CNNs still reorder permeability
  rankings. Same data as this project.
- **Correction:** Authors are Hayatdavoudi, Emami Niri and Kalhor (the gate review gave no
  authors). Euler number is not computed here; it is computed in their 2026 JPEPT paper (item 7).

## 18b. Phan, Ruspini & Lindseth 2021, Scientific Reports (s41598-021-98697-z)

- **Citation:** Phan, J., Ruspini, L. C., Lindseth, F. (2021). Automatic segmentation tool for 3D
  digital rocks by deep learning. *Sci. Rep.* 11:19123. doi:10.1038/s41598-021-98697-z.
  PMC8476575.
- **URLs opened:** https://pmc.ncbi.nlm.nih.gov/articles/PMC8476575/ and the Europe PMC full-text
  XML (first 100k of 106k characters).
- **Access:** full text, except the last ~6k characters (likely data availability and
  references).
- **Verified:**
  - Data: 10 micro-CT images, about 1.9–17 µm (e.g. Bentheimer 1024³ at 1.94 µm). Labels are a
    consensus from several tools (Avizo, PerGeos, ImageJ, Mango).
  - Network: SE-ResNeXt-50 U-Net on 2D slice stacks, 3 phases (pore, micro-phase, solid). The
    loss was not found in the text read.
  - Metrics: voxel accuracy, per-phase IoU, phase fractions, Euler number and 26-connected
    component counts. Euler on the clean synthetic (solid / solid+micro): ground truth −1688 /
    −251, model −1383 / −332.
  - Permeability by PNM, units not given in the table: Bentheimer model 2319 vs five expert users
    1069–2294; Berea 795 vs 394–841.
  - The tool is "available under the SmartRocks project"; no public weights were found.
- **Q1:** Shows inter-operator segmentation spread produces about a 2× permeability spread
  (Bentheimer), a useful scale reference for "how big is a meaningful permeability error". No
  topology loss.

---

## Corrections to CLAUDE.md and docs/gate0-review.md (summary)

1. **Saxena 2017 (Mar. Pet. Geol.)** was not accessible even as an abstract. "Five sandstones",
   "2/4/8 µm" and the "rounding and smoothing of pore throats" quote are unverified. The MDPI
   review cites a different Saxena 2017 (Comput. Geosci., thin sections).
2. **"Wang et al., SPE Journal, microfractures (Ying Da Wang / Mostaghimi)"** is a misattribution.
   The SPE J. 2024 paper is by Hongsheng Wang, ..., Cheng Chen (doi:10.2118/215117-PA).
3. **Skeleton Recall overheads** (8%/2% vs 88%/52%) are verified. Both are relative to nnU-Net.
4. **Topological Filtering** is published in Comput. Mater. Sci. 202:110920 (2022). Its data are
   polymer and battery-electrode, not rock.
5. **Enninful** (Leipzig) Perspective: the abstract names no material class (no MOFs).
6. **Gärttner** is the first author of ref. 152, not Alpak. **Andrä** is the first author of
   refs 7 and 8, not Combaret.
7. **Sci. Rep. 2025** is by Hayatdavoudi, Emami Niri & Kalhor. The same group wrote the Springer
   JPEPT 2026 paper (item 7). Both use DRP-317 and BCE loss.
8. **Saxena 2018** is now verified at abstract level: the "≥ 10 voxels per throat" criterion.
9. **STACOM 2025 benchmark** identified: Acebes et al., LNCS 16459:13–22.
10. **arXiv 2607.28327:** the rank-correlation type is unstated, and the joint model is a
    patient-clustered GEE on a binary outcome. The Phase 3 adaptation needs a continuous-outcome
    model.
11. The MDPI review does not cite Wang et al. 2021 (Applied Soft Computing).

## Inaccessible; the owner may fetch manually

- Saxena et al. 2017, Mar. Pet. Geol. (paywalled): **priority**.
- Saxena et al. 2018, AWR, full text (paywalled; abstract seen).
- Andrä et al. 2013 parts I and II (paywalled). The supplementary spreadsheet was used instead.
- Robins et al. 2016: open PDF on ANU Open Research; the fetch failed and may work in a browser.
- Omrani & Omrani 2026, Next Chem. Eng.: open access, but ScienceDirect blocked the fetch.
- Acebes et al. 2026, STACOM 2025 chapter (Springer).
- Marfo et al. 2026, body text and the preprints.org version (both 403 in this pass).
- Not opened but flagged from the review list: Purswani 2020, Zhao 2020 (PRE), Berg 2018
  (Leading Edge), Sun 2026 (Swin-UNETR), Wang & Zai 2023 (AWR).

Search budget for this pass: about 15 web searches plus about 50 page fetches. InterPore, SCA and
Chinese-language sources were not searched in this pass.
