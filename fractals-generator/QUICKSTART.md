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
