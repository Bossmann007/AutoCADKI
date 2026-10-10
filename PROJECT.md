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

## Project inputs (from the owner, 2026-10-10)

- Tank: circular section, inner diameter 2190 mm, straight length 12,400 mm, shell 3 mm, heads 4 mm,
  torispherical "ASME 10" heads (ASSUMED: crown R = Di, knuckle r = 0.10 Di; to confirm), 3 baffles (positions TBD).
- Trailer: 4 axles, spacings 2450 / 1250 / 1250 mm; kingpin 750 mm from the front (reference to confirm);
  loads: kingpin 12,500 kg, axle 1 = 10,000 kg, axles 2-4 = 25,500 kg together (spoken "33.500" then corrected to 35.500 total).
- Axle positions are computed by moment balance about the kingpin. CG is ASSUMED at 5,030 mm from the kingpin, taken from a reference study the owner supplied only as a basis (Pastre 45,000 L, 4E chassis, 10/2015; reference E1 at 4,540 mm from kingpin, kingpin 13.5 t). The engineer replaces it with the real CG.
- Baffles go at the suspension supports (stiffness), so their positions follow the axle positions.

## Known issues

- 

## Current work

See `.claude/state/checkpoint.json` for live task state.
