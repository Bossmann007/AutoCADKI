# PROJECT.md

Project brain — semi-static. Update when stack or architecture changes.

## Goal

Create 2D and 3D drawings of trailers (carretas) and their parts using AI.
Phase 1 is research: what approaches/tools exist (text-to-CAD, parametric CAD
generation via LLM code, DXF/DWG output for AutoCAD, 3D mesh/STEP generation),
what is feasible, and what output formats a trailer shop needs.

## Stack

- Language: Python 3.12
- Framework: CadQuery 2.x (OCCT B-rep), pytest
- Package manager: uv (`.venv/`, git-ignored)

## Commands

```bash
uv venv --python 3.12 .venv && uv pip install --python .venv/bin/python cadquery pytest
.venv/bin/python -m pytest -q
mkdir -p out && .venv/bin/python -m src.tank_shell   # writes out/tank_shell.step
```

## Architecture

Research in `docs/research/`. `src/tank_shell.py`: parametric tank shell (oval section + half-ellipsoid heads, thickness as input). Next: nozzles/manholes, baffles, chassis, DXF drawings. All dimensions are placeholders until the reviewing engineer sets them.

## Conventions

- Research notes: Markdown in `docs/research/`, primary sources, dated

## Decisions

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-10-10 | Research before building | User request at setup |
| 2026-10-10 | MVP target: tank trailer (carreta tanque) | User choice |
| 2026-10-10 | Shell thickness is an input, not computed from Anexo H | Tables depend on cargo group, density, l/cm, L; engineer reviews at the end |
| 2026-10-10 | Deliverable format includes DWG (not only DXF) | User requirement; see docs/research/ai-cad-trailers.md §5 |

## Known issues

- 

## Current work

See `.claude/state/checkpoint.json` for live task state.
