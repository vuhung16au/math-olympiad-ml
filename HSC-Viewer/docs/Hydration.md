# Preventing Hydration Mismatches

Contributor guide for avoiding React hydration errors in HSC Math Hub. For agent/automation rules, see [docs/agents/hydration.md](agents/hydration.md).

## What is a hydration mismatch?

Next.js server-renders HTML, then React on the client “hydrates” that markup. If the client’s first render does not match the server HTML (attributes, structure, text), React logs a console error such as:

> A tree hydrated but some attributes of the server rendered HTML didn't match the client properties.

These bugs are easy to introduce and painful to debug. This project has hit them several times on client layouts (`MobileMenu`, cookie banner, toolbar prefs).

## PR checklist

Copy into your PR description when you touch UI under `components/` or client layouts:

```markdown
## Hydration

- [ ] Ran `bunx playwright test tests/e2e/hydration-mismatch.spec.ts`
- [ ] Ran full suite (`make test`) or CI equivalent
- [ ] Checked browser console on `/` and a booklet route in dev — no hydration errors
- [ ] Restarted `make dev` after changing client `className`s (if applicable)
- [ ] Added new shell/overlay routes to `CORE_HYDRATION_ROUTES` in `hydration-mismatch.spec.ts` (if applicable)
```

## Run the hydration spec on every UI PR

The automated guard visits core routes and fails if the browser console reports a hydration mismatch:

```bash
bunx playwright test tests/e2e/hydration-mismatch.spec.ts
```

Also run the full suite before merge:

```bash
make test
```

When you add a **new top-level layout, shell, or client overlay**, register its URL in `CORE_HYDRATION_ROUTES` inside `tests/e2e/hydration-mismatch.spec.ts`.

Helpers for other specs live in `tests/e2e/helpers.ts`: `attachHydrationMismatchGuard()`, `gotoAndAssertNoHydrationMismatch()`.

## Local dev habits

### After changing client `className`s

1. Stop and restart `make dev` (Turbopack can serve a stale client bundle against fresh SSR HTML).
2. Hard-refresh the browser (Cmd+Shift+R / Ctrl+Shift+R).
3. Re-check the console on `/` and `/booklets/<slug>/1`.

### False positives from browser extensions

If the stack trace mentions `chrome-extension://` (e.g. React DevTools), retry in a private/incognito window before debugging app code.

## Coding guidelines

### New overlays and drawers

Prefer one of:

| Approach | When to use | Example |
|---|---|---|
| `dynamic(() => import("./Menu"), { ssr: false })` | Fixed overlay, drawer, or UI that does not need SSR HTML | `MobileMenu` in `AppShell.tsx` |
| Stable `className` strings | Layout classes that are the same on server and client | `MobileMenu` aside/nav classes |
| `joinClasses(...parts)` | Conditional Tailwind without empty segments | `MobileMenu.tsx` |

Avoid toggling layout classes with a post-mount flag:

```tsx
// Avoid — causes mismatch or double spaces in className
const [mounted, setMounted] = useState(false);
className={[base, mounted ? "flex flex-col" : ""].join(" ")}
```

Never build `className` with `.join(" ")` when the array may contain `""` — use `.filter(Boolean).join(" ")` instead.

### Cookie and `window` preferences

Read cookies, `localStorage`, and `window.matchMedia` in **`useEffect`** (or event handlers), not during render. Server and client must share the same defaults on first paint; effects may update afterward.

Examples in the codebase: `AppShell` sidebar collapse, `PDFViewer` toolbar prefs, `CookieConsentBanner`.

## CI suggestions

### Minimum (recommended today)

Run the full Playwright suite in CI, including `hydration-mismatch.spec.ts` (already part of `make test`).

### Optional: faster feedback on layout PRs

Add a dedicated job (e.g. `playwright-hydration`) that runs only:

```bash
bunx playwright test tests/e2e/hydration-mismatch.spec.ts
```

Trigger it on path filters such as:

```yaml
paths:
  - 'components/**'
  - 'app/**/layout.tsx'
  - 'tests/e2e/hydration-mismatch.spec.ts'
```

Keep the full e2e job on main/merge queue so nothing slips through on non-UI changes.

## Optional improvement: shared `joinClasses`

`joinClasses()` currently lives in `MobileMenu.tsx`. Consider extracting to `lib/classnames.ts` and reusing anywhere you assemble Tailwind strings:

```ts
export function joinClasses(...parts: Array<string | false | null | undefined>): string {
  return parts.filter(Boolean).join(' ');
}
```

## Related docs

| Doc | Audience | Content |
|---|---|---|
| [docs/agents/hydration.md](agents/hydration.md) | AI agents / policy | Strict rules, anti-patterns |
| [docs/agents/testing.md](agents/testing.md) | Agents | E2e requirements, hydration guard API |
| [docs/TESTING.md](TESTING.md) | Contributors | Full Playwright strategy |
| [docs/agents/state-management.md](agents/state-management.md) | Agents | Cookie vs React state |
| [docs/agents/coding-conventions.md](agents/coding-conventions.md) | Agents | `"use client"`, `dynamic()` |
