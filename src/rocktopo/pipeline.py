"""End-to-end evaluation of one mask: permeability (LBM and PNM), network, topology.

Writes one results folder per run (CLAUDE.md section 3): config.json, metrics.json, log.txt.
Every number reported anywhere must come from these files.
"""
from __future__ import annotations

import json
import platform
import time
from pathlib import Path

import numpy as np

from . import flow, metrics, network


def _jsonable(x):
    if isinstance(x, dict):
        return {k: _jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_jsonable(v) for v in x]
    if isinstance(x, np.generic):
        return x.item()
    if isinstance(x, np.ndarray):
        return x.tolist()
    return x


def geometric_mean_k(ks):
    ks = np.asarray(ks, float)
    return float(np.exp(np.mean(np.log(ks)))) if (ks > 0).all() else 0.0


def evaluate_reference(mask, voxel_size, axes=(0, 1, 2), lbm_kw=None, with_pnm=True,
                       with_topology=True, log=print):
    """Characterise a reference mask. Returns (summary dict, network dict or None)."""
    lbm_kw = dict(lbm_kw or {})
    out = dict(shape=list(mask.shape), voxel_size=voxel_size, porosity=metrics.porosity(mask))
    span_any = np.zeros(mask.shape, bool)
    for a in axes:
        span_any |= flow.spanning_pores(mask, a)
    out["connected_porosity"] = float(span_any.mean())
    lbm = {}
    for a in axes:
        r = flow.lbm_permeability(mask, axis=a, voxel_size=voxel_size, **lbm_kw)
        r.pop("velocity", None)
        lbm[a] = r
        log(f"LBM axis {a}: k = {r['k_mD']:.4g} mD  ({r['how']}, {r['steps']} steps, "
            f"tail {r['tail']:.2%}, {r['seconds']:.0f} s)")
    out["lbm"] = {str(a): {k: v for k, v in r.items() if k != "history"} for a, r in lbm.items()}
    out["lbm_history"] = {str(a): r.get("history", []) for a, r in lbm.items()}
    out["k_lbm_mD_geomean"] = geometric_mean_k([lbm[a]["k_mD"] for a in axes])
    net = None
    if with_pnm:
        t = time.time()
        net = network.extract(mask, voxel_size=voxel_size)
        out["n_pores"] = int(len(net["pore.coords"]))
        out["n_throats"] = network.throat_count(net)
        out["snow2_seconds"] = time.time() - t
        pnm = {str(a): flow.pnm_permeability(net, mask.shape, axis=a, voxel_size=voxel_size) for a in axes}
        out["pnm"] = pnm
        out["k_pnm_mD_geomean"] = geometric_mean_k([pnm[str(a)]["k_mD"] for a in axes])
        if out["k_lbm_mD_geomean"]:
            out["pnm_over_lbm"] = out["k_pnm_mD_geomean"] / out["k_lbm_mD_geomean"]
        log(f"PNM: k = {out['k_pnm_mD_geomean']:.4g} mD (geo-mean), "
            f"{out['n_pores']} pores, {out['n_throats']} throats")
    if with_topology:
        out["topology"] = metrics.topology_summary(mask, voxel_size)
    return out, net


class Run:
    """A results/<name>/ folder with config, metrics and a log."""

    def __init__(self, name, config, root="results"):
        self.dir = Path(root) / name
        self.dir.mkdir(parents=True, exist_ok=True)
        cfg = dict(config, started=time.strftime("%Y-%m-%d %H:%M:%S"), host=platform.node(),
                   python=platform.python_version())
        (self.dir / "config.json").write_text(json.dumps(_jsonable(cfg), indent=2))
        self._log = open(self.dir / "log.txt", "a", encoding="utf-8")

    def log(self, msg):
        line = f"[{time.strftime('%H:%M:%S')}] {msg}"
        print(line, flush=True)
        self._log.write(line + "\n")
        self._log.flush()

    def save(self, metrics_dict, name="metrics.json"):
        (self.dir / name).write_text(json.dumps(_jsonable(metrics_dict), indent=2))
