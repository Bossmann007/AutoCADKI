# PROJECT.md

Project brain — semi-static. Update when stack or architecture changes.

## Goal

Create 2D and 3D drawings of trailers (carretas) and their parts using AI.
Phase 1 is research: what approaches/tools exist (text-to-CAD, parametric CAD
generation via LLM code, DXF/DWG output for AutoCAD, 3D mesh/STEP generation),
what is feasible, and what output formats a trailer shop needs.

## Stack

- Language: TBD (decided after research)
- Framework: TBD
- Package manager: TBD

## Commands

```bash
# install
# test
# run
```

## Architecture

TBD after research. Findings go in `docs/research/`.

## Conventions

- Research notes: Markdown in `docs/research/`, primary sources, dated

## Decisions

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-10-10 | Research before building | User request at setup |
| 2026-10-10 | MVP target: tank trailer (carreta tanque) | User choice |
| 2026-10-10 | Deliverable format includes DWG (not only DXF) | User requirement; see docs/research/ai-cad-trailers.md §5 |

## Known issues

- 

## Current work

See `.claude/state/checkpoint.json` for live task state.
