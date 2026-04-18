# Bun Notes (HSC-Viewer)

## Overview

This project is Bun-first for JavaScript/TypeScript workflows.

- Dependency install uses `bun install` (see `Makefile` target `install`)
- Script execution uses `bun run ...` (dev/build/start/lint/test)
- One-off CLI usage uses `bunx ...` (Playwright browser install)
- Lockfile is `bun.lock`, so Bun is the canonical package manager here
- Vercel build command is explicitly `bun run build`

### Why Bun over npm in this project?

Short answer: consistency + speed + simpler ops.

- Single toolchain path already wired into project automation (`Makefile`, Playwright config, Vercel)
- Faster install/script startup in daily dev loops (noticeable for Next.js + Playwright workflows)
- `bun.lock` gives deterministic dependency resolution aligned with current CI/deploy setup
- Bun-specific dependency safety controls are already configured in `package.json`:
  - `ignoreScripts`
  - `trustedDependencies`

If you switch to npm locally, behavior may diverge from the project defaults and lockfile source of truth.

## Frequently Used Commands

Run from `HSC-Viewer/`.

- Install deps: `bun install`
- Dev server: `bun run next dev`
- Build: `bun run next build`
- Start prod server: `bun run next start`
- Lint: `bun run lint`
- E2E tests: `bun run test:e2e`
- E2E headed: `bun run test:e2e:headed`
- E2E UI: `bun run test:e2e:ui`
- Playwright browser binary install: `bunx playwright install chromium`

Equivalent via Make targets:

- `make install`, `make dev`, `make build`, `make lint`, `make test`

## Quick How-To

### Use `bun`

- Install dependencies: `bun install`
- Run package script: `bun run <script>`
- Run a local binary/script directly when needed: `bun run <command>`

Examples:

- `bun run build`
- `bun run test:e2e`

### Use `bunx`

Use `bunx` for one-off package executables (similar to `npx`) without changing package scripts.

Example used by this project:

- `bunx playwright install chromium`

Rule of thumb:

- Use `bun run ...` for repo-defined scripts
- Use `bunx ...` for ad-hoc executable invocations
