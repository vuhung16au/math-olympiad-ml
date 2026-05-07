# HSC-Viewer-MathJax PRD

## Goal

Build a standalone Next.js viewer that converts sibling `HSC-xxx` LaTeX booklets into web-readable HTML while keeping `.tex` as the single source of truth.

## Core decisions

- Stack: Vercel, Next.js, bun, MathJax, make4ht, TypeScript
- HTML is generated into `.generated/`
- `make` is the main workflow interface
- No edits to existing booklet `.tex` files
- UI stays close to `HSC-Viewer`

## Main workflows

- `make generate`: rebuild all booklet HTML
- `make generate-one BOOKLET=...`: rebuild one booklet
- `make watch`: watch `.tex` and shared style changes
- `make dev`: generate then start local app
- `make build`: generate then run production build
- `make deploy`: alias to Vercel production deploy

## Reader shape

- Left sidebar for booklet selection
- Right pane for generated booklet content
- No PDF controller
- No page navigator
- Same HSC color system

## Notes

- Conversion uses `make4ht`, then sanitizes and rewrites output.
- Generated assets are served through a Next.js route.
- Docs under `docs/` are intentionally short and task-oriented.
