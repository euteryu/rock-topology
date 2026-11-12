"""Primary-tier metrics on shapes with known answers."""
import numpy as np
import pytest

from rocktopo import metrics as M


def ball(n, r, c=None):
    c = (n - 1) / 2 if c is None else c
    z, y, x = np.mgrid[:n, :n, :n]
    return (z - c) ** 2 + (y - c) ** 2 + (x - c) ** 2 <= r ** 2


def solid_torus(n=40, R=12, r=4):
    z, y, x = np.mgrid[:n, :n, :n] - (n - 1) / 2
    return (np.sqrt(x ** 2 + y ** 2) - R) ** 2 + z ** 2 <= r ** 2


# ---------------- Euler / Betti
def test_single_voxel():
    m = np.zeros((3, 3, 3), bool)
    m[1, 1, 1] = True
    assert M.euler_number(m) == 1
    assert M.betti_numbers(m) == (1, 0, 0)


def test_two_balls():
    m = ball(30, 5, c=7) | ball(30, 5, c=22)
    assert M.betti_numbers(m) == (2, 0, 0)
    assert M.euler_number(m) == 2


def test_torus_has_one_loop():
    t = solid_torus()
    assert M.euler_number(t) == 0
    assert M.betti_numbers(t) == (1, 1, 0)


def test_hollow_ball_has_cavity():
    m = ball(30, 12) & ~ball(30, 6)
    assert M.betti_numbers(m) == (1, 0, 1)
    assert M.euler_number(m) == 2


def test_six_connectivity():
    """Two voxels touching only along an edge are two pore clusters (no face to flow through)."""
    m = np.zeros((4, 4, 4), bool)
    m[1, 1, 1] = m[1, 2, 2] = True
    assert M.betti_numbers(m)[0] == 2
    assert M.euler_number(m) == 2


def test_euler_matches_skimage():
    from skimage.measure import euler_number

    rng = np.random.default_rng(0)
    from scipy import ndimage as ndi

    m = ndi.gaussian_filter(rng.random((40, 40, 40)), 2) > 0.5
    assert M.euler_number(m) == euler_number(m, connectivity=1)


def test_frame_has_loops():
    """A cubic wire frame (12 edges, 8 corners) has b1 = 5."""
    m = np.zeros((12, 12, 12), bool)
    for a in (1, 10):
        for b in (1, 10):
            m[1:11, a, b] = m[a, 1:11, b] = m[a, b, 1:11] = True
    assert M.betti_numbers(m) == (1, 5, 0)


def test_topology_errors_densities():
    t = solid_torus()
    e = M.topology_errors(t | ball(40, 3, c=3), t, voxel_size=1e-6)
    assert e["b0_diff"] == 1 and e["b1_diff"] == 0
    assert e["b0_density_diff"] == pytest.approx(1 / (40 ** 3 * 1e-9))


# ---------------- overlap
def test_dice_iou():
    a = np.zeros((10, 10, 10), bool)
    b = a.copy()
    a[:5] = True
    b[:4] = True
    assert M.dice(a, b) == pytest.approx(2 * 400 / 900)
    assert M.iou(a, b) == pytest.approx(400 / 500)
    assert M.dice(a, a) == 1.0


def test_porosity_error_sign():
    a = np.zeros((10, 10, 10), bool)
    b = a.copy()
    a[:5] = True
    b[:4] = True
    assert M.porosity_error(a, b) == pytest.approx(0.1)


# ---------------- clDice
def test_cldice_perfect_and_broken():
    m = np.zeros((40, 9, 9), bool)
    m[:, 3:6, 3:6] = True
    assert M.cldice(m, m)["cldice"] == pytest.approx(1.0)
    broken = m.copy()
    broken[18:22] = False  # cut the tube: Dice barely moves, clDice drops
    d = M.dice(broken, m)
    c = M.cldice(broken, m)
    assert c["tprec"] == pytest.approx(1.0)
    assert c["tsens"] < 1.0
    assert c["cldice"] < 1.0 and d > 0.9


# ---------------- throat matching
def test_match_throats_identical():
    xyz = np.array([[0, 0, 0], [10, 0, 0], [0, 10, 0]], float)
    r = np.array([1.0, 2.0, 3.0])
    out = M.match_throats(xyz, r, xyz, r)
    assert out["n_matched"] == 3 and out["n_missed"] == 0 and out["n_false"] == 0
    assert out["radius_rel_err"] == 0 and out["throat_f1"] == 1


def test_match_throats_missed_false_radius():
    ref = np.array([[0, 0, 0], [10, 0, 0], [20, 0, 0]], float)
    rr = np.array([2.0, 2.0, 2.0])
    pred = np.array([[0.5, 0, 0], [20, 1, 0], [50, 50, 50]], float)
    pr = np.array([1.0, 2.0, 2.0])
    out = M.match_throats(ref, rr, pred, pr)
    assert out["n_matched"] == 2 and out["n_missed"] == 1 and out["n_false"] == 1
    assert out["radius_rel_err"] == pytest.approx(0.25)  # (0.5 + 0) / 2
    assert out["radius_rel_bias"] == pytest.approx(-0.25)


def test_match_is_one_to_one_and_optimal():
    """Two pred throats near one ref throat: only one may match; the closer one wins."""
    ref = np.array([[0, 0, 0], [3, 0, 0]], float)
    rr = np.array([2.0, 2.0])
    pred = np.array([[1.8, 0, 0], [0.2, 0, 0]], float)
    out = M.match_throats(ref, rr, pred, rr)
    assert out["n_matched"] == 2
    assert sorted(map(tuple, out["pairs"])) == [(0, 1), (1, 0)]


def test_throat_errors_on_networks():
    import porespy as ps

    from rocktopo.network import extract

    im = ps.generators.blobs(shape=[48, 48, 48], porosity=0.35, blobiness=1, seed=2)
    n = extract(im, voxel_size=2e-6)
    e = M.throat_errors(n, n)
    assert e["n_missed"] == 0 and e["n_false"] == 0 and e["throat_f1"] == 1.0
    from scipy import ndimage as ndi

    er = ndi.binary_erosion(im, iterations=1)
    e2 = M.throat_errors(extract(er, voxel_size=2e-6), n)
    assert e2["radius_rel_bias"] < 0  # erosion narrows throats
    assert e2["n_missed"] > 0


def test_primary_metrics_runs():
    t = solid_torus()
    out = M.primary_metrics(t, t)
    assert out["dice"] == 1 and out["chi_diff"] == 0 and out["cldice"] == pytest.approx(1.0)
