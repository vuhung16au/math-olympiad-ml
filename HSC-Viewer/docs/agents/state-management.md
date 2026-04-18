# State Management Policy

## Purpose

State in HSC-Viewer is simple and deliberately local. There is no global state library. This document defines exactly where each kind of state lives so agents always put new state in the right place.

## Decision table

| State category | Where it lives | Why |
|---|---|---|
| PDF render state (current page, scale, loading, error) | React `useState` inside `PDFViewer` | Component-local, ephemeral, no need to share |
| Sidebar open/collapsed | React `useState` in `AppShell` / `Sidebar` | UI-local |
| Mobile menu open | React `useState` in `AppShell` / `MobileMenu` | UI-local |
| Outline tab (pages vs outline) | Cookie via `PREF_KEYS.outlineTab` | Persists across refreshes |
| Reading theme (light/dark/sepia) | Cookie via `PREF_KEYS.readingTheme` | Persists across sessions |
| Zoom / scale | Cookie via `PREF_KEYS.scale` | Persists across sessions |
| Last visited page per booklet | Cookie via `PREF_KEYS.lastPageBySlug` | Enables resume-on-return |
| Last opened booklet URL | Cookie via `PREF_KEYS.lastUrl` | Used by home route to restore session |
| Resume mode preference | Cookie via `PREF_KEYS.resumeMode` | User choice: auto / prompt / off |
| Navigator panel position | Cookie via `PREF_KEYS.navPanelPos` | Layout preference |
| Booklet metadata | `lib/booklets.ts` static array | Never changes at runtime |
| Active booklet | URL route (`/booklets/[slug]`) | Shareable, linkable, indexable |
| Initial page on load | URL query param (`?page=N`) | Allows deep-linking to a specific page |
| Transient scroll / outline expand | `sessionStorage` via `PREF_KEYS` | Lost on tab close is acceptable |

## Rules for agents

1. **No global state library.** Do not introduce Redux, Zustand, Context API for data that already fits one of the above buckets.
2. **React Context is permitted only** for values that genuinely need to be shared across the entire component tree without prop drilling (e.g., the current theme). Keep context providers narrow in scope.
3. **URL is the source of truth for the active booklet.** Never derive "which booklet is open" from local state or a cookie — read the route slug.
4. **All cookie reads/writes go through `lib/preferences.ts`.** Never call `document.cookie` directly. Use `getPref()` / `setPref()` with a key from `PREF_KEYS`.
5. **Validate cookie values on read.** Cookies are user-editable. Always clamp or validate before use:
   ```ts
   const raw = getPref(PREF_KEYS.scale);
   const scale = validateScale(raw ? parseFloat(raw) : PDF_DEFAULTS.defaultScale);
   ```
6. **Deep-link support.** Any state that should be shareable via URL (current page, initial zoom) must be expressible as a query parameter or route segment, not only in a cookie.

## Adding new persistent state

If you need to persist a new user preference:

1. Add a key to `PREF_KEYS` in `lib/preferences.ts`.
2. Add it to the permitted keys table in [docs/agents/cookies.md](cookies.md).
3. Read it with `getPref()`, validate the value, fall back to a sensible default.
4. Write it with `setPref()` when the user changes the value.
5. Add an e2e test that verifies the preference survives a page reload.
