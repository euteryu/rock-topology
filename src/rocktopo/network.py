"""Pore-network extraction with PoreSpy SNOW2.

A pore network model (PNM) reduces the pore space to a graph: pore bodies are nodes and
the narrow throats joining them are edges. SNOW2 (PoreSpy; primary references to be
opened and added to docs/refs.bib before citing) finds pore bodies as watershed regions of the distance transform; a throat is the
shared face between two regions.

Units: coordinates and sizes in the returned dict are in metres if voxel_size is given
(PoreSpy convention), with 'param.voxel_size' stored so callers can convert to voxels.
"""
from __future__ import annotations

import time

import numpy as np


def extract(mask, voxel_size=1.0, sigma=0.4, r_max=4):
    """Run SNOW2 on a pore mask and tag inlet/outlet pores on each pair of faces.

    Adds boolean arrays 'pore.inlet{a}' / 'pore.outlet{a}' for axes a = 0, 1, 2: pores
    whose region touches the first / last slice along that axis.
    """
    import porespy as ps

    t0 = time.time()
    m = np.asarray(mask, bool)
    snow = ps.networks.snow2(m, voxel_size=voxel_size, boundary_width=0, sigma=sigma, r_max=r_max)
    net = dict(snow.network)
    regions = snow.regions
    labels = np.asarray(net["pore.region_label"])
    Np = len(labels)
    lut = np.full(int(regions.max()) + 1, -1, np.int64)
    lut[labels] = np.arange(Np)
    for a in range(3):
        for name, sl in (("inlet", 0), ("outlet", -1)):
            face = np.unique(np.take(regions, sl, axis=a))
            face = face[(face > 0) & (face < len(lut))]
            idx = lut[face]
            flag = np.zeros(Np, bool)
            flag[idx[idx >= 0]] = True
            net[f"pore.{name}{a}"] = flag
    net["param.voxel_size"] = voxel_size
    net["param.shape"] = m.shape
    net["param.seconds"] = time.time() - t0
    return net


def throat_count(net):
    return int(len(net["throat.conns"]))


def size_distributions(net):
    """Pore and throat inscribed radii in voxels (for secondary-tier distribution metrics)."""
    vs = float(net["param.voxel_size"])
    return (np.asarray(net["pore.inscribed_diameter"]) / (2 * vs),
            np.asarray(net["throat.inscribed_diameter"]) / (2 * vs))
