# Architecture (Agent Reference)

## Purpose

This is the agent-focused architecture summary. Read this before adding or moving files. For full details see [docs/architecture.md](../architecture.md).

## Rendering model

| Route | Rendering | Notes |
|---|---|---|
| `/` | Server component → `GridView` (client) | Library grid |
| `/booklets/[slug]` | Statically generated at build time | One page per booklet slug from `BOOKLETS` in `lib/booklets.ts` |
| PDF rendering | Client-side only (`"use client"`) | `react-pdf` + `pdfjs-dist` |

**Important:** `generateStaticParams()` in `app/booklets/[slug]/page.tsx` drives which slugs are built. Adding a booklet means adding it to `lib/booklets.ts` — that's the only data source.

## Data flow

```
lib/booklets.ts (BOOKLETS array)
  └─► app/booklets/[slug]/page.tsx  (static generation, metadata)
        └─► components/pages/PDFViewer.tsx  (client component)
              ├─► lib/preferences.ts  (cookie read/write)
              ├─► lib/analytics.ts    (event tracking)
              ├─► lib/pdf-helpers.ts  (pure utilities)
              ├─► lib/constants.ts    (PDF_DEFAULTS, PREF_KEYS)
              └─► components/ui/*     (controls, spinner, error boundary)
```

## Component responsibilities

| Component | Responsibility |
|---|---|
| `components/layout/AppShell.tsx` | Outer shell: sidebar + main content area |
| `components/layout/Header.tsx` | Top bar with title and toolbar toggle |
| `components/layout/Sidebar.tsx` | Booklet list navigation |
| `components/layout/MobileMenu.tsx` | Slide-in menu for narrow viewports |
| `components/pages/GridView.tsx` | Home grid of booklet cards |
| `components/pages/PDFViewer.tsx` | Full PDF reader: state, controls, canvas |
| `components/ui/PDFControls.tsx` | Toolbar buttons (zoom, nav, fullscreen, etc.) |
| `components/ui/ErrorBoundary.tsx` | Catches render errors, shows friendly fallback |
| `components/ui/LoadingSpinner.tsx` | Loading state indicator |
| `components/ui/ThumbnailCard.tsx` | Single booklet card for the grid |
| `components/common/Footer.tsx` | Site-wide footer |

## lib/ modules

| Module | What lives here |
|---|---|
| `lib/booklets.ts` | `Booklet` type, `BOOKLETS` array, `getBookletBySlug()`, `getAvailableBooklets()` |
| `lib/constants.ts` | `COLORS`, `BREAKPOINTS`, `PDF_DEFAULTS`, `REPO_LINKS`, `APP_NAME` |
| `lib/preferences.ts` | Cookie helpers: `getPref()`, `setPref()`, `PREF_KEYS`, page-by-slug persistence |
| `lib/analytics.ts` | Thin wrappers around `@vercel/analytics` `track()` |
| `lib/pdf-helpers.ts` | `fetchPdf()`, `validatePageNumber()`, `validateScale()`, `PDFState` type |

## State management summary

See [docs/agents/state-management.md](state-management.md) for the full policy. Quick reference:

| State type | Where it lives |
|---|---|
| Current page, scale, loading state | React `useState` inside `PDFViewer` |
| Theme, zoom, last page, last URL | Cookies via `lib/preferences.ts` |
| Transient UI (outline open/closed) | `sessionStorage` via `PREF_KEYS` |
| Route | Next.js App Router URL (`/booklets/[slug]`) |
| Booklet metadata | `lib/booklets.ts` (static, no runtime fetch) |

## Key constraints for agents

- **No server-side data fetching for PDFs.** PDFs are fetched client-side via `fetchPdf()` in `lib/pdf-helpers.ts`. The raw GitHub URL is the source.
- **No database.** All booklet metadata is hardcoded in `lib/booklets.ts`.
- **No authentication.** The app is fully public.
- **Static export.** The build output is a set of static HTML/JS/CSS files deployed to Vercel. Do not use APIs that require a Node.js server at runtime (e.g., `app/api/` routes are not currently used and should not be added without discussion).
- **`pdfjs` worker** is loaded from a CDN (`cdnjs.cloudflare.com`). Do not change this without updating CSP headers (see [security.md](security.md)).

## Adding a new booklet

1. Add an entry to `BOOKLETS` in `lib/booklets.ts`.
2. Generate its thumbnail: `bun run thumbnails`.
3. Run `bun run build` and verify the new static route appears in the output.
4. No other files need to change.
