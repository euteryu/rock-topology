"""Classical segmentation baselines (pores are dark in micro-CT: low X-ray attenuation).

All return a bool mask with True = pore.
"""
from __future__ import annotations

import numpy as np
from scipy import ndimage as ndi


def otsu(grey):
    from skimage.filters import threshold_otsu

    return np.asarray(grey) < threshold_otsu(np.asarray(grey))


def isodata(grey):
    from skimage.filters import threshold_isodata

    return np.asarray(grey) < threshold_isodata(np.asarray(grey))


def watershed(grey, band=0.1):
    """Marker-based watershed on the gradient magnitude.

    Seeds: voxels clearly darker than the Otsu threshold are pore seeds, clearly brighter
    are grain seeds. "Clearly" = more than `band` x (grain mode - pore mode) away from the
    threshold. Uncertain voxels in between are assigned by flooding the Sobel gradient.
    """
    from skimage.filters import sobel, threshold_otsu
    from skimage.segmentation import watershed as ws

    g = np.asarray(grey, np.float32)
    t = threshold_otsu(g)
    lo, hi = np.median(g[g < t]), np.median(g[g >= t])
    d = band * (hi - lo)
    markers = np.zeros(g.shape, np.int32)
    markers[g < t - d] = 1
    markers[g > t + d] = 2
    lab = ws(sobel(g), markers)
    return lab == 1


BASELINES = {"otsu": otsu, "isodata": isodata, "watershed": watershed}
