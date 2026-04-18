# Offline & Caching Policy

## Purpose

Students may use HSC Math Hub in low-connectivity environments (exam venues, public transport). Previously viewed PDF pages must remain accessible offline via a service worker cache.

## Strategy overview

| Asset type | Strategy | Cache name |
|---|---|---|
| Static assets (JS, CSS, fonts, images) | **Cache-first** | `hsc-static-v1` |
| Next.js page HTML | **Stale-while-revalidate** | `hsc-pages-v1` |
| PDF data (`raw.githubusercontent.com/*.pdf`) | **Network-first with cache fallback** | `hsc-pdfs-v1` |
| Thumbnails (`/thumbnails/*.webp`) | **Cache-first** | `hsc-static-v1` |

## Service worker implementation

- Register the service worker in the root layout (`app/layout.tsx`) after the page hydrates:
  ```ts
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js');
  }
  ```
- The service worker file lives at `public/sw.js` (served at `/sw.js`).
- Use the **Workbox** library (already available as a Bun dependency) rather than hand-rolling cache logic.

## PDF caching rules

- Cache individual PDF responses keyed by URL.
- Maximum cached PDF storage: **100 MB** (managed by LRU eviction via Workbox `CacheableResponsePlugin` and `ExpirationPlugin`).
- PDF cache TTL: **7 days** (users should get fresh content on a new week's study session).
- On a cache hit while offline, show a banner: `"Viewing cached version — you're offline."` (see [error-handling.md](error-handling.md)).

## Cache versioning

- Increment the cache name suffix (e.g., `hsc-static-v2`) when static assets change in a way that requires a hard cache bust.
- The service worker's `activate` event must delete all caches with outdated version suffixes.

## Offline UI

- If a booklet URL has **never** been cached and the user is offline, show:
  ```
  ⚠  This booklet is not available offline.
  Open it once while connected to make it available offline.
  ```
- Do not show a broken PDF viewer for an uncached booklet.

## Testing

Playwright does not natively simulate service workers in offline mode. For offline behavior:
- Use Playwright's `context.setOffline(true)` to simulate network loss.
- Seed the cache in the test setup by navigating to the booklet while online first.
- Assert that the PDF page is still visible (or the offline-cached banner is shown) after going offline.

Add these tests to `tests/e2e/` under a new `offline.spec.ts` file.
