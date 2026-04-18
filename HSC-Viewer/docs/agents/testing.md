# Testing Policy

## Purpose

All features implemented by agents must be covered by Playwright end-to-end tests. This is the only test layer for HSC-Viewer (no Jest, no unit tests).

## Stack

- Runner: `@playwright/test`
- Package manager: Bun
- Config: `playwright.config.ts`
- Test files: `tests/e2e/`

## Commands

```bash
# Install browser (first time)
bunx playwright install chromium

# Run full suite
make test

# Run in headed mode (debugging)
make test-headed

# Open Playwright UI
make test-ui

# Run a single spec
bunx playwright test tests/e2e/my-spec.spec.ts
```

## Existing test files

| File | Coverage area |
|---|---|
| `viewer-smoke.spec.ts` | Shell renders sidebar, toolbar, navigator, footer |
| `navigation-and-state.spec.ts` | Next/prev/page-input updates route and `last-url` cookie |
| `toolbar-and-zoom.spec.ts` | Tooltip attributes and zoom cookie persistence |
| `navigator-outline.spec.ts` | Pages and outline navigation jump to expected targets |
| `error-and-recovery.spec.ts` | PDF load failure shows user-facing error state |
| `responsive.spec.ts` | Key controls usable at mobile/tablet/desktop viewports |
| `restore-last-session.spec.ts` | Home route restores last booklet via cookie |
| `helpers.ts` | Shared test utilities |

## PDF mocking

Tests use `NEXT_PUBLIC_E2E_MOCK_PDF=1`. Control behavior via query parameter:

| Parameter | Behavior |
|---|---|
| `?e2ePdfMock=success` | Deterministic mocked pages + outline |
| `?e2ePdfMock=error` | Forces load failure state |
| `?e2ePdfMock=off` | Disables mock (use with Playwright network interception) |

For network-level control, intercept `*.pdf` requests:
```ts
await page.route('**/*.pdf', route => route.fulfill({ status: 500 }));
```

## Rules for agents

1. **Every new feature or bug fix must include or update a Playwright test.**
2. **Use role- and accessible name-based selectors** (`getByRole`, `getByLabel`, `getByText`) — not CSS selectors or test IDs, except where a stable `data-testid` already exists.
3. **Avoid visual snapshot tests** unless rendering flakiness is resolved.
4. **Do not use `page.waitForTimeout()`** — use `expect(locator).toBeVisible()` or explicit event waits instead.
5. **Tests must pass in CI** with retries enabled. Do not commit flaky tests.
6. **Add network mocking** only when behavior depends on success/failure of a fetch.

## Viewports to cover for new UI

New interactive UI must be tested at:

| Label | Viewport |
|---|---|
| Mobile | 375 × 812 |
| Tablet | 768 × 1024 |
| Desktop | 1280 × 800 |

## Adding a new spec

1. Create `tests/e2e/my-feature.spec.ts`.
2. Import shared helpers from `tests/e2e/helpers.ts`.
3. Use `test.describe` to group related cases.
4. Run `make test` locally and confirm all tests pass before submitting.
5. Update the table above in this document.

## CI

- Playwright e2e suite runs as the test stage.
- Collect `playwright-report/` and `test-results/` as artifacts on failure.
- Retries are enabled in CI (`retries: 2` in `playwright.config.ts`) and disabled locally.
