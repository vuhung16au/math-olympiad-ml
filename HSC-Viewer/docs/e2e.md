# E2E Test Notes (HSC-Viewer)

## Overview

Current test strategy is browser-level E2E with Playwright, executed through Bun.

- runner: `@playwright/test`
- package manager/runtime: `bun`
- scope: critical user-visible reader flows (navigation, zoom, outline, error/recovery, responsive)
- this phase intentionally excludes Jest and unit/component tests

Why Playwright over Jest here:

- The product risk is in end-user browser behavior, not isolated pure functions.
- Key features span routing + cookies + PDF loading + responsive UI, which are integration-heavy.
- Playwright validates real browser interactions and failure modes (including mocked PDF/network paths) with higher confidence for this app.

Why no unit tests (for now):

- Team chose depth in high-value E2E coverage over fragmented low-signal unit coverage.
- Reader behavior is best validated at system level because most logic is UI-state + browser API integration.
- This keeps maintenance focused on behavior contracts that matter in production.

## Frequently Useful Commands

Run from `HSC-Viewer/`.

- Install deps: `bun install`
- Install Playwright browser: `bunx playwright install chromium`
- Run E2E suite: `bun run test:e2e` or `make test`
- Run headed mode: `bun run test:e2e:headed` or `make test-headed`
- Open Playwright UI: `bun run test:e2e:ui` or `make test-ui`
- Direct Playwright invocation: `bunx playwright test`

## Quick How-To (bun, bunx, Playwright)

1. Install dependencies and browser binary:

```bash
cd HSC-Viewer
bun install
bunx playwright install chromium
```

2. Run tests (default CI-like headless path):

```bash
bun run test:e2e
```

3. Debug locally when needed:

```bash
bun run test:e2e:headed
bun run test:e2e:ui
```

Rule of thumb:

- Use `bun run ...` for repo scripts in `package.json`
- Use `bunx ...` for one-off Playwright CLI commands
