import numpy as np
import pytest
from scipy import ndimage as ndi

from rocktopo import degrade as D
from rocktopo import segment as S


def synthetic_grey(seed=0, n=48):
    """Two-phase volume with known mask: pore grey 60, grain 180, blurred + noise."""
    rng = np.random.default_rng(seed)
    mask = ndi.gaussian_filter(rng.random((n, n, n)), 2.5) > 0.5
    grey = np.where(mask, 60.0, 180.0)
    grey = ndi.gaussian_filter(grey, 0.8) + rng.normal(0, 8, grey.shape)
    return grey, mask


def test_block_mean_and_shapes():
    a = np.arange(64, dtype=float).reshape(4, 4, 4)
    b = D.block_mean(a, 2)
    assert b.shape == (2, 2, 2)
    assert b[0, 0, 0] == pytest.approx(a[:2, :2, :2].mean())
    g, m = synthetic_grey()
    assert D.degrade(g, 2).shape == (24, 24, 24)
    assert D.degrade(g, 4).shape == (12, 12, 12)


def test_degrade_reproducible_and_noise_scale():
    g, m = synthetic_grey()
    a = D.degrade(g, 2, noise_frac=0.1, contrast=120, seed=3)
    b = D.degrade(g, 2, noise_frac=0.1, contrast=120, seed=3)
    assert np.array_equal(a, b)
    c = D.degrade(g, 2, noise_frac=0.0, seed=3)
    assert np.std(a - c) == pytest.approx(12, rel=0.1)


def test_resample_label_methods_ordering():
    _, m = synthetic_grey()
    por = {k: D.resample_label(m, 2, k).mean() for k in D.LABEL_METHODS}
    assert por["all"] <= por["majority"] <= por["majority_tie_pore"] <= por["any"]
    assert abs(por["porosity_matched"] - m.mean()) < 0.02


def test_baselines_recover_mask():
    g, m = synthetic_grey()
    for name, fn in S.BASELINES.items():
        p = fn(g)
        assert p.dtype == bool
        dice = 2 * (p & m).sum() / (p.sum() + m.sum())
        assert dice > 0.95, name


def test_erode_to_porosity():
    _, m = synthetic_grey()
    one = ndi.binary_erosion(m, ndi.generate_binary_structure(3, 1), border_value=1).mean()
    e, n = D.erode_to_porosity(m, one * 0.99)
    assert n == 1 and e.mean() == pytest.approx(one)
