"""Synthetic low-resolution inputs and consistent label resampling.

Procedure (fixed in docs/prereg.md):
  1. blur the high-resolution greyscale with a Gaussian of sigma = blur_sigma * factor
     (in high-resolution voxels), standing in for the coarser point-spread function;
  2. downsample by `factor` with block averaging (each coarse voxel = mean of
     factor^3 fine voxels, i.e. ideal integrating detector);
  3. add zero-mean Gaussian noise with standard deviation noise_frac * (grey-level
     difference between the pore and grain modes of the input).

Label resampling: the reference mask must be brought to the coarse grid too. Each method
below can itself open or close throats, so `label_resampling_check` measures what each
does to topology, throat count and permeability of the label alone.
"""
from __future__ import annotations

import numpy as np
from scipy import ndimage as ndi


def _crop_to_multiple(a, factor):
    sl = tuple(slice(0, (s // factor) * factor) for s in a.shape)
    return a[sl]


def block_mean(a, factor):
    a = _crop_to_multiple(np.asarray(a, float), factor)
    s = a.shape
    return a.reshape(s[0] // factor, factor, s[1] // factor, factor, s[2] // factor, factor).mean((1, 3, 5))


def phase_contrast(grey, mask):
    """Difference between median grain and median pore grey value."""
    grey = np.asarray(grey, float)
    return float(np.median(grey[~mask]) - np.median(grey[mask]))


def degrade(grey, factor, blur_sigma=0.5, noise_frac=0.05, contrast=None, seed=0):
    """Blur, block-downsample and add noise. Returns float32 coarse greyscale.

    contrast: grey-level pore/grain contrast used to scale noise (see phase_contrast);
    if None the input standard deviation is used.
    """
    g = np.asarray(grey, np.float32)
    if factor > 1 and blur_sigma > 0:
        g = ndi.gaussian_filter(g, blur_sigma * factor)
    g = block_mean(g, factor) if factor > 1 else g.astype(float)
    scale = float(np.std(grey)) if contrast is None else float(contrast)
    rng = np.random.default_rng(seed)
    if noise_frac > 0:
        g = g + rng.normal(0, noise_frac * scale, g.shape)
    return g.astype(np.float32)


LABEL_METHODS = ("majority", "majority_tie_pore", "porosity_matched", "subsample", "any", "all")


def resample_label(mask, factor, method="majority"):
    """Bring a fine pore mask to the coarse grid.

    majority  : coarse voxel is pore if > 50 % of its fine voxels are pore (ties go to
                grain, which biases towards closing throats);
    majority_tie_pore : pore if >= 50 % of its fine voxels are pore (ties go to pore);
    porosity_matched  : rank coarse voxels by pore fraction (ties broken by a lightly
                smoothed fraction, sigma = factor/2 fine voxels) and label the top ones pore
                so the coarse porosity equals the fine porosity;
    subsample : take one fine voxel per block (nearest neighbour; aliasing-prone);
    any       : pore if any fine voxel is pore (liberal: opens throats);
    all       : pore only if all fine voxels are pore (conservative: closes throats).
    """
    m = np.asarray(mask, bool)
    if factor == 1:
        return m.copy()
    if method == "subsample":
        o = factor // 2
        return _crop_to_multiple(m, factor)[o::factor, o::factor, o::factor].copy()
    frac = block_mean(m, factor)
    if method == "majority":
        return frac > 0.5
    if method == "majority_tie_pore":
        return frac >= 0.5
    if method == "porosity_matched":
        target = _crop_to_multiple(m, factor).mean()
        smooth = block_mean(ndi.gaussian_filter(m.astype(np.float32), factor / 2), factor)
        score = frac + 1e-3 * smooth  # smooth term only reorders blocks with equal frac
        n_pore = int(round(target * score.size))
        out = np.zeros(score.size, bool)
        out[np.argsort(-score, axis=None, kind="stable")[:n_pore]] = True
        return out.reshape(score.shape)
    if method == "any":
        return frac > 0
    if method == "all":
        return frac >= 1.0
    raise ValueError(method)


def label_resampling_check(mask, factor, voxel_size, methods=LABEL_METHODS, flow_axis=0,
                           with_network=True, with_flow=True, lbm_kw=None):
    """For each method: Betti numbers, throat count and permeability of the resampled
    label alone, against the fine-grid label. Returns a list of dicts (one per method,
    plus the reference first)."""
    from . import flow, metrics, network

    lbm_kw = lbm_kw or {}

    def describe(m, vs, name):
        b0, b1, b2 = metrics.betti_numbers(m)
        vol_mm3 = m.size * (vs * 1e3) ** 3
        row = dict(method=name, factor=vs / voxel_size, porosity=float(m.mean()),
                   b0=b0, b1=b1, b2=b2, b1_density=b1 / vol_mm3, chi_density=(b0 - b1 + b2) / vol_mm3)
        if with_network:
            row["n_throats"] = network.throat_count(network.extract(m, voxel_size=vs))
            row["throat_density"] = row["n_throats"] / vol_mm3
        if with_flow:
            r = flow.lbm_permeability(m, axis=flow_axis, voxel_size=vs, **lbm_kw)
            row["k_mD"] = r["k_mD"]
            row["lbm_converged"] = r["converged"]
        return row

    rows = [describe(_crop_to_multiple(np.asarray(mask, bool), factor), voxel_size, "reference")]
    for meth in methods:
        rows.append(describe(resample_label(mask, factor, meth), voxel_size * factor, meth))
    ref = rows[0]
    for r in rows[1:]:
        for k in ("b1_density", "chi_density", "throat_density", "k_mD", "porosity"):
            if k in r and k in ref and ref[k]:
                r[f"{k}_rel_change"] = (r[k] - ref[k]) / abs(ref[k])
    return rows


def erode_to_porosity(mask, target, max_iter=50):
    """Erode the pore phase one voxel layer at a time (6-connected structuring element)
    and return the last mask with porosity >= target, plus the number of layers. Used to
    push reference masks towards the percolation threshold."""
    m = np.asarray(mask, bool)
    s = ndi.generate_binary_structure(3, 1)
    for i in range(max_iter):
        nxt = ndi.binary_erosion(m, s, border_value=1)
        if nxt.mean() < target:
            return m, i
        m = nxt
    return m, max_iter
