# Script Rationalization

Status map for scripts during migration.

## keep

- `scripts/generate-all-fractals.js`
  - keeps static artifact generation for all families

## adapt

- `scripts/generate-all-fractals-playwright.js`
  - adapted from static HTML server flow to Next.js app flow

## adapt

- `scripts/generate-fractals-docs.js`
  - remains docs automation script (path/wording updates may be needed)

## deprecate

- static server startup instructions tied to `examples/canvas-ifs.html`
  - replaced by `npm run dev` Next.js flow
