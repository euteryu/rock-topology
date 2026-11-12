# Data manifest

Date verified for everything below: **2026-11-12**. Nothing has been downloaded yet. Checksums
are filled in at download time.

How it was checked: pages and API responses were fetched directly. No file over 50 MB was
downloaded. The only data-tree files actually fetched were small: DRP-317 metadata JSON
(208.4K), two binary-volume histogram CSVs (1.4K each), the DRP-362/211/215 metadata JSONs,
the Andrä benchmark `results/simulations.ods` (50.7 KB) and figshare / GitHub API listings.
"NOT VERIFIED" means the source did not show the detail, or could not be reached.

Rock terms used below:
- **Porosity**: fraction of the rock volume that is empty pore space.
- **Permeability**: how easily fluid flows through the rock. Units: mD (millidarcy).
  1 D is about 0.987e-12 m^2.
- **Segmentation / binary volume**: a voxel image labelled pore versus solid (grain).
- **Isolated pores**: pore voxels not connected to the pore network that crosses the sample.
  They hold fluid but carry no flow.
- **PNM / RMB / CNM**: three pore-network models. PNM is the classic pore network model. RMB
  is a reduced maximal-ball network. CNM is Neumann et al.'s capillary network model.
- **LBM**: lattice-Boltzmann, a direct voxel-level flow solver. **EJ Stokes**: an
  explicit-jump Stokes solver (GeoDict).

---

## 1. PRIMARY: "11 Sandstones: raw, filtered and segmented data" (DRP-317)

| Field | Value |
|---|---|
| DOI | 10.17612/f4h1-w124 (DataCite record: publisher "Digital Rocks Portal", 2020; DataCite `updated` 2025-11-11) |
| Landing URL (current) | DOI resolves (302) to `https://digitalporousmedia.org/published-datasets/drp.project.published.DRP-317`. This returned HTTP 403 to automated fetching, so it was not read directly. |
| Old URL | `https://www.digitalrocksportal.org/projects/317` now returns 301 to `https://digitalporousmedia.org/digital-rocks-portal-tombstone`. **The Digital Rocks Portal has moved.** It is now the Digital Porous Media Portal (DPMP) at TACC. |
| File host (verified, public) | TACC Web Corral: `https://web.corral.tacc.utexas.edu/digitalporousmedia/DRP-317/` (per-file tree) and `https://web.corral.tacc.utexas.edu/digitalporousmedia/archive/DRP-317/` (one zip + metadata + manifest) |
| Authors | Rodrigo Neumann, Mariane Andreeta, Everton Lucas-Oliveira (IBM Research / USP). Publication date 2020-10-08. |
| Licence | **ODC-BY 1.0** (Open Data Commons Attribution). Source: `license` field in `DRP-317_metadata.json`. ODC-BY allows commercial use, derivatives and redistribution, provided the database is attributed. The required attribution text is not given in the metadata, which only lists the related publications. Recommended attribution: cite the dataset DOI **and** Lucas-Oliveira et al. 2022 (Data in Brief) **and** Neumann et al. 2021 (Sci. Rep.). The old DRP user agreement asked users to cite DOI plus full citation (seen only in a search snippet, NOT VERIFIED on the live page). |
| Samples | 11. Bandera Gray, Parker, Kirby, Bandera Brown, Berea Sister Gray (BSG), Berea Upper Gray (BUG), Berea, Castlegate (folder "CastleGate"), Buff Berea (BB), Leopard, Bentheimer. Supplier: Kocurek Industries. |
| Volumes per sample | 3: `*_grayscale.raw` (raw reconstruction), `*_grayscale_filtered.raw` (contrast-enhanced + non-local means), `*_binary.raw` (segmented). |
| Format (from metadata `fileObjs`) | Headerless raw. width 1000, height 1000, numberOfImages 1000. imageType `8_bit`, byteOrder `little_endian`, offsetToFirstImage 0, gapBetweenImages 0. Every one of the 33 raw files is listed as 953.6M, which matches 1000^3 bytes = uint8 (consistency check computed here). |
| Label convention (binary) | **0 = pore, 1 = solid.** Evidence: the histogram CSVs on Corral. Parker binary has value 0 = 136,520,926 and value 1 = 863,479,074. Berea binary has value 0 = 216,715,332 and value 1 = 783,284,668. The 0-fractions (13.65% and 21.67%, computed) match the published image porosities (13.00% and 21.43% connected), so 0 is pore. No other values occur. |
| Voxel size | 2.25 µm isotropic (metadata `voxelX/Y/Z = 2.25`, `micrometer`). |
| Scanner | Bruker SkyScan 1272. Reconstruction in NRecon 1.7.0.4 (Data in Brief adds the InstaRecon 2.0.2.6 engine). **Acquisition settings disagree between sources.** The DRP metadata and Neumann et al. arXiv say "50 kV and 200 µA". The Data in Brief descriptor says 100 kV, 100 µA, Cu 0.11 mm filter, 4-frame averaging, 180° in 0.1° steps. NOT RESOLVED. |
| Plug / sub-sample | Lab plugs: 38 mm high, 19 mm radius. Imaged sub-samples: 30 mm high, 5 mm radius. The 1000^3 cube is cut from inside the reconstruction, away from the centre. |
| Greyscale bit depth | The paper says images were "converted ... from 16-bit to 8-bit gray scale" before processing. The published `grayscale.raw` files are 8-bit. |

### Reference segmentation method: settled as **IsoData** (single global threshold), not Otsu + watershed

- Data in Brief descriptor (Lucas-Oliveira et al. 2022), Data Description:
  > "The grayscale image was segmented at threshold level calculated using the IsoData algorithm [4]."

  Experimental Design: "the IsoData method [4] was used to compute a grayscale threshold level for each image". Abstract: "segmented images obtained by using the IsoData segmentation method". Ref. [4] is Ridler & Calvard 1978, "Picture thresholding using an iterative selection method". The descriptor does not mention Otsu or watershed.
- DRP metadata, per binary file (Parker shown, the others are identical except the level):
  > "Binary image data obtained from the filtered grayscale image data. The grayscale image was segmented at threshold level 72 calculated using the IsoData algorithm."
- Neumann et al. 2021 (arXiv v2, Methods): "by using a threshold level calculated by the IsoData method [40], we have segmented the noise-reduced grayscale images into solid and void space leading to a binary image."
- **Where "watershed" comes from:** Neumann et al. extracted the *pore network* with "the SNOW algorithm based on watershed transformation" (PoreSpy 1.2.0). That is a network-extraction step, not the segmentation. No source opened today says Otsu for DRP-317. Otsu-type segmentation belongs to the IBM dataset (item 2, Multi-Otsu) and the Imperial 2007 images (item 3).
- **Important difference:** the published binary volumes **include isolated pores**. Data in Brief: "the segmented image includes isolated pores, unlike what is observed in the related work developed by Neumann". In the Sci. Rep. paper the authors "eliminated from each data cube the pore voxels that are not connected to the percolating network" (Hoshen-Kopelman). Their µCT porosities and simulated permeabilities therefore refer to the *connected* pore space. Our pipeline must apply the same connected-component filter before comparing.
- Pipeline before thresholding (descriptor and metadata): 16-to-8-bit conversion. Histogram cut-off where the cumulative histogram reaches 99.8%, then rescaling to [0,255]. 3D non-local means in Fiji (smoothing factor 1, sigma estimated automatically). Then the IsoData threshold.

Per-sample processing parameters, from Neumann et al. arXiv v2 Suppl. Table S1, which match the per-file DRP metadata descriptions:

| Sample | Contrast cut-off level | IsoData threshold |
|---|---|---|
| A Bandera Gray | 93 | 81 |
| B Parker | 63 | 72 |
| C Kirby | 61 | 75 |
| D Bandera Brown | 73 | 80 |
| E Berea Sister Gray | 90 | 54 |
| F Berea Upper Gray | 101 | 48 |
| G Berea | 71 | 59 |
| H Castlegate | 156 | 81 |
| I Buff Berea | 62 | 73 |
| J Leopard | 76 | 72 |
| K Bentheimer | 200 | 71 |

### Lab and published simulated properties

Lab method (Neumann et al.): porosity by helium in a Boyle's-law double cell. Permeability from steady-state nitrogen flow, Klinkenberg-corrected, API RP-40, 500 psi confining. Stated error ±0.5% (porosity) and ±10% (permeability).
Simulations (Neumann et al.): network models on the full 1000^3 connected-pore cube, water with µ = 1 cP, 10 kPa/m gradient. Each value is the quadratic mean of k along x, y and z.

Source: Neumann et al. arXiv:2010.10679v2, Supplementary Table S2. Sci. Rep. Table 1 has the same lab values, with two small differences noted in the table.

| Sample | Porosity lab (%) | Porosity µCT, connected (%) | k lab (mD) | k PNM (mD) | k RMB (mD) | k CNM (mD) |
|---|---|---|---|---|---|---|
| A Bandera Gray | 18.10 | 20.56 | 9 | 40 | 29 | 26 |
| B Parker | 14.77 | 13.00 | 10 | 13 | 8 | 11 |
| C Kirby | 19.95 | 21.35 | 62 | 154 | 93 | 76 |
| D Bandera Brown | 24.11 | 20.93 | 63 | 67 | 45 | 38 |
| E Berea Sister Gray | 19.07 | 19.57 | 80 | 138 | 79 | 86 |
| F Berea Upper Gray | 18.56 | 19.38 | 85 (Sci. Rep. Table 1: 86) | 122 | 66 | 70 |
| G Berea | 18.96 | 21.43 | 121 | 186 | 106 | 102 |
| H Castlegate | 26.54 | 24.50 | 269 | 450 | 234 | 249 |
| I Buff Berea | 24.02 | 22.50 | 274 (Sci. Rep. Table 1: 275) | 471 | 230 | 267 |
| J Leopard | 20.22 | 19.28 | 327 | 226 | 126 | 153 |
| K Bentheimer | 22.64 | 26.56 | 386 | 973 | 480 | 538 |

The DRP metadata `porosity` field per sample equals the lab porosity column. It has no permeability field.
Neumann et al. Suppl. Fig. S2: on Berea the mean simulated (CNM) k converges to the lab value only at a cube side of 2250 µm (1000 voxels). Smaller cubes overestimate it. Sub-volumes of 256^3 to 400^3 will therefore not reproduce the lab k. Compare crops against our own full-cube reference, not against the lab.

Other simulated values found (not peer-reviewed, lower weight):
- `geomech-project/voids` documentation (https://geomech-project.github.io/voids/validation/drp317) gives PoreSpy-snow2 / PREGO / maximal-ball network permeabilities for all 11 samples on ROIs (e.g. Berea 256^3 ROI at origin (0,744,0): snow2 139.98 mD, maximal-ball 80.05 mD). Its XLB-LBM 75^3 ROIs give 383.8 to 3700.7 mD, far above the lab values, which shows small-ROI LBM is unreliable here.
- Liu et al. (github huahualiu0302/Permeability-prediction) use 256^3 sub-volumes with PNM-computed k. The README gives no values.
- A 2025 TiPM capsule-network paper (doi 10.1007/s11242-025-02270-5) reportedly used LBM on 6 of these sandstones. NOT VERIFIED (not opened).
- The second related publication listed in the DRP metadata (Lucas-Oliveira et al., J. Pet. Sci. Eng., doi 10.1016/j.petrol.2020.107400, NMR relaxivity + digital permeability) was NOT opened.

### Files and sizes (Corral listing, sizes exactly as shown by the server, "M" = MiB)

Every sample folder holds three sub-folders, `<prefix>_2d25um_{grayscale,grayscale_filtered,binary}.raw/`. Each sub-folder contains the `.raw` (953.6M) plus a preview `.gif`, `.histogram.csv`, `.histogram.jpg`, `.jpg` and `.thumb.jpg`. Only the `.raw` files are needed. The GIFs are large and should be skipped.

| Sample folder | File prefix | binary.raw | grayscale.raw | grayscale_filtered.raw | binary .gif | grayscale .gif | filtered .gif |
|---|---|---|---|---|---|---|---|
| Bandera Gray | BanderaGray | 953.6M | 953.6M | 953.6M | 39.5M | 733.1M | 179.9M |
| Parker | Parker | 953.6M | 953.6M | 953.6M | 22.3M | 621.9M | 755.3M |
| Kirby | Kirby | 953.6M | 953.6M | 953.6M | 35.7M | 527.3M | 838.3M |
| Bandera Brown | BanderaBrown | 953.6M | 953.6M | 953.6M | 38.7M | 60.1M | 337.5M |
| Berea Sister Gray | BSG | 953.6M | 953.6M | 953.6M | 31.7M | 583.2M | 731.5M |
| Berea Upper Gray | BUG | 953.6M | 953.6M | 953.6M | 22.4M | 551.0M | 683.6M |
| Berea | Berea | 953.6M | 953.6M | 953.6M | 34.8M | 64.9M | 783.1M |
| CastleGate | CastleGate | 953.6M | 953.6M | 953.6M | (no gif listed) | 164.1M | 851.5M |
| Buff Berea | BB | 953.6M | 953.6M | 953.6M | 28.9M | 80.2M | 800.4M |
| Leopard | Leopard | 953.6M | 953.6M | 953.6M | 27.4M | 116.6M | 773.2M |
| Bentheimer | Bentheimer | 953.6M | 953.6M | 953.6M | 31.2M | 135.5M | 92.6M |

Small files (per sub-folder): histogram.csv 1.4K to 2.8K, jpgs 13.9K to 329.1K. The Bandera Gray grayscale folder also holds stray `BanderaGray_2d25um_Rec_grayscale.raw.*` preview files (2.4K, 143.2K, 183.4K).

Archive folder `archive/DRP-317/`: `DRP-317_archive.zip` **22.9G**, `DRP-317_metadata.json` 208.4K, `manifest-sha512.txt` 42.4K (the fetch failed with a socket hang-up, so its contents are NOT VERIFIED).

Totals (computed here from the listed sizes):
- 11 binary volumes: 11 × 953.6M = **10.2 GiB** (about 11.0 GB).
- All 33 raw volumes (binary + grayscale + filtered): **30.7 GiB** (about 33 GB). **Over the 20 GB hard stop.**
- All files including preview GIFs: about 41.3 GiB.
- The one-click zip archive: 22.9G. **Over the 20 GB hard stop.**

### Download mechanism

- **Per-file direct HTTPS download works without login.** Web Corral serves a plain lighttpd directory index, and individual files can be fetched by URL. This was tested on the small `*.histogram.csv` files, which downloaded without authentication. A full `.raw` was not downloaded (it exceeds the 50 MB limit).
- URL pattern: `https://web.corral.tacc.utexas.edu/digitalporousmedia/DRP-317/<Sample folder>/<prefix>_2d25um_<type>.raw/<prefix>_2d25um_<type>.raw`. Spaces in folder names must be URL-encoded as `%20`.
- DPMP documentation (https://digital-porous-media.github.io/dpm_docs/download_data) says to use the portal's "Download Dataset" button for datasets under 2 GB. For larger datasets it recommends Globus or the Web Corral folder `https://web.corral.tacc.utexas.edu/digitalporousmedia/`. Whether the DPMP portal itself requires login was NOT VERIFIED (portal returned 403).
- No REST API was found that works anonymously. `digitalporousmedia.org/api/...` returned 403.
- Integrity: `manifest-sha512.txt` in the archive folder presumably lists SHA-512 per file (NOT VERIFIED). Use it at download.
- **Example, one segmented volume of one sample for a first test:**
  `https://web.corral.tacc.utexas.edu/digitalporousmedia/DRP-317/Berea/Berea_2d25um_binary.raw/Berea_2d25um_binary.raw` (953.6M; uint8, little-endian, 1000×1000×1000, 0 = pore)
- Checksum: to fill at download.

---

## 2. IBM microCT-Dataset (Esteves Ferreira et al., Scientific Data 2023)

| Field | Value |
|---|---|
| Paper | Esteves Ferreira M. et al., "Full scale, microscopically resolved tomographies of sandstone and carbonate rocks augmented by experimental porosity and permeability values", *Sci. Data* 10, 368 (2023), doi 10.1038/s41597-023-02259-z, PMC10247717. Paper licence CC BY 4.0. |
| Data DOI / URL | 10.25452/figshare.plus.21375565 (current version v6, published 2023-04-17). `https://plus.figshare.com/articles/dataset/Full_scale_microscopically_resolved_tomographies_of_sandstone_and_carbonate_rocks_augmented_by_experimental_porosity_and_permeability_values/21375565` |
| **Data licence** | **CDLA-Sharing-1.0** (Community Data License Agreement, Sharing 1.0, https://cdla.dev/sharing-1-0/), per the figshare API `license` field. It is **not** CC BY. CDLA-Sharing allows use, modification and commercial use. If you *publish/share the data or modified data*, you must do so under CDLA-Sharing (a copyleft-like condition) and keep the notices. Results computed from the data are not restricted. |
| GitHub | `https://github.com/IBM/microCT-Dataset` returned **HTTP 404** on 2026-11-12, so it was removed or made private. A search snippet described a `DigitalRock.ipynb` notebook under BSD-3-Clause (NOT VERIFIED now). |
| Total size | **1,530,541,492,772 bytes** (about 1.53 TB / 1.39 TiB), **293 files** (figshare API). |
| Samples | 18 plugs, 9.5 mm diameter × 25.4 mm long. 5 sandstones (13A Castlegate, 14A Carbon Tan, 15A Bentheimer, 18A Liver Rock, 20A Idaho Gray). 13 carbonates (1B, 1C, SD Silurian Dolomite; 4A, I-151016, 2-ILC Indiana Limestone; 5A Lueders; 6A Mt. Gambier; GD Guelph Dolomite; EdY, EdW, EdB-1 Edwards Yellow/White/Brown; DP Desert Pink). |
| Scanner, voxel | Bruker SkyScan 1272. 2.25 µm voxels ("2p25um" in every file name). NRecon 1.7.4.6 / InstaRecon 2.0.4.6. |
| Volumes per sample | `_grayscale_full` (largest inscribed box, e.g. 3000×3000×12300 for DP), `_grayscale_standard` (2500×2500×7500), three `_grayscale_ROI-1..3` cubes (2500^3), three `_grayscale_filtered_ROI-X`, and three `_binary_ROI-X` (2500^3). All raw volumes are distributed as `.raw.tar.bz2`, each with a small `.hdr` (about 196 bytes) holding the size information. Also `Dataset_Information.xlsx` (99,875 B) and QRM bar-pattern volumes (`qrm_10w__ir_rec_tra_vertical.raw` 509,858,184 B; `..._horizontal.raw` 351,623,300 B). |
| dtype / endianness | NOT VERIFIED. The paper does not state them, and the `.hdr` fetch failed (signed S3 link expired). Read the `.hdr` at download. |
| Label convention | Paper: "values 0 and 1 for void and solid matrix spaces, respectively". 0 = pore, which matches DRP-317. |
| Segmentation | Contrast stretch (99.8% cut-off), then 3D anisotropic diffusion (Perona-Malik, 5 iterations, gradient threshold 10). Then "Each grayscale cube was segmented at a threshold level calculated using the Multi-Otsu algorithm with a number of classes set to three". The intermediate class "was considered part of the mineral matrix". Thresholds per ROI are in paper Table 3 (not copied). |

Binary ROI file sizes (compressed `.tar.bz2`, bytes, figshare API):

| Sample (file prefix) | ROI-1 | ROI-2 | ROI-3 |
|---|---|---|---|
| sd | 188,961,314 | 199,614,569 | 189,892,547 |
| edb-1 | 441,733,025 | 408,940,539 | 412,293,812 |
| dp | 515,455,345 | 495,803,089 | 496,206,932 |
| kocurek_6a | 326,242,425 | 333,806,566 | 325,542,644 |
| ilc2 | 338,755,839 | 348,100,515 | 319,166,192 |
| kocurek_5a | 226,343,286 | 321,589,494 | 300,747,768 |
| kocurek_4a | 102,987,628 | 103,472,025 | 102,095,817 |
| kocurek_20a | 185,514,671 | 184,402,440 | 187,339,697 |
| kocurek_1b | 134,835,039 | 123,141,291 | 121,470,065 |
| kocurek_18a | 302,668,825 | 298,682,152 | 298,873,517 |
| kocurek_15a | 278,084,437 | 275,156,643 | 272,425,570 |
| kocurek_13a | 294,395,545 | 291,239,808 | 287,163,594 |
| kocurek_14a | 268,648,972 | 266,487,228 | 269,901,364 |
| kocurek_1c | 152,082,577 | 146,144,001 | 143,891,689 |
| edw | 436,367,700 | 531,688,056 | 602,921,650 |
| edy | 251,422,873 | 251,994,390 | 244,510,842 |
| gd | 89,192,721 | 90,711,456 | 84,825,949 |
| i-151016 | 127,058,260 | 134,202,178 | 124,572,753 |

The large greyscale files, e.g. for kocurek_15a: full 30,278,430,888 B, standard 16,256,226,344 B, ROI greyscale about 5.3 to 5.6 GB each, filtered ROI about 7.8 to 8.1 GB each. The five largest files are 35.9 to 53.5 GB (the `_grayscale_full` volumes). Not every greyscale file was listed individually here. The full per-file list is in the figshare API: `https://api.figshare.com/v2/articles/21375565`.
Uncompressed size of one 2500^3 uint8 binary ROI would be 15.6 GB (computed, assuming 1 byte/voxel, which is NOT VERIFIED).

Download mechanism: figshare+ direct links, no login. Pattern `https://ndownloader.figshare.com/files/<id>`, which redirects to a time-limited S3 URL. Example: kocurek_4a binary ROI-1 = `https://ndownloader.figshare.com/files/38022590`. Per-file download works.

Lab properties (paper Table 4; computed porosity is the mean of 3 ROIs; k in mD; nitrogen at 21 °C, 500 psi overburden):

| Sample | Rock | φ lab (%) | φ image mean (%) | k air (mD) | k Klinkenberg (mD) |
|---|---|---|---|---|---|
| 1B | Silurian Dolomite | 8.22 | 11.70 | 67.39 | 61.34 |
| 1C | Silurian Dolomite | 13.46 | 13.34 | 373.14 | 353.53 |
| 4A | Indiana Limestone | 14.71 | 8.27 | 23.11 | 20.41 |
| 5A | Lueders | 13.89 | 11.23 | 55.79 | 50.66 |
| 6A | Mt. Gambier | 53.45 | 39.18 | 144.41 | 134.37 |
| 13A | Castlegate | 27.39 | 17.23 | 638.56 | 610.16 |
| 14A | Carbon Tan | 23.49 | 13.16 | 67.56 | 61.53 |
| 15A | Bentheimer | 22.91 | 21.29 | 0.42 | 0.31 |
| 18A | Liver Rock | 25.00 | 21.44 | 392.97 | 372.64 |
| 20A | Idaho Gray | 28.48 | 27.54 | >5,000.00 | 5,000.00 |
| SD | Silurian Dolomite | 14.67 | 13.19 | 80.59 | 73.80 |
| I-151016 | Indiana Limestone | 17.57 | 12.40 | 50.11 | 45.23 |
| GD | Guelph Dolomite | 14.35 | 11.45 | 1228.80 | 1184.53 |
| EdY | Edwards Yellow | 25.96 | 16.84 | 11.45 | 9.80 |
| EdW | Edwards White | 15.38 | 12.73 | 0.63 | 0.48 |
| EdB-1 | Edwards Brown | 29.63 | 18.45 | 14.61 | 12.59 |
| DP | Desert Pink | 24.54 | 18.61 | 47.98 | 43.26 |
| 2-ILC | Indiana Limestone | 17.05 | 14.03 | 72.94 | 66.57 |

Caution: 15A Bentheimer at 0.42 mD is implausible for Bentheimer (DRP-317 Bentheimer lab value: 386 mD). It may be a transcription error in the paper. Do not use it as a benchmark without checking with the authors.
Checksum: to fill at download.

---

## 3. Imperial College pore-scale modelling images and networks (Blunt / Bijeljic group)

Page: `https://www.imperial.ac.uk/earth-science/research/research-groups/pore-scale-modelling/micro-ct-images-and-networks/`. The images are not on the Digital Rocks Portal (no Imperial folder in the Corral list). Contact on the page: Branko Bijeljic.

**2015 set (sandstone + carbonate, 1000^3 voxels).** Hosted on Imperial Box. Box pages render via JavaScript, so file sizes are NOT VERIFIED and whether login is needed is NOT VERIFIED.

| Sample | Size | Voxel (µm) | Link |
|---|---|---|---|
| Bentheimer sandstone (image from iRock Technologies) | 1000^3 | 3.0035 | https://imperialcollegelondon.box.com/v/iccpsim-bentheimer2015 |
| Doddington sandstone | 1000^3 | 2.6929 | https://imperialcollegelondon.box.com/v/iccpsim-doddington2015 |
| Estaillades carbonate | 1000^3 | 3.31136 | https://imperialcollegelondon.box.com/v/iccpsim-estaillades2015 |
| Ketton carbonate | 1000^3 | 3.00006 | https://imperialcollegelondon.box.com/v/iccpsim-ketton2015 |
| Bulk | | | https://imperialcollegelondon.box.com/v/ImagesICPSC2015 |

Format: `.mhd` header + raw. **Licence: not stated on the page.** Treat as "ask before redistribution" and cite Raeini et al. 2017 and the page. Segmentation: the page points to Andrew (2014) PhD thesis. A search snippet for a related Imperial page said "multi-thresholding based on Otsu's algorithm" (NOT VERIFIED on that page).

Published permeabilities for the 2015 set. Source: Raeini, Bijeljic & Blunt, *Phys. Rev. E* 96, 013312 (2017), Table I, open access CC BY 4.0. Units are ×10^-12 m^2 as printed; the mD conversion was computed here.

| | Bentheimer | Doddington | Estaillades | Ketton |
|---|---|---|---|---|
| Image | 1000^3 | 1000^3 | 1000^3 | 1000^3 |
| Voxel (µm) | 3.003 | 2.693 | 3.311 | 3.000 |
| Porosity | 0.216 | 0.194 | 0.109 | 0.132 |
| k DNS (×10^-12 m^2) | 3.55 | 3.76 | 0.218 | 5.91 |
| k GNM | 3.35 | 3.63 | 0.21 | 5.75 |
| k CNM (conventional network) | 2.46 | 3.19 | 0.114 | 4.94 |
| Formation factor DNS | 15.5 | 20.0 | 166 | 24.2 |
| k DNS in mD (computed) | ~3597 | ~3810 | ~221 | ~5988 |

**2007 set (Dong 2007 thesis; 19 samples incl. Berea, sandstones S1 to S9, carbonates C1 and C2, sand packs, silica).** On figshare. Example verified: Berea, doi 10.6084/m9.figshare.1153794 (v2), **CC BY 4.0**, a single file `Berea.7z` of **3,690,231 bytes** (`https://ndownloader.figshare.com/files/3216671`), with an NRRD header `Berea.nhdr`. The image size and voxel size are in the header and were NOT VERIFIED. The other 2007 records (DOIs 10.6084/m9.figshare.1189255 to 1189286, 1153795) are presumably the same, but their licence and size are NOT VERIFIED. Bulk: https://imperialcollegelondon.box.com/v/ImagesICPSC2007. Published Berea network permeability (Dong & Blunt 2009, PRE 80, 036307) is paywalled and was not opened, so it is NOT VERIFIED.
Checksum: to fill at download.

---

## 4. MRCCM: Multi-Resolution Complex Carbonates Micro-CT dataset (Alqahtani et al.)

| Field | Value |
|---|---|
| Dataset | "A Multi-Resolution Complex Carbonates Micro-CT Dataset (MRCCM)", **DRP-362**, DOI **10.17612/3t36-q704**, published 2021-05-19, UNSW. Authors Alqahtani, Mostaghimi, Armstrong. |
| Related paper | Alqahtani N.J. et al., "Super-Resolved Segmentation of X-ray Images of Carbonate Rocks Using Deep Learning", *Transp. Porous Media* 143(2), 497–525 (2022), doi 10.1007/s11242-022-01781-9. The paper is CC BY 4.0 (Crossref license field). Springer full text needs a cookie login for automated fetch, so the paper's own data-availability statement was NOT read. The link between paper and dataset is confirmed by the DRP-362 metadata ("related publication"). |
| **Downloadable?** | **Yes.** Public Corral tree `https://web.corral.tacc.utexas.edu/digitalporousmedia/DRP-362/` (folders "Indiana Limestone (ILS)" and "Middle Eastern Carbonate (MEC)"). |
| Licence | **ODC-BY 1.0** (metadata). The dataset asks users to "cite both (DOI) of this project and the related journal publication." |
| Size | Archive `DRP-362_archive.zip` **99.3G**. Also a stray file `zi1lmpn8` (20.8G) in the archive folder, purpose unknown. Verified per-file sizes (ILS): `ILS_seg_hr.mat` 556.2M; `ILS_LR.mat` 201.9M; `ILS1.mat` 3.1G, `ILS2.mat` 3.1G, `ILS3.mat` 3.0G, `ILS4.mat` 407.8M. MEC per-file sizes NOT VERIFIED. |
| Content | Two monomineralic (>95% calcite) carbonates: Indiana Limestone (MICP porosity 16.38%: macro 9.17%, micro 7.22%) and Middle Eastern Carbonate (MICP 29.79%: macro 17.84%, micro 10.97%). 6 mm plugs, HeliScan micro-CT (Mark I), UNSW. **HR 2.68 µm, LR 10.72 µm** (4× ratio). Raw tomograms are netCDF `.nc` blocks of [2520 2520 40] voxels, variable `tomo` (HR: ILS 101 blocks, MEC 119; LR: ILS 25, MEC 31). Processed volumes are registered central LR/HR domains as MATLAB v7.3 `.mat` (h5py-readable). The HR is split into 4 z-parts. MEC HR domain is 1520×1520×4100. |
| Segmentation | "The segmentations were performed using Avizo Software using a combination of watershed and hysteresis algorithms." There are **three phases**: macropores, solid grains, microporosity (sub-resolution porosity). Only the HR volumes are segmented. The paper's test volume is the first 256 (LR) / 1024 (HR) voxels in x, y and z. |
| Lab properties | MICP porosities only (above). No permeability is listed. |
| Verdict for this project | Usable as the conditional robustness check: a real paired LR/HR scan, open licence, single-file downloads. A binary pore/grain label is **not** directly defensible: the third "microporosity" phase must be assigned to pore or solid, and that choice must be documented. The ILS processed set alone (LR + seg + HR) is about 10.4 GB (computed from the sizes above), under 20 GB. |

Checksum: to fill at download.

---

## 5. DeepRock-SR (DRP-215) and DRSRD1 (DRP-211)

| | DeepRock-SR (DRP-215) | DRSRD1 (DRP-211) |
|---|---|---|
| Title | "A Diverse Super Resolution Dataset of Digital Rocks (DeepRock-SR): Sandstone, Carbonate, and Coal" | "A Super Resolution Dataset of Digital Rocks (DRSRD1): Sandstone and Carbonate" |
| DOI | 10.17612/s3m9-e024 | 10.17612/P7D38H |
| Authors / date | Y.D. Wang, R. Armstrong, P. Mostaghimi (UNSW), 2019-05-20 | Y.D. Wang, P. Mostaghimi, R. Armstrong (UNSW), 2019-04-16 |
| Licence | ODC-BY 1.0 | ODC-BY 1.0 |
| Size | Archive zip **14.6G** | Archive zip **6.6G** |
| URL | `https://web.corral.tacc.utexas.edu/digitalporousmedia/DRP-215/` (archive: `.../archive/DRP-215/`) | `https://web.corral.tacc.utexas.edu/digitalporousmedia/DRP-211/` (archive: `.../archive/DRP-211/`) |
| Content | 12,000 2D PNG (500×500) + 3,000 3D MAT (100^3, array `temp`). Bentheimer ×2, Berea, Leopard, Gildehauser, Wilcox tight sandstone; Estaillades, Savonnieres, Massangis carbonates; 2 coals. | 2D PNG 800×800 and 3D MAT 80^3. Bentheimer (3.8 µm) and Estaillades (3.1 µm). |
| LR generation | Synthetic: MATLAB `imresize`/`imresize3` downsampling ×2 and ×4 (default and randomised settings). Not real LR scans. | Same method. |
| Segmentation | None (greyscale only). Voxel sizes not stated in DRP-215 metadata. | None. |
| Relevance | Low. Greyscale-only and synthetic degradation, with no permeability. | Low. Same reasons. |

Checksum: to fill at download.

---

## 6. Small benchmark with published permeability: Andrä et al. 2013 "Digital Rock Physics Benchmarks"

| Field | Value |
|---|---|
| Repository | `https://github.com/fkrzikalla/drp-benchmarks` ("Supplements to 'Digital Rock Physics Benchmarks'"), last push 2012-09-18, default branch `master`. |
| Licence | **None declared** (GitHub `license: null`, no LICENSE file in the tree). By default all rights are reserved. Using the files for research and citing the papers is the normal practice. Redistributing them (for example inside our repo or a Kaggle dataset) is **not** clearly permitted. Do not re-host; download at run time instead. |
| Papers | Andrä et al., "Digital rock physics benchmarks—part I: Imaging and segmentation", *Comput. Geosci.* 50, 25–32 (2013), doi 10.1016/j.cageo.2012.09.005. "—part II: Computing effective properties", 50, 33–43, doi 10.1016/j.cageo.2012.09.008. Neither paper was opened (paywalled; OA repository copies failed to load). The numbers below come from the repository's own `results/simulations.ods`, the authors' supplement. |
| Format | README: "Segmented images are provided in raw unsigned char format (uint8), compressed using gzip." Headerless. Which label value is pore is NOT VERIFIED (check by porosity after download: 0.147 for Fontainebleau). |
| Endianness | Not applicable (uint8). |

Files (git tree, bytes):

| Path | Bytes | Image (nx×ny×nz) | Voxel (µm) | Segmentation |
|---|---|---|---|---|
| images/fontainebleau/segmented-exxon.raw.gz | **1,090,208** | 288×288×300 | 7.50 | ExxonMobil |
| images/berea/segmented-vsg.raw.gz | 32,679,828 | 1024^3 | 0.74 | VSG (reference) |
| images/berea/segmented-stanford.raw.gz | 25,393,873 | 1024^3 | 0.74 | Stanford |
| images/berea/segmented-kongju.raw.gz | 42,743,165 | 1024^3 | 0.74 | Kongju |
| images/berea/segmented-kongju.mat | 61,132,732 | | | |
| images/grosmont/segmented-vsg.raw.gz | 59,571,790 | 1024^3 | 2.02 | VSG |
| images/grosmont/segmented-su.raw.gz | 68,453,587 | 1024^3 | 2.02 | Stanford |
| images/grosmont/segmented-kongju.raw.gz | 40,111,356 | 1024^3 | 2.02 | Kongju |
| images/grosmont/segmented-kongju.mat | 43,848,191 | | | |
| images/berea/tif/B6_10_*.rec.16bit.tif | 2,097,350 each (≥375 files; full count not visible) | | | greyscale |
| images/grosmont/tif/Carb*.tif | 2,098,374 each (≥114 files; full count not visible) | | | greyscale |
| images/spherepack/segmented-788x791x793.raw.gz | size NOT VERIFIED | 788×791×793 | 7.00 | generated |

Image dimensions and voxel sizes come from the `Samples` sheet of `results/simulations.ods`.
Direct download: `https://raw.githubusercontent.com/fkrzikalla/drp-benchmarks/master/images/fontainebleau/segmented-exxon.raw.gz` (also via `https://github.com/fkrzikalla/drp-benchmarks/raw/master/...`).

Published permeability (simulations.ods, sheet "2.2 Overview" and "Details"; mD):

| Image | Sub-volume | Porosity | EJ Stokes (Fraunhofer, GeoDict) | LBM (Kongju) | Midrange ± ½range |
|---|---|---|---|---|---|
| Fontainebleau | full 288×288×300 | 0.147 | 1914 (x 1975, y 1693, z 2073) | 1503 (x 1556, y 1328, z 1624; porosity 14.5%) | 1708 ± 12.0% |
| Berea (VSG) | 400^3 at x,y 151–550, z 126–525 | 0.184 | 124 | 113 | 118 ± 4.3% |
| Berea (VSG) | 724×724×1024 (Fraunhofer: 720×720×1024) | 0.184 | 139 | 109 | 124 ± 12.2% |
| Grosmont carbonate (VSG) | 400^3 at x,y 1–400, z 551–950 | 0.247 | 512 | 353 | 433 ± 18.3% |
| Grosmont carbonate (VSG) | 1024^3 | 0.247 | 1706 | 773 | 1239 ± 37.6% |
| Sphere pack | 788×791×793 | 0.343 | 270220 | 221587 | 245903 ± 9.9% |

Segmentation porosity spread ("1.1 Porosity"): Berea KJ 0.195, SU 0.209, VSG 0.184. Carbonate KJ 0.195, SU 0.271, VSG 0.247. This illustrates how much the choice of segmentation alone changes the result.
Checksum: to fill at download.

---

## Corrections to CLAUDE.md

1. **Segmentation of DRP-317 is IsoData, not Otsu + watershed.** It is a single global threshold per sample, computed by IsoData (Ridler & Calvard 1978) on the contrast-enhanced, non-local-means-filtered 8-bit image. The thresholds are listed above. "Watershed" appears only in Neumann et al.'s PNM extraction (PoreSpy SNOW). No opened source supports Otsu for DRP-317.
2. **The DRP-317 binary volumes include isolated pores.** Neumann et al. removed non-percolating pore voxels before computing µCT porosity and permeability. To compare with their numbers, keep only the percolating cluster.
3. **Digital Rocks Portal has moved.** `digitalrocksportal.org` now redirects to a tombstone page. The DOI resolves to `digitalporousmedia.org` (Digital Porous Media Portal, TACC), which blocks automated access. The files are publicly downloadable per file from TACC Web Corral (`https://web.corral.tacc.utexas.edu/digitalporousmedia/DRP-317/`).
4. **DRP-317 licence is ODC-BY 1.0.** Attribution is required. Commercial use and derivatives are allowed.
5. **DRP-317 size:** each volume is 953.6M (1000^3 uint8). All 33 volumes come to 30.7 GiB, and the one-click archive is 22.9G. Both are **over the 20 GB hard stop**. The 11 binary volumes alone are 10.2 GiB, which is under it.
6. Sample count (11), 1000^3 voxels, 2.25 µm voxel size, scanner (SkyScan 1272) and lab permeability range (9 to 386 mD) are **confirmed**. The "connected porosity 14–27%" in the brief is the paper's µCT connected porosity. The *lab* porosity range is 14.77% to 26.54%, and the µCT connected range is 13.00% to 26.56% (Suppl. Table S2). Minor lab-value discrepancy between arXiv Suppl. S2 and Sci. Rep. Table 1: BUG 85 vs 86 mD, Buff Berea 274 vs 275 mD. Use the Sci. Rep. values as the published record.
7. **Acquisition kV/µA conflict:** 50 kV / 200 µA (DRP metadata, Neumann arXiv) versus 100 kV / 100 µA (Data in Brief). Unresolved. Not important for us.
8. **Lab-to-image scale and REV:** Neumann et al. show that simulated k on Berea reaches the lab value only at the full 1000^3 cube. The 256^3 and 400^3 crops in Phase 1 must use a full-cube or same-crop simulated reference k, **not** lab k.
9. **IBM dataset licence is CDLA-Sharing-1.0, not CC BY** (the paper is CC BY 4.0, the data is not). The total is 1.53 TB, so it is far over 20 GB. Only the binary ROI cubes (85 to 603 MB compressed each, 2500^3) are practical. The GitHub repo `IBM/microCT-Dataset` now returns 404. Lab k range: 0.31 mD (Klinkenberg, 15A "Bentheimer", suspect) to 5000 mD. The voxel size is 2.25 µm, the same as DRP-317.
10. **Imperial College images:** the 2015 set is 1000^3 (not "roughly 300^3–400^3 crops"), with voxels of 2.69 to 3.31 µm, hosted on Box with no stated licence. The 2007 set is on figshare under CC BY 4.0 (Berea: 3.69 MB 7z). The published 2015 DNS permeabilities (Raeini et al. 2017) are above, so the images are no longer "image-based only, no values".
11. **MRCCM is downloadable** (DRP-362, ODC-BY 1.0, 99.3G archive, per-file access). LR is 10.72 µm and HR 2.68 µm (4×). The segmentation is 3-phase (macropore / grain / microporosity) by Avizo watershed + hysteresis.
12. DRP-215 / DRP-211 are ODC-BY 1.0, 14.6G / 6.6G, greyscale-only with synthetic downsampling and no segmentation. Not useful for flow-based scoring.

## Recommended first download for Phase 2

**Step 1 (pipeline check, about 1 MB):** Andrä et al. Fontainebleau segmented image.
`https://raw.githubusercontent.com/fkrzikalla/drp-benchmarks/master/images/fontainebleau/segmented-exxon.raw.gz`
1,090,208 bytes. uint8 288×288×300, 7.5 µm. Published porosity 0.147. Published permeability: EJ Stokes 1914 mD and LBM 1503 mD (full image, mean of x, y, z), with per-axis values above. A Stokes/LBM run on 288×288×300 fits easily inside the 1-hour local cap. If our solver lands within or near 1503 to 1914 mD, the flow pipeline works. Caveat: no licence, so do not commit or re-host the file.

**Step 2 (first DRP-317 volume, 953.6M, below the 20 GB stop):** Berea segmented volume.
`https://web.corral.tacc.utexas.edu/digitalporousmedia/DRP-317/Berea/Berea_2d25um_binary.raw/Berea_2d25um_binary.raw`
uint8 little-endian 1000^3, 0 = pore, 2.25 µm. Published values: lab 121 mD, lab porosity 18.96%, µCT connected porosity 21.43%. Neumann et al. full-cube network k: PNM 186, RMB 106, CNM 102 mD. Andrä et al. independently studied a different Berea at about 109 to 139 mD. Berea is also the sample with Neumann's REV curve. Alternative low-porosity, near-percolation case for later: Parker (`.../DRP-317/Parker/Parker_2d25um_binary.raw/Parker_2d25um_binary.raw`, 953.6M, lab 10 mD, PNM 13 / RMB 8 / CNM 11 mD).
