# Fractals Generator

TypeScript fractal engine + Next.js web app.

This repository now supports two products:

- a publishable npm package (`IFS`, `LSystem`) from `src/`
- a Vercel-ready Next.js web app with six fractal families

## Fractal Families

- `ifs`
- `lsystem`
- `escapeTime`
- `newton`
- `attractor`
- `inversion`

## Local Development

Install dependencies:

```bash
npm install
```

Run Next.js app:

```bash
npm run dev
```

Open:

```text
http://127.0.0.1:3000
```

## Build Targets

Build package outputs:

```bash
npm run build
```

Build web app:

```bash
npm run build:web
```

Run production web app:

```bash
npm run start
```

## Package Usage

```ts
import { IFS, LSystem } from 'fractals';
```

Library outputs:

- `lib/` CommonJS + declarations
- `esm/` ESM build

## Script Automation

- `npm run test:fractals:playwright`:
  - starts Next.js dev server
  - tests all fractal type + preset combinations in UI
  - writes artifacts to `artifacts-playwright/`

- `node scripts/generate-all-fractals.js`:
  - generates catalog images to `artifacts/`
  - writes summary `artifacts/index.json`

## Documentation

- `docs/architecture.md`
- `docs/techstack.md`
- `docs/use-cases.md`
- `docs/fractals.md`
