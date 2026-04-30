# Quickstart

## Prerequisites

- Node.js 18+
- npm 9+

## 1) Install

```bash
npm install
```

## 2) Run Web App (Next.js)

```bash
npm run dev
```

Open:

```text
http://127.0.0.1:3000
```

This is the primary interactive fractal UI for:

- `ifs`
- `lsystem`
- `escapeTime`
- `newton`
- `attractor`
- `inversion`

## 3) Package Build (publishable core)

```bash
npm run build
```

Outputs:

- `lib/` (CommonJS + typings)
- `esm/` (ESM)

## 4) Web Build / Start

```bash
npm run build:web
npm run start
```

## 5) Playwright Sweep

```bash
npm run test:fractals:playwright
```

What it does:

- starts Next.js dev server on `127.0.0.1:3000`
- iterates all fractal type + preset combinations
- captures screenshots and parameter trials
- writes outputs to `artifacts-playwright/` and `artifacts-playwright/index.json`

## 6) Artifact Generation Script

```bash
node scripts/generate-all-fractals.js
```

Generates static fractal assets and summary index in `artifacts/`.

## 7) TeX / TikZ export (CLI)

Export TikZ and/or standalone LaTeX for presets (same engine as the web/API):

```bash
npm run export:tex
```

Default: writes one default preset per family under `artifacts/tex/`. See [docs/CLI.md](docs/CLI.md) for `--family`, `--preset`, `--format`, `--param`, etc.

## 8) TeX / TikZ export (web & API)

- In the running app (`npm run dev`), use the **TikZ** and **TeX** buttons on the viewer to download `.tikz` / `.tex` from the current fractal and form settings.
- Or call the v1 route directly, for example:

```text
GET /api/v1/ifs/fern?format=tikz&width=980&height=760
GET /api/v1/escape-time/mandelbrot?format=tex&width=640&height=480&texMaxDim=256
```
