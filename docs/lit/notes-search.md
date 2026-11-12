# Fresh prior-work search (Phase 0, second pass)

Run 12 November 2026 by an automated search agent. Scope: find what `docs/gate0-review.md`
missed for Q1 (which metric predicts permeability error), Q2 (topology-aware losses judged by
permeability at matched Dice) and Q3 (dependence on resolution and porosity). Papers on the
CLAUDE.md Phase 0 list were left to another agent and not re-checked here.

**HARD STOP CHECK: no hard-stop candidate found.** Nothing found trains a topology-aware loss
(soft-clDice, Skeleton Recall, persistent-homology/Betti, Euler, connectivity) on rock or
porous micro-CT and scores it by permeability or flow error. Nothing found applies controlled,
error-type-specific perturbations to rock masks and ranks metrics against permeability error.
Two items need a full-text check before Gate 0 because their abstracts are close (see the
threat notes): Eshimiakhe et al. 2026 (IEEE TGRS) and Fernandes et al. 2024 (Sci. Rep.).

Rock terms used below: *pore* = void, *grain* = solid, *throat* = narrow neck between two pore
bodies, *permeability* = how easily fluid flows through the rock, *LBM* = lattice-Boltzmann
voxel flow solver, *PNM* = pore-network model, *percolation* = the pore space forming a
sample-spanning connected path, *REV* = representative elementary volume, *micro-porosity* =
pores smaller than a voxel.

Access levels: **FULL** = full text read; **ABSTRACT** = abstract page or full abstract
(publisher, OpenAlex, Semantic Scholar or arXiv); **SNIPPET** = only search-engine snippets
plus a metadata record (stated where it applies).

---

## 1. Query log

"Hits" = new relevant items found by that query that were then opened and are reported in
section 2 (items already known from `docs/gate0-review.md` or the CLAUDE.md list are not
counted). Venue = where the query was run. "Web" = general web search engine.

### 1a. Web searches (rows 1-59) and direct full-text reads (rows 60-63)

| # | Query | Venue | Hits |
|---|---|---|---|
| 1 | topology-aware loss segmentation rock micro-CT permeability | Web | 0 |
| 2 | clDice porous media segmentation permeability | Web | 0 |
| 3 | "skeleton recall" loss porous media OR rock OR soil micro-CT | Web | 0 |
| 4 | persistent homology loss segmentation micro-CT porous connectivity | Web | 0 |
| 5 | physics-informed segmentation digital rock permeability loss function | Web | 0 (Li/Aslam/Yan SPE J 2025 seen, not opened) |
| 6 | Dagdelen 2026 training segmentation porous media topology NJIT | Web / InterPore | 1 |
| 7 | segmentation error sensitivity permeability erosion dilation micro-CT sandstone threshold sweep | Web / SCA / EGU | 1 |
| 8 | "segmentation uncertainty" permeability propagation micro-CT rock lattice Boltzmann | Web / SCA | 0 new (SCA2011-28 seen, not opened) |
| 9 | Euler characteristic loss function segmentation deep learning connectivity | Web / arXiv | 0 (medical only) |
| 10 | connectivity-preserving segmentation porous material micro-CT deep learning pore throat | Web / InterPore | 1 |
| 11 | "pore throat" segmentation loss deep learning digital core permeability connectivity | Web | 0 |
| 12 | topological loss segmentation battery electrode tomography connectivity tortuosity | Web | 0 |
| 13 | gas diffusion layer X-ray tomography segmentation deep learning permeability evaluation loss | Web | 0 |
| 14 | soil pore network X-ray CT deep learning segmentation connectivity topology loss | Web | 1 |
| 15 | fracture segmentation CT clDice topology loss connectivity permeability | Web | 0 |
| 16 | 数字岩心 分割 拓扑 损失 渗透率 | Web (Chinese) | 0 |
| 17 | 孔隙 喉道 分割 深度学习 渗透率 误差 连通性 | Web (Chinese) | 0 |
| 18 | 拓扑感知 分割 岩心 CT 深度学习 | Web (Chinese) | 0 |
| 19 | 石油勘探与开发 数字岩心 图像分割 深度学习 孔隙连通性 渗透率 | Web (Chinese) | 0 |
| 20 | 数字岩心 阈值分割 渗透率 敏感性 分辨率 孔隙度 影响 | Web (Chinese) | 0 |
| 21 | 中心线 Dice 损失 孔隙 分割 骨架 CT | Web (Chinese) | 0 |
| 22 | "Bridging the Synthetic-to-Real Domain Gap in Pore-Scale Image Segmentation" connectivity-preserving | Web | 0 (found via OpenAlex instead) |
| 23 | Eshimiakhe Yasin connectivity domain gap pore segmentation tight sandstone Swin-UNETR | Web | 0 new |
| 24 | "Pore-Aware Gaussian Splatting" digital rock super-resolution | Web | 0 (SSRN blocked) |
| 25 | Garfi John Berg Krevor 2019 sensitivity of estimates ... to image processing | Web / TiPM | 1 |
| 26 | Salek Beckingham 2023 Earth and Space Science segmentation permeability micro-CT | Web | 0 |
| 27 | Zhang 2024 WRR "topology-based permeability prediction model" | Web / WRR | 1 |
| 28 | events.interpore.org segmentation topology loss micro-CT permeability deep learning | InterPore | 0 new |
| 29 | InterPore 2025 abstract segmentation connectivity Betti Euler permeability error | InterPore | 0 |
| 30 | differentiable flow simulation loss segmentation porous media end-to-end permeability | Web / arXiv | 0 (differentiable PNM papers are not segmentation) |
| 31 | EGU abstract topology-aware segmentation pore space deep learning connectivity permeability | EGU | 0 (EGU26-17416, EGU26-3949, AdGeo 67:79 opened, none relevant) |
| 32 | AGU Fall Meeting abstract segmentation errors permeability digital rock deep learning | AGU / ADS | 0 |
| 33 | Bayesian deep learning segmentation uncertainty digital rock permeability propagation ensemble | Web | 0 new |
| 34 | morphological erosion dilation pore space permeability sensitivity micro-CT "one voxel" | Web / TiPM | 0 opened (Perez 2022 unreachable) |
| 35 | voxel size relative to throat radius permeability error digital rock resolution | Web | 0 opened (Callow 2020 unreachable) |
| 36 | synthetic segmentation errors perturbation masks evaluate metrics permeability porous media | Web / Comput. Geosci. | 1 |
| 37 | Purswani Euler characteristic threshold small cluster removal micro-CT | Web | 0 new |
| 38 | super-resolution digital rock loss function permeability connectivity Euler physics-informed | Web / InterPore | 2 |
| 39 | Betti numbers segmentation evaluation digital rock sandstone deep learning permeability | Web | 0 new |
| 40 | trabecular bone micro-CT segmentation topology-preserving loss connectivity | Web (bone) | 0 |
| 41 | comparing pore networks from different segmentations throat matching metric | Web / SCA | 0 |
| 42 | "Absolute permeability estimation from microtomography rock images through deep learning super-resolution and adversarial fine tuning" | Web / Sci. Rep. | (same as #38) |
| 43 | "permeability-aware" OR "flow-aware" segmentation loss micro-CT | Web | 0 |
| 44 | percolation spanning cluster loss deep learning segmentation porous connected porosity | Web | 0 |
| 45 | 渗透率 损失函数 数字岩心 图像分割 网络 训练 物理约束 | Web (Chinese) | 0 |
| 46 | 石油学报 深度学习 岩心 CT 孔隙 分割 连通性 欧拉数 | Web (Chinese) | 0 |
| 47 | jgmaas.com SCA segmentation uncertainty permeability digital rock deep learning connectivity | SCA | 1 |
| 48 | OnePetro SPE paper segmentation deep learning digital rock permeability error pore connectivity loss URTeC | SPE / OnePetro (via web) | 1 |
| 49 | PoreSkel skeletonization grayscale micro-CT porous media deep learning Mahdaviara | AWR | 1 |
| 50 | "Intelligent Digital Rock Physics: Advances and Perspectives" Applied Sciences 2026 | Web | 0 |
| 51 | Lavrukhin Gerke Romanenko assessing fidelity NN segmentation soil XCT permeability IoU | Web / EGU | (same as #14) |
| 52 | Gerke Karsanina segmentation errors permeability pore-scale uncertainty 2023-2025 | Web | 0 |
| 53 | "On the Deviation of Computed Permeability Induced by Unresolved Morphological Features" | Web / TiPM | 0 opened |
| 54 | Mahmoudi Asghari Boisvert 2025 modified U-Net class weighting micro-CT | Web / C&G | 0 |
| 55 | low porosity near percolation threshold segmentation resolution permeability tight sandstone | Web | 1 |
| 56 | membrane OR foam OR "catalyst layer" tomography segmentation topology-aware loss | Web | 0 |
| 57 | "clDice" sandstone OR carbonate OR "digital rock" OR "pore space" 2025 2026 | Web | 0 |
| 58 | 拓扑损失 OR 骨架损失 OR clDice 数字岩心 孔隙 分割 渗流 | Web (Chinese) | 0 |
| 59 | Purswani Karpyn ... "Evaluation of image segmentation techniques for image-based rock property estimation" | Web / JPSE | 1 |
| 60 | (Eshimiakhe) Semantic Scholar DOI lookup | Semantic Scholar | (same as A2) |
| 61 | (SCA2026-037) full-text read | SCA | (same as #7) |
| 62 | (Howard SCA2018-034) full-text read | SCA | (same as #47) |
| 63 | (InterPore Journal 3(1) Tabrizipour 2026) full-text read | InterPore Journal | 0 (plain weighted-Dice benchmark) |

### 1b. Structured database / citation queries (13)

| # | Query | Venue | Hits |
|---|---|---|---|
| A1 | Citations of Wang et al. 2021 (arXiv 2002.05322) | Semantic Scholar API | failed (HTTP 429); `curl` was denied |
| A2 | `cites:W3131674184` (Wang 2021, ASoC 107185), 2025 onward: 50 works | OpenAlex | 1 (Eshimiakhe 2026), plus 7 screened by abstract |
| A3 | Same, up to 2024: 104 works | OpenAlex | 3 (Lavrukhin 2021, Li 2024 WRR, Niu 2020 WRR) |
| A4 | Find clDice work id | OpenAlex | n/a |
| A5 | Find Skeleton Recall work id | OpenAlex | n/a |
| A6 | `cites:W4403843587` (Skeleton Recall): 71 works, all screened by title | OpenAlex | 1 (Tang 2026 E&F, the only porous / rock one) |
| A7 | `cites:W3010789210` (clDice) AND title/abstract contains porous / rock / soil / pore / permeability / electrode / fracture / tomography: 111 works | OpenAlex | 2 (Tang 2026, Li et al. 2026 SSRN) |
| A8 | title/abstract search (topology OR connectivity OR clDice OR skeleton OR Betti OR Euler) AND loss AND segmentation AND (rock OR porous OR ...), 2020 onward: 48 works | OpenAlex | 1 (PoreSkel), others not relevant |
| A9 | abs:(topolog OR clDice OR skeleton OR Betti OR connectivity) AND segmentation AND (rock OR porous OR sandstone OR pore): 32 entries | arXiv API | 0 new |
| A10 | abs:permeability AND segmentation AND (loss OR perturbation OR sensitivity OR uncertainty): 9 entries | arXiv API | 0 |
| A11 | Find Krygier et al. 2021 work id | OpenAlex | n/a |
| A12 | `cites:W3116287554` (Krygier 2021): 71 works, all screened by title | OpenAlex | 1 (Jiang et al. 2024 Plant Soil) |
| A13 | Keyword search "topology-aware loss segmentation porous media permeability" | Semantic Scholar API | failed (HTTP 429) |

Total distinct queries: 59 web searches + 13 database queries = 72 (rows 60-63 are direct reads, not counted). Each OpenAlex result list was read in full, by
title (about 470 records in all). Abstracts were pulled for about 25 of them.

---

## 2. Relevant papers found (not in the first review)

Ordered by closeness to the project.

### 2.1 Eshimiakhe et al. 2026, IEEE TGRS: synthetic-to-real transfer and lost connectivity
- **Citation:** D. Eshimiakhe, Q. Yasin, M. Sun, B. Wang, D. A. Wood, B. Liu, "Bridging the
  Synthetic-to-Real Domain Gap in Pore-Scale Image Segmentation: Connectivity-Preserving
  Strategies for Digital Rock Reservoir Characterization", *IEEE Trans. Geosci. Remote Sens.*
  64:4507612 (2026). doi:10.1109/TGRS.2026.3745602
- **URL:** https://doi.org/10.1109/TGRS.2026.3745602 (redirects to ieeexplore document 11745544)
- **Access:** ABSTRACT, from OpenAlex and Semantic Scholar. OpenAlex lists it as hybrid open
  access (CC-BY), but the IEEE page renders with JavaScript and could not be read. Full text
  NOT read. It cites Wang et al. 2021.
- **What it does (from the abstract):** It segments tight-sandstone micro-CT from China's
  Southern Basin. It generates a "physics-informed" synthetic set with Gaussian random fields,
  using descriptors taken from the real data. It compares U-Net and Swin-UNETR under
  synthetic-only, direct-transfer, fine-tuning and hybrid regimes, against a real-only
  baseline. Direct transfer gives high Dice but fragmented pore networks with lost
  percolating connectivity. The authors define a "Connectivity Domain Gap" (CDG): about 1.00
  for direct transfer against about 0.06 after fine-tuning. Their conclusion: "reliable digital
  rock characterization requires preserving pore network topology beyond voxel-level accuracy
  alone."
- **Overlap:** Q1, partial. It is another high-Dice / broken-connectivity demonstration with
  a new connectivity metric. Q2: the "connectivity-preserving strategies" in the abstract are
  training regimes (transfer learning), not topology losses, but this must be confirmed in
  the full text. Q3: tight sandstone, so a low-porosity regime.
- **Threat:** **medium, pending full text.** Check (a) whether any connectivity or topology
  loss is used, (b) whether permeability is simulated, (c) how CDG is defined. If CDG is
  correlated against permeability across models, Q1 overlap grows. Cite it either way.

### 2.2 Fernandes et al. 2024, Sci. Rep.: training an image model through a differentiable permeability surrogate
- **Citation:** J. de C. V. Fernandes, A. D. Vidal, L. C. Medeiros, C. E. M. dos Anjos,
  R. Surmas, A. G. Evsukoff, "Absolute permeability estimation from microtomography rock images
  through deep learning super-resolution and adversarial fine tuning", *Sci. Rep.* 14:16704
  (2024). doi:10.1038/s41598-024-67367-1
- **URL:** https://pmc.ncbi.nlm.nih.gov/articles/PMC11271552/
- **Access:** FULL (open access, PMC).
- **What it does:** A super-resolution (SR) network is chained to a frozen CNN surrogate that
  predicts permeability. The SR network is then fine-tuned by back-propagating an MSE
  permeability loss through the surrogate ("adversarial" fine-tuning, with the surrogate as
  discriminator). Data: DeePore, about 17,700 semi-real 256³ volumes; the reference
  permeability comes from OpenPNM pore networks. Reported permeability MSE: surrogate alone
  0.035, SR + surrogate 0.051, fine-tuned SR + surrogate 0.013 (Table 3). No voxel or pixel
  fidelity metric and no connectivity or topology metric are reported. The authors note that
  fine-tuning adds noise and artifacts, shifts porosity and adds small pores.
- **Overlap:** Q2, adjacent. It is the only paper found that actually executes Wang et al.'s
  "approximate flow as a loss" idea on rock images. However, the task is SR, not
  segmentation; the target is the surrogate's own prediction, not an independent solver; there
  is no matched-overlap comparison; and no topology loss is used. It also warns that a
  flow-proxy loss can "game" the proxy by degrading the image.
- **Threat:** **low to medium.** It does not answer Q2. Cite it as the nearest
  differentiable-flow-loss precedent. Reviewers may ask why a surrogate-permeability loss was
  not one of the arms.

### 2.3 Garfi, John, Berg & Krevor 2019/2020, Transp. Porous Media: permeability is the most processing-sensitive property
- **Citation:** G. Garfi, C. M. John, S. Berg, S. Krevor, "The Sensitivity of Estimates of
  Multiphase Fluid and Solid Properties of Porous Rocks to Image Processing", *Transp. Porous
  Media* 131:985–1005 (2020; online Dec 2019). doi:10.1007/s11242-019-01374-z
- **URL:** https://spiral.imperial.ac.uk/entities/publication/38f39250-3226-4dab-9334-32956588112b
- **Access:** FULL (CC-BY, Imperial Spiral PDF).
- **What it does:** It compares two pipelines (non-local-means + watershed versus Trainable
  WEKA random forest) on Bentheimer, Berea, Ketton, Edwards and Estaillades. It computes
  porosity, specific surface area, single-phase permeability (OpenFOAM direct simulation),
  contact angle, curvature and mineral fractions. Permeability differences between pipelines
  are larger than the porosity or surface-area differences. Maximal-ball networks show
  "small shifts towards larger values of pore and throat radii distributions" when
  permeability rises. Sensitivity "increases with the complexity of its definition and its
  relationship to boundary shape". It explicitly does not study voxel size.
- **Overlap:** Q1, partial: it gives evidence that throat calibre, not porosity, drives the
  permeability differences. Only two pipelines are compared; there are no controlled
  perturbations, no topology metrics and no metric ranking.
- **Threat:** **low.** Cite it in the introduction with Leu 2014 and Saxena 2017.

### 2.4 Lavrukhin, Gerke, Romanenko et al. 2021, Soil & Tillage Res.: IoU versus permeability for soil
- **Citation:** E. V. Lavrukhin, K. M. Gerke, K. A. Romanenko, K. N. Abrosimov, M. V. Karsanina,
  "Assessing the fidelity of neural network-based segmentation of soil XCT images based on
  pore-scale modelling of saturated flow properties", *Soil Tillage Res.* 209:104942 (2021).
  doi:10.1016/j.still.2021.104942
- **URL:** https://doi.org/10.1016/j.still.2021.104942
- **Access:** SNIPPET for the journal paper (closed access; OpenAlex has no abstract). The
  companion EGU2020-8946 abstract (Romanenko, Lavrukhin, Vasilyev, Gerke) was opened:
  https://meetingorganizer.copernicus.org/EGU2020/EGU2020-8946.html
- **What it does (snippets plus EGU abstract):** U-Net + ResNet-101 trained on seven soil XCT
  images, with converging-active-contour labels. Scored by precision, recall and IoU, and by
  Stokes / pore-network saturated permeability. Snippets report that "IoU ... was found to be
  the most sensitive to false positive and false negative porosity predictions" and that
  permeability error reached about 5% for some samples. It cites Wang et al. 2021.
- **Overlap:** Q1, partial, for soil. It relates pixel metrics to permeability across trained
  networks; there are no controlled perturbations and no topology metrics.
- **Threat:** **low.** Exact claims are unverified because the full text was not read.

### 2.5 Jiang, Leung, Liu et al. 2024, Plant and Soil: segmentation uncertainty propagated to permeability
- **Citation:** Z. Jiang, A. K. Leung, J. Liu, et al., "Segmentation uncertainty of vegetated
  porous media propagates during X-ray CT image-based analysis", *Plant Soil* (2024).
  doi:10.1007/s11104-024-07030-w
- **URL:** https://doi.org/10.1007/s11104-024-07030-w
- **Access:** ABSTRACT (OpenAlex). Hybrid open access, CC-BY, but the Springer PDF redirected to
  a login and was not read.
- **What it does:** A machine-learning framework quantifies segmentation uncertainty in CT of
  glass beads with roots and water, and propagates it into phase fractions, morphology and
  absolute permeability. Fine roots carry more uncertainty than coarse roots. Small
  segmentation errors distort pore-morphology estimates. It cites Krygier et al. 2021.
- **Overlap:** Q1, adjacent (uncertainty propagation in Krygier's style, in porous media). No
  error-type separation is visible in the abstract.
- **Threat:** **low.**

### 2.6 Tang et al. 2026, Energy & Fuels: structure-preserving fracture segmentation citing clDice and Skeleton Recall
- **Citation:** J. Tang, J. Chai, X. Zhang, S. Cai, Y. Xiao, W. Liu, B. Liu, "Fracture Network
  Characterization for Supercritical CO2 Fracturing in Shale Using a Structure-Preserving
  Direction-Adaptive Segmentation Framework", *Energy Fuels* 40(35):19456–19470 (2026).
  doi:10.1021/acs.energyfuels.6c03530
- **URL:** https://doi.org/10.1021/acs.energyfuels.6c03530
- **Access:** ABSTRACT (OpenAlex inverted index). Closed access; full text not read.
- **What it does:** A 2D deep segmentation framework for CT of SC-CO2-fractured shale, built to
  keep microfractures connected. Reported scores: precision 87.96%, recall 92.04%, F1 89.96%,
  IoU 81.75%. The 2D masks are stacked into 3D networks, and "topological and geometric
  descriptors" are computed from them. It is the only porous-media / rock paper among the 71
  works citing Skeleton Recall, and it also cites clDice. The abstract does not say whether
  either is used as a loss, and it reports no permeability or flow simulation.
- **Overlap:** Q2, weak: fracture networks rather than pore space, no flow, 2D.
- **Threat:** **low.** Check the full text for whether clDice or Skeleton Recall is a baseline
  loss.

### 2.7 Alwan, Choudhry, Tliba, Glover, Collier, Alghamdi 2026, InterPore poster: connectivity-aware SEM pore segmentation
- **Citation:** "Connectivity-aware pore segmentation in carbonate SEM images using an attention
  U-Net with physics-aware refinement", InterPore 2026 (19–22 May 2026), contribution 8841.
- **URL:** https://events.interpore.org/event/58/contributions/8841/
- **Access:** ABSTRACT.
- **What it does:** 2D BSE-SEM of carbonates, three classes (isolated pores, connected pore
  pathways, matrix). The labels preserve 1–2 px throats. Connected-pore IoU is about 0.48. No
  topology loss and no permeability are described. The companion paper (Alwan et al., *Adv.
  Geosci.* 67:79–89, 2025, https://adgeo.copernicus.org/articles/67/79/2025/, FULL abstract
  read) benchmarks classical segmentation only. It names "topology-aware training" as a
  requirement but trains no model.
- **Overlap:** Q2, conceptual only.
- **Threat:** **none to low.** A group to watch: it may move to topology losses in 3D.

### 2.8 Tavakkoli, Wang, Zhao, Mostaghimi, Li, Armstrong 2026, SCA symposium: greyscale LBM to avoid threshold sensitivity
- **Citation:** O. Tavakkoli, Y. D. Wang, B. Zhao, P. Mostaghimi, Z. Li, R. T. Armstrong,
  "Single-Phase Greyscale Lattice Boltzmann Simulation for Porous Media", SCA2026-037, 39th
  Int. Symp. Society of Core Analysts (2026).
- **URL:** https://jgmaas.com/SCA/2026/SCA2026-037.pdf
- **Access:** FULL.
- **What it does:** A greyscale (Darcy–Brinkman) LBM runs on unsegmented images with a
  Kozeny–Carman closure. It matches binary high-resolution simulation within 1% on a
  co-registered Bandera Brown sub-volume. At the full low-resolution domain, greyscale and
  binary results diverge by 93%. The Kozeny–Carman constant scales with resolution. It states
  that binary permeability is "sensitive to the chosen segmentation threshold, introducing an
  often unquantified source of uncertainty", citing Saxena 2017, Garfi 2019 and Salek &
  Beckingham 2023. Same UNSW group as Wang et al. 2021.
- **Overlap:** Q3, adjacent: coarse resolution makes binary segmentation unreliable for
  permeability. It is also an alternative to segmentation that reviewers may raise.
- **Threat:** **none** for Q1 and Q2. Worth one sentence in the limitations section.

### 2.9 Howard, Lin & Zhang 2018, SCA symposium: segmentation uncertainty quantification in a shaly sandstone
- **Citation:** J. Howard, S. Lin, S. Zhang, "Uncertainty Quantification in Image Segmentation
  for Image-Based Rock Physics in a Shaly-Sandstone", SCA2018-034, Int. Symp. Society of Core
  Analysts, Trondheim (2018).
- **URL:** https://jgmaas.com/SCA/2018/SCA2018-034.pdf
- **Access:** FULL.
- **What it does:** It compares operator-seeded machine-learning segmentation with threshold
  sweeps, and proposes a sampling / numerical / physical UQ framework. It reports over 100%
  uncertainty, and finds that a threshold tuned to core porosity can still give a wrong pore
  distribution. Connected porosity was above 90% of total in all runs.
- **Overlap:** Q1, weak: a threshold sweep, but no metric ranking and no topology metric.
- **Threat:** **none to low.**

### 2.10 Li, Yang & Zhang 2024, Water Resour. Res.: regional-minima segmentation of unresolved rock images
- **Citation:** R. Li, Y. Yang, Y. Zhang, "A Novel Regional-Minima Image Segmentation Method for
  Fluid Transport Simulations in Unresolved Rock Images", *Water Resour. Res.* (2024).
  doi:10.1029/2023WR036855
- **URL:** https://doi.org/10.1029/2023WR036855
- **Access:** ABSTRACT (OpenAlex; gold open access).
- **What it does:** Pore-fraction (partial-volume) pixels appear as regional intensity minima.
  Converting them to pore raises modelled-permeability accuracy by over 50% compared with
  thresholding and over 30% compared with watershed, on sandstone and carbonate. It yields
  smaller throats and more detailed pore structure.
- **Overlap:** Q3. At coarse resolution, recovering thin throats is what fixes permeability.
  This supports the throat-calibre hypothesis. It also cites Wang et al. 2021.
- **Threat:** **low.** Consider it as a classical baseline for degraded inputs.

### 2.11 Zhang, Ma, Yang et al. 2024, Water Resour. Res.: which structural and topological features predict permeability
- **Citation:** J. Zhang, G. Ma, Z. Yang, J. Mei, D. Zhang, W. H. Zhou, X. Chang, "Knowledge
  Extraction via Machine Learning Guides a Topology-Based Permeability Prediction Model",
  *Water Resour. Res.* 60(7) (2024). doi:10.1029/2024WR037124
- **URL:** https://doi.org/10.1029/2024WR037124
- **Access:** ABSTRACT (OpenAlex; gold open access, CC-BY).
- **What it does:** XGBoost + SHAP on 458 porous-media samples. The most important features for
  permeability are closeness centrality (a graph topology feature), tortuosity, porosity,
  throat diameter, throat length and pore diameter. Partial-dependence laws are derived.
- **Overlap:** Q1, indirect. It ranks descriptors of the structure, not errors in the
  descriptors. It suggests that graph centrality and throat diameter deserve a place in the
  exploratory metric tier.
- **Threat:** **none.**

### 2.12 Dagdelen, Kondic et al. 2026, arXiv 2605.17581: topological data analysis features for permeability
- **Citation:** E. Dagdelen, C. N. Lalu, A. Karlekar, M. Arora, M. Illingworth, J. Jaquette,
  L. Cummings, L. Kondic, "Topological Data Analysis combined with Machine Learning for
  Predicting Permeability of Porous Media", arXiv:2605.17581 (v1 17 May 2026, v2 30 Jul 2026).
  Also an InterPore 2026 poster.
- **URL:** https://arxiv.org/abs/2605.17581 ; slides https://cfsm.njit.edu/publications/slides/dagdelen2026training.pdf
- **Access:** ABSTRACT (arXiv) + FULL (slides).
- **What it does:** Geometric, persistent-homology and SNOW2 pore-network features feed an
  ML regressor of permeability. The slides use 1000 PuMA overlapping-sphere structures at
  porosity 0.5. Persistent homology features (MAPE about 4.7%) and geometric features (about
  4.8%) are nearly tied; pore-network features alone do worse (about 6–12%).
- **Overlap:** Q1, indirect (descriptors, not segmentation errors). No segmentation is involved.
- **Threat:** **none.**

### 2.13 Purswani, Karpyn, Enab, Xue, Huang 2020, J. Pet. Sci. Eng.: segmentation method versus Euler characteristic
- **Citation:** P. Purswani, Z. T. Karpyn, K. Enab, Y. Xue, X. Huang, "Evaluation of image
  segmentation techniques for image-based rock property estimation", *J. Pet. Sci. Eng.*
  195:107890 (2020). doi:10.1016/j.petrol.2020.107890
- **URL:** https://pure.psu.edu/en/publications/evaluation-of-image-segmentation-techniques-for-image-based-rock-/
- **Access:** ABSTRACT (Penn State portal). This is the "Purswani et al." cited inside the Marfo
  review; it is listed here because the first review did not open it.
- **What it does:** A sintered glass frit with air and brine. It compares Fast Random Forest,
  k-means / fuzzy c-means clustering and thresholding on low-resolution images against
  high-resolution benchmarks, using porosity, saturation, surface and interfacial area, and
  Euler characteristic. The abstract does not mention permeability.
- **Overlap:** Q1/Q3, weak.
- **Threat:** **none.**

### 2.14 Niu, Mostaghimi, Shabaninejad, Swietojanski, Armstrong 2020, Water Resour. Res.: CNN segmentation judged by permeability variance
- **Citation:** Y. Niu, P. Mostaghimi, M. Shabaninejad, P. Swietojanski, R. T. Armstrong,
  "Digital Rock Segmentation for Petrophysical Analysis With Reduced User Bias Using
  Convolutional Neural Networks", *Water Resour. Res.* 56(2):e2019WR026597 (2020).
  doi:10.1029/2019WR026597
- **URL:** https://researchportalplus.anu.edu.au/en/publications/digital-rock-segmentation-for-petrophysical-analysis-with-reduced/
- **Access:** ABSTRACT.
- **What it does:** A CNN against watershed on sandstone, with ground truths from micro-CT and
  SEM. Porosity, permeability and pore-size distribution are compared. The CNN has smaller
  variance than threshold-dependent watershed.
- **Overlap:** Q1, weak (method comparison by permeability).
- **Threat:** **none.**

### 2.15 Andrew 2018, Comput. Geosci.: segmentation scored on synthetic images with known truth
- **Citation:** M. Andrew, "A quantified study of segmentation techniques on synthetic geological
  XRM and FIB-SEM images", *Comput. Geosci.* 22(6):1503–1512 (2018). doi:10.1007/s10596-018-9768-y
- **URL:** https://doi.org/10.1007/s10596-018-9768-y
- **Access:** ABSTRACT (OpenAlex; hybrid open access, CC-BY; Springer PDF blocked by a login
  redirect).
- **What it does:** Synthetic images built from a sandstone XRM scan (8.96 µm) and a shale
  FIB-SEM scan, with known truth. It compares multi-Otsu, seeded watershed and an ML
  classifier as noise increases. The abstract reports only voxel misclassification (over 50%
  for traditional methods in noisy textural regions, under 5% for ML).
- **Overlap:** Q1, design precedent only (synthetic truth). No permeability in the abstract.
- **Threat:** **none.**

### 2.16 Mahdaviara, Sharifi & Raoof 2023, Adv. Water Resour.: PoreSkel, deep skeletonization of greyscale micro-CT
- **Citation:** M. Mahdaviara, M. Sharifi, A. Raoof, "PoreSkel: Skeletonization of grayscale
  micro-CT images of porous media using deep learning techniques", *Adv. Water Resour.*
  180:104544 (2023). doi:10.1016/j.advwatres.2023.104544
- **URL:** https://research-portal.uu.nl/en/publications/poreskel-skeletonization-of-grayscale-micro-ct-images-of-porous-m/
- **Access:** ABSTRACT (via search-engine extract and Utrecht portal; green OA copy exists, not read).
- **What it does:** It predicts the skeleton and distance map directly from greyscale micro-CT,
  skipping segmentation. Data: 10,240 sub-volumes from 20 sandstone, carbonate and sand-pack
  samples. Skeleton F1 is 0.964 and distance-map RMSE 0.057. It is claimed to give more
  accurate pore networks than the medial axis.
- **Overlap:** Q2, tangential. A learned skeleton of porous media might matter for
  clDice-style losses on rock, where soft skeletons of blob-shaped bodies are poor.
- **Threat:** **none.**

### 2.17 Jacob et al. 2021, Solid Earth: micro-CT overestimates tight-sandstone permeability ninefold
- **Citation:** A. Jacob, M. Peltz, S. Hale, F. Enzmann, O. Moravcova, L. N. Warr, G. Grathoff,
  P. Blum, M. Kersten, "Simulating permeability reduction by clay mineral nanopores in a tight
  sandstone by combining computer X-ray microtomography and focussed ion beam scanning electron
  microscopy imaging", *Solid Earth* 12:1–14 (2021). doi:10.5194/se-12-1-2021 (a corrigendum
  exists)
- **URL:** https://se.copernicus.org/articles/12/1/2021/
- **Access:** ABSTRACT + article page (open access).
- **What it does:** Micro-CT at 2.43 µm alone gives a mean of 26.5 mD against 2.9 mD measured
  (+814%). Assigning FIB-SEM-derived permeability to microporous voxels gives 1.9 mD (−34.5%).
- **Overlap:** Q3. In tight rock the binary-segmentation error is dominated by unresolved pores;
  this limits what a pore/grain label can mean at low porosity.
- **Threat:** **none.**

### 2.18 Minor items opened, not threats (one line each)
- **Li, Pan, Wu, Kong, Zou, Chen 2026**, "Pore-Aware Gaussian Splatting for Structure-Preserving
  Super-Resolution of Digital Rock CT Images", SSRN doi:10.2139/ssrn.7412246. METADATA ONLY
  (SSRN 403). It cites clDice; keywords include "pore topology" and "Euler characteristic". It
  is super-resolution, not segmentation. Unknown whether a topology loss or permeability is
  used. Threat: unknown, probably low. Check if reachable.
- **Xing & Yao 2024**, InterPore 2024 contribution 6442, "Efficient 3D Digital Rock Detail
  Reconstruction and Quality Enhancement with Super-Resolution Transformer"
  (https://events.interpore.org/event/46/contributions/6442/). ABSTRACT. A "hybrid loss" for
  SR. Single-phase permeability error falls from 35% (tricubic) to 8%. Not segmentation, no
  topology loss. Threat: none.
- **Tabrizipour, Sadeghnejad, Hajipour, Schäfer 2026**, *InterPore J.* 3(1):IPJ010326-5,
  doi:10.69631/j6zv1891. FULL. U-Net with inverse-frequency-weighted Dice against
  watershed / multi-Otsu on fractured coal; voxel metrics and porosity only. Threat: none.

---

## 3. Seen but NOT opened (do not cite until checked)

- Li, Aslam & Yan 2025, SPE J. 226188-PA: integrated 3D pore segmentation + physics-constrained
  upscaling for permeability. The loss type is unknown. **Check: plausible Q2-adjacent.**
- Maas et al., SCA2011-28: probabilistic segmentation realisations propagated to computed
  properties (seen in a snippet).
- Perez, Moonen & Poncet 2022, TiPM 141, doi:10.1007/s11242-021-01713-z: permeability
  deviation from interface uncertainty (slip). HAL refused the connection.
- Callow et al. 2020, GJI (Bentheimer, 24 versus 12 µm): the snippet says the main error is
  "reassignment of voxels along the pore–solid interface and the subsequent change in pore
  connectivity". **Relevant to Q3**; eprints.soton returned 403.
- Lavrukhin & Gerke 2022, Adv. Syst. Sci. Appl. 22(4):31–50, on how image morphology affects NN
  segmentation (ijassa.ipu.ru DNS failure).
- Zha et al. 2017: pore dilation with LBM permeability (snippet).
- Salek & Beckingham 2023, Earth Space Sci. 10 (cited in SCA2026-037 for threshold sensitivity;
  not found by search).
- Reinhardt et al. 2022, Environ. Earth Sci. (fractured-rock segmentation benchmark,
  doi:10.1007/s12665-021-10133-7).
- Li et al. 2025, IEEE TMI, fast Euler-characteristic topology loss (medical; a candidate
  implementation of an Euler loss for this project).
- ContextLoss (Schacht et al., arXiv 2506.11134, ICIP 2025): a topology loss tested on bone
  nano-imaging.
- Mahmoudi, Asghari, Boisvert 2025, C&G 105853 (class weighting); Siavashi & Sharifi 2025,
  EAAI 112188 (multiphase segmentation assessment); Wang, Hou, Cao 2025, C&G 105884
  (edge-guided). OpenAlex has no abstracts for these; all cite Wang 2021.
- Chung & Day 2018, J. Math. Imaging Vis., "Topological Fidelity and Image Thresholding: A
  Persistent Homology Approach" (closed).

---

## 4. Venues that could not be reached or were only partly covered

- **Google Scholar:** not queried directly (no API); general web search was used instead.
- **Semantic Scholar API:** HTTP 429 on both citation-list and keyword calls; one DOI lookup
  succeeded. `curl` was denied in this session. OpenAlex citation lists were used instead;
  coverage may differ from Semantic Scholar's.
- **CNKI / Wanfang:** no direct access. Nine Chinese-language web searches returned no
  relevant hit. Index pages (napstic.cn, cup.edu.cn) appeared but none matched. *Acta Petrolei
  Sinica* (石油学报) and *Petroleum Exploration and Development* (石油勘探与开发) were not
  searched on their own sites.
- **ESS Open Archive / EarthArXiv:** not searched directly; one ESSOAr item surfaced by web
  search (not relevant).
- **IEEE Xplore** (JavaScript pages), **SSRN** (403), **MDPI** (403), **ScienceDirect** full
  texts, **Springer** PDFs (login redirect), **HAL** (connection refused),
  **eprints.soton.ac.uk** (403), **ijassa.ipu.ru** (DNS).
- **OnePetro / SPE / URTeC:** not searched natively; only web-indexed SPE items.
- **InterPore 2019–2024:** abstracts were reached only through web search; the programmes were
  not browsed session by session. InterPore 2025 and 2026 were partly covered.
- **SCA proceedings:** reached through jgmaas.com PDFs found by web search; the 2019–2026
  indexes were not browsed exhaustively.
- **AGU:** reached only through ADS snippets; no AGU abstract was opened.

Bottom line: Q2 remains open, with the same absence-of-evidence caveat as the first review,
now based on a citation sweep of Wang 2021, clDice, Skeleton Recall and Krygier 2021, plus
arXiv API searches. Before Gate 0, read in full: Eshimiakhe 2026 (TGRS), Li/Aslam/Yan 2025
(SPE J.) and Callow 2020 (GJI).
