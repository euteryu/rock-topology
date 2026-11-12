# The one prompt

Put `rock-topology.zip` in an empty folder, open Claude Code in that folder, and paste:

```
Unzip rock-topology.zip here, cd into rock-topology, and run git init if it is not
already a repository. Then read README.md, CLAUDE.md, docs/gate0-review.md and
docs/lab-notebook.md in full. CLAUDE.md is your standing brief: follow it exactly,
including its hard stops and its rule of no local job over 1 hour.

Work through Phases 0, 1 and 2 on your own, in parallel where that makes sense:

- Phase 0: finish the literature check (the papers the first review could not open, plus
  a fresh search), and write docs/novelty.md and docs/refs.bib.
- Phase 1: verify each dataset's URL, licence and size, write data/MANIFEST.md, and draft
  docs/prereg.md.
- Phase 2: build and unit-test the CPU pipeline and the primary-tier metrics.

Work out for yourself what tools and packages you need and install them. I am new to
rock physics, so explain rock terms the first time you use them and keep
docs/glossary.md up to date. Make the sensible choice when something is unclear, note
the choice in docs/lab-notebook.md, and keep going.

Only stop and ask me at the hard stops listed in CLAUDE.md. When you do stop, or when
Phases 0 to 2 are finished, give me a short plain-English summary: what you did, what
you found, what you need from me, and what happens next.
```

## What you will be asked for along the way

- A go-ahead if the dataset download is over 20 GB.
- A Kaggle API token, saved as `~/.kaggle/kaggle.json` (Kaggle account settings →
  "Create New Token"), once heavy runs are needed.
- Your approval of `docs/novelty.md` before any GPU training.
- Any paywalled paper the CLI could not open.
