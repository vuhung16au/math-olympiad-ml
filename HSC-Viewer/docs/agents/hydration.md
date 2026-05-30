# Hydration Policy

## Purpose

Hydration mismatches mean the HTML React rendered on the server does not match what the client renders on first paint. React will log a console error, leave the UI in an inconsistent state, and may show subtle bugs. This project has hit these repeatedly — follow this policy to prevent regressions.

## What counts as a failure

Any browser console **error** or **warning** that includes phrases such as:

- `hydration` + `didn't match` / `did not match`
- `A tree hydrated but some attributes of the server rendered HTML didn't match`
- `Hydration failed`

Browser extensions (e.g. React DevTools) can also trigger false positives locally. If the message references `chrome-extension://`, verify in a private window before chasing app code.

## Automated guard

Playwright watches the console on core routes:

- Spec: `tests/e2e/hydration-mismatch.spec.ts`
- Helpers: `attachHydrationMismatchGuard()`, `gotoAndAssertNoHydrationMismatch()` in `tests/e2e/helpers.ts`

**When you add a new top-level layout, shell, or client-only overlay**, add its primary URL to `CORE_HYDRATION_ROUTES` in `hydration-mismatch.spec.ts` (or extend an existing describe block with the same guard).

Run before every PR:

```bash
bunx playwright test tests/e2e/hydration-mismatch.spec.ts
```

## Rules for agents (must follow)

### 1. Server and client first paint must match

The initial render of every `"use client"` component in the tree must produce the **same DOM** on the server (when SSR runs) and on the client (hydration). Do not branch on `typeof window`, `Date.now()`, `Math.random()`, or locale-specific formatting during render.

### 2. Defer browser-only state to `useEffect`

Cookie reads, `localStorage`, `window.matchMedia`, and layout preferences belong in `useEffect` (or event handlers), not in the render path. The server and the client's first paint should use the same defaults; then effects may update.

Existing examples: `AppShell` sidebar collapse, `PDFViewer` toolbar prefs, `CookieConsentBanner` visibility.

### 3. Never toggle `className` with a post-mount flag for layout

Avoid patterns like:

```tsx
// Bad — often causes mismatch or double spaces in className
const [mounted, setMounted] = useState(false);
useEffect(() => setMounted(true), []);
className={[base, mounted ? "flex flex-col" : ""].join(" ")}
```

Prefer:

- **Stable class strings** on server and client, or
- **`dynamic(() => import("./Overlay"), { ssr: false })`** when the component is purely client UI (see `MobileMenu` in `AppShell.tsx`).

### 4. Build `className` without empty segments

Use `filter(Boolean).join(" ")` (see `joinClasses()` in `MobileMenu.tsx`). Never use `.join(" ")` on an array that may contain `""` — that inserts double spaces and can differ between server HTML and client output.

### 5. Use `dynamic(..., { ssr: false })` for client-only shells

Use when the component:

- Depends on `window` / cookies on first paint, or
- Is a fixed overlay (drawer, modal, PDF viewer) that does not need SEO from SSR

Document the import in [architecture.md](architecture.md) when adding a new one.

### 6. Do not SSR and client-render different component trees

If the server renders component A and the client renders component B for the same slot, hydration will fail. Keep conditional rendering driven by props that are identical on server and client for the first paint.

## Checklist before merging UI changes

1. Run `bunx playwright test tests/e2e/hydration-mismatch.spec.ts`.
2. Run the full suite: `make test`.
3. Manually open `/` and a booklet route in dev; confirm the browser console has no hydration errors (hard refresh after layout changes).
4. If you changed Tailwind classes on a client layout, restart `make dev` so Turbopack does not serve a stale client bundle against fresh SSR HTML.

## Contributor guide

Team PR checklist, CI ideas, and local dev habits: [../Hydration.md](../Hydration.md).

## Related policies

- [state-management.md](state-management.md) — where cookies vs React state live
- [coding-conventions.md](coding-conventions.md) — `"use client"` and `dynamic()` patterns
- [testing.md](testing.md) — e2e requirements
