"""Analytic checks of the voxel flow solver and the pore-network solver."""
import numpy as np
import pytest

from rocktopo.flow import grid_refinement, lbm_permeability, pnm_permeability, refine, spanning_pores


def plates(h, Lx, nz=8, ny=4):
    m = np.zeros((nz, ny, Lx), bool)
    m[:, :, 1:1 + h] = True
    return m


@pytest.mark.parametrize("h", [4, 10, 20])
def test_parallel_plates_exact_profile(h):
    """Channel of gap h between plates, periodic sideways. The TRT solver with Lambda=3/16
    reproduces the parabolic profile exactly at the nodes, so the voxel-summed flux equals
    the midpoint-rule sum of the parabola: k = (h^3 + h/2) / (12 Lx)."""
    Lx = h + 2
    r = lbm_permeability(plates(h, Lx), axis=0, side_walls=False, mode="periodic", nu=0.5, tol=1e-9, dtype="float64")
    assert r["converged"]
    k_discrete = (h ** 3 + h / 2) / (12 * Lx)
    assert r["k_vox2"] == pytest.approx(k_discrete, rel=1e-6)
    # and against the continuum value h^3 / (12 Lx): error is 1/(2 h^2)
    assert r["k_vox2"] == pytest.approx(h ** 3 / (12 * Lx), rel=0.6 / h ** 2)


def test_viscosity_independence():
    """With the magic parameter, permeability must not depend on the chosen viscosity."""
    m = np.zeros((6, 12, 12), bool)
    yy, xx = np.mgrid[:12, :12]
    m[:, (yy - 5.5) ** 2 + (xx - 5.5) ** 2 < 4.5 ** 2] = True
    ks = [lbm_permeability(m, axis=0, nu=nu, mode="periodic", tol=1e-9, dtype="float64")["k_vox2"] for nu in (1 / 6, 0.5, 1.0)]
    assert np.ptp(ks) / np.mean(ks) < 1e-6


def test_straight_tube_poiseuille():
    """Circular tube of radius R in an L x L cross-section: k = pi R^4 / (8 L^2).
    The voxelised circle has a staircase wall, so use the radius of equal area and
    allow 3 %."""
    R, L = 10.0, 24
    yy, xx = np.mgrid[:L, :L]
    disc = (yy - (L - 1) / 2) ** 2 + (xx - (L - 1) / 2) ** 2 < R ** 2
    m = np.repeat(disc[None], 6, axis=0)
    r = lbm_permeability(m, axis=0, nu=0.5, mode="periodic", tol=1e-9)
    R_eq = np.sqrt(disc.sum() / np.pi)
    k_theory = np.pi * R_eq ** 4 / (8 * L ** 2)
    assert r["k_vox2"] == pytest.approx(k_theory, rel=0.03)


def test_axis_and_units():
    """Same tube along each axis gives the same k; units scale with voxel_size^2."""
    R, L = 6.0, 16
    yy, xx = np.mgrid[:L, :L]
    disc = (yy - 7.5) ** 2 + (xx - 7.5) ** 2 < R ** 2
    m0 = np.repeat(disc[None], 8, axis=0)
    k0 = lbm_permeability(m0, axis=0, nu=0.5, mode="periodic", tol=1e-9, dtype="float64")["k_vox2"]
    k1 = lbm_permeability(np.moveaxis(m0, 0, 1), axis=1, nu=0.5, mode="periodic", tol=1e-9, dtype="float64")["k_vox2"]
    k2 = lbm_permeability(np.moveaxis(m0, 0, 2), axis=2, nu=0.5, mode="periodic", tol=1e-9, dtype="float64")["k_vox2"]
    assert k1 == pytest.approx(k0, rel=1e-6) and k2 == pytest.approx(k0, rel=1e-6)
    r = lbm_permeability(m0, axis=0, nu=0.5, mode="periodic", tol=1e-9, dtype="float64", voxel_size=2e-6)
    assert r["k_m2"] == pytest.approx(k0 * 4e-12, rel=1e-9)


def test_non_percolating_is_zero():
    m = np.zeros((10, 10, 10), bool)
    m[2:5, 2:8, 2:8] = True  # does not touch inlet/outlet
    r = lbm_permeability(m, axis=0)
    assert r["k_vox2"] == 0.0 and not r["percolates"]


def test_dead_end_removed():
    m = np.zeros((10, 10, 10), bool)
    m[:, 4:6, 4:6] = True
    span = spanning_pores(m, 0)
    m2 = m.copy()
    m2[3:6, 0:2, 0:2] = True  # isolated blob
    assert (spanning_pores(m2, 0) == span).all()


def test_grid_refinement_converges():
    """Refining the lattice of a fixed (staircase) geometry: k converges, each refinement
    changing it less than the previous one."""
    R, L = 3.0, 8
    yy, xx = np.mgrid[:L, :L]
    disc = (yy - 3.5) ** 2 + (xx - 3.5) ** 2 < R ** 2
    m = np.repeat(disc[None], 2, axis=0)
    rows, rel = grid_refinement(m, axis=0, voxel_size=1.0, factors=(1, 2, 4), nu=0.5,
                                mode="periodic", tol=1e-8)
    k = [r["k_m2"] for r in rows]
    assert abs(k[2] - k[1]) < abs(k[1] - k[0])
    assert rel < 0.05
    assert refine(m, 2).shape == (4, 16, 16)


@pytest.mark.slow
def test_pnm_vs_lbm_same_order():
    """Pore network and voxel solver on a synthetic porous medium agree within a factor
    of 3 (PNM is an approximation; the actual disagreement is reported, not tuned)."""
    import porespy as ps

    from rocktopo.network import extract

    im = ps.generators.blobs(shape=[64, 64, 64], porosity=0.35, blobiness=1, seed=1)
    kl = lbm_permeability(im, axis=0, voxel_size=1e-6, nu=0.5, tol=1e-6)["k_m2"]
    net = extract(im, voxel_size=1e-6)
    kp = pnm_permeability(net, im.shape, axis=0, voxel_size=1e-6)["k_m2"]
    assert kl > 0 and kp > 0
    assert 1 / 3 < kp / kl < 3
