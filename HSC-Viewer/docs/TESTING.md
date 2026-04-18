# Testing Strategy

HSC-Viewer uses browser-level end-to-end tests with Playwright.

## Scope

- e2e coverage only for this phase
- no Jest
- no component/unit tests in this phase
- focus on critical reader functionality

## Tooling

- runner: `@playwright/test`
- package manager/runtime: Bun
- command entrypoints:
  - `make test`
  - `bun run test:e2e`

## Deterministic PDF Mocking

Tests run the app with `NEXT_PUBLIC_E2E_MOCK_PDF=1`.

In this mode, the viewer can render mock pages and mock outline data by query parameter:

- `?e2ePdfMock=success` uses deterministic mocked pages and outline
- `?e2ePdfMock=error` forces a mocked load failure state
- `?e2ePdfMock=off` disables internal mock mode (used with Playwright network interception)

For network-level behavior, tests may intercept `*.pdf` requests and return:

- mocked PDF content for success
- HTTP 500 for failure

## Test Structure

- `tests/e2e/viewer-smoke.spec.ts`
  - shell renders sidebar, toolbar, navigator controls, and footer
- `tests/e2e/navigation-and-state.spec.ts`
  - next/prev/page input updates route and last-url cookie
- `tests/e2e/toolbar-and-zoom.spec.ts`
  - tooltip attributes and zoom persistence via cookies
- `tests/e2e/navigator-outline.spec.ts`
  - pages and outline navigation jump to expected targets
- `tests/e2e/error-and-recovery.spec.ts`
  - PDF load failure shows user-facing error state
- `tests/e2e/responsive.spec.ts`
  - key controls remain usable on mobile/tablet/desktop
- `tests/e2e/restore-last-session.spec.ts`
  - home route restores last opened booklet via cookie

## Local Run

```bash
cd HSC-Viewer
bunx playwright install chromium
make test
```

## CI Guidance

- run Playwright e2e suite as the test stage
- collect `playwright-report` and `test-results` artifacts on failure
- keep retries enabled in CI and disabled locally

## Adding New Tests

- keep tests focused on user-visible behavior
- prefer stable selectors by role and accessible name
- avoid visual snapshots unless rendering flakiness is resolved
- add network mocking only when behavior depends on failure/success paths
