# rock-topology

Which segmentation errors matter for permeability in digital rock?

A research project testing which segmentation metrics predict permeability error in rock
micro-CT, and whether topology-aware training losses reduce that error.

- `CLAUDE.md`: the standing brief for Claude Code. Read this first.
- `KICKOFF.md`: the one prompt to paste to start.
- `docs/gate0-review.md`: first literature review and draft novelty statement.
- `docs/novelty.md`, `docs/refs.bib`, `docs/lit/`: Phase 0 literature check (Gate 0 draft).
- `data/MANIFEST.md`, `docs/prereg.md`: Phase 1 data manifest and pre-registration (Gate 1 draft).
- `docs/gates/`: gate reports. `docs/lab-notebook.md`: dated log and gate approvals.
- `docs/glossary.md`: rock and topology terms in plain language.

## Status (2026-11-12)

Phases 0–2 are under way. Gates 0, 1 and 2 have not been approved. The Phase 2 code is
built and unit-tested on synthetic data. The Gate 2 benchmark reproduction is waiting on
the first data download.

## Setup

```
uv venv --python 3.12 .venv
uv pip install --python .venv/Scripts/python.exe -e .[dev]
uv pip install --python .venv/Scripts/python.exe torch --index-url https://download.pytorch.org/whl/cpu
.venv/Scripts/python.exe -m pytest -q            # all tests; add -m "not slow" for the quick ones
```

## Code (`src/rocktopo/`)

| Module | What it does |
|---|---|
| `io` | read headerless raw / tif volumes, crop, checksum |
| `metrics` | primary tier: Dice, porosity error, Euler and Betti errors (6-connected pore), clDice, one-to-one throat matching |
| `network` | SNOW2 pore-network extraction (PoreSpy), inlet/outlet pores per axis |
| `flow` | voxel permeability by D3Q19 TRT lattice-Boltzmann (torch, CPU or GPU); PNM permeability (OpenPNM); grid refinement |
| `degrade` | blur + downsample + noise; label resampling methods and the resampling check; erosion towards percolation |
| `segment` | Otsu, IsoData and watershed baselines |
| `pipeline` | evaluate a reference mask; results folder with config, metrics and log |

Analysis scripts in `analysis/` write to `results/<run>/`, one flow axis or crop per call,
so every local job stays under the 1-hour cap.
"# rock-topology" 
