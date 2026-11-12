# Gate 1 report: data manifest and pre-registration (2026-11-12)

Report-and-continue gate. The owner approves `data/MANIFEST.md` and `docs/prereg.md` in
`docs/lab-notebook.md`. Approval is needed before any Phase 3 analysis.

## Five-line summary

1. DRP-317 (11 Sandstones) confirmed: 11 samples, 1000³ voxels, 2.25 µm, ODC-BY 1.0, per-file
   downloads from TACC (the old Digital Rocks Portal has moved).
2. Its reference segmentation is a single IsoData threshold per sample (not Otsu + watershed);
   the masks keep isolated pores, so we filter to the connected pore space.
3. Size: the 11 segmented volumes are 10.2 GiB (OK); all 33 volumes are 30.7 GiB (**over the
   20 GB stop**). Downloading the filtered greyscale too (needed for degradation and
   baselines) makes 20.5 GiB, also over the stop, so it needs your go-ahead.
4. Lab permeability is valid only for full 1000³ cubes, so crops use simulated reference k.
5. `docs/prereg.md` is drafted: outcome log10(k_pred/k_ref) from the LBM; nine primary metrics;
   Spearman and partial Spearman, joint regression and factorial model; bootstrap by rock
   sample; Holm correction; solver-error floor.

## Decisions for the owner

- **Download scope (hard stop b):** proposed: all 11 binary volumes plus all 11 filtered
  greyscale volumes = 22 × 953.6 MiB = 20.5 GiB (about 22.0 GB). The alternative that stays
  under 20 GB is all 11 binary volumes plus filtered greyscale for 8 samples (19 volumes,
  about 19.0 GB). The raw
  (unfiltered) greyscale volumes are not needed.
- **Test samples for Phase 4:** proposed rule: rank by lab porosity, test = ranks 2, 6, 10
  (prereg section 2). With the manifest's lab porosities this is Bandera Gray (18.10%),
  Kirby (19.95%) and Bandera Brown (24.11%); the lowest-porosity sample, Parker (14.77%),
  stays in training. Please confirm or change.
- Secondary datasets: IBM (CDLA-Sharing licence, 2500³ binary ROI cubes only) and MRCCM
  (real paired low/high resolution, 3-phase labels) are both usable; neither is downloaded.
