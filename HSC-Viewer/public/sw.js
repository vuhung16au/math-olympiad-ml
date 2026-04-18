// HSC Math Hub — Service Worker
// Caching strategy per docs/agents/offline-caching.md:
//   Static assets (JS, CSS, fonts, images, thumbnails) → Cache-first  (hsc-static-v1)
//   Next.js page HTML                                  → Stale-while-revalidate (hsc-pages-v1)
//   PDF data (raw.githubusercontent.com/*.pdf)         → Network-first + cache fallback (hsc-pdfs-v1)

importScripts(
  "https://storage.googleapis.com/workbox-cdn/releases/6.6.0/workbox-sw.js"
);

workbox.setConfig({ debug: false });

const { registerRoute } = workbox.routing;
const { CacheFirst, NetworkFirst, StaleWhileRevalidate } = workbox.strategies;
const { CacheableResponsePlugin } = workbox.cacheableResponse;
const { ExpirationPlugin } = workbox.expiration;

// ── 1. Static assets — Cache-first ──────────────────────────────────────────
// Matches JS, CSS, fonts, images, and thumbnail WebPs served from this origin.
registerRoute(
  ({ request, url }) =>
    ["script", "style", "font", "image"].includes(request.destination) ||
    url.pathname.startsWith("/thumbnails/"),
  new CacheFirst({
    cacheName: "hsc-static-v1",
    plugins: [
      new CacheableResponsePlugin({ statuses: [0, 200] }),
      new ExpirationPlugin({
        maxEntries: 150,
        maxAgeSeconds: 30 * 24 * 60 * 60, // 30 days
      }),
    ],
  })
);

// ── 2. Next.js page HTML — Stale-while-revalidate ───────────────────────────
registerRoute(
  ({ request }) => request.destination === "document",
  new StaleWhileRevalidate({
    cacheName: "hsc-pages-v1",
    plugins: [
      new CacheableResponsePlugin({ statuses: [0, 200] }),
      new ExpirationPlugin({
        maxEntries: 30,
        maxAgeSeconds: 7 * 24 * 60 * 60, // 7 days
      }),
    ],
  })
);

// ── 3. PDF data — Network-first with 100 MB / 7-day LRU cache ───────────────
// Covers raw.githubusercontent.com PDFs and any same-origin .pdf paths.
registerRoute(
  ({ url }) =>
    (url.hostname === "raw.githubusercontent.com" &&
      url.pathname.endsWith(".pdf")) ||
    url.pathname.endsWith(".pdf"),
  new NetworkFirst({
    cacheName: "hsc-pdfs-v1",
    networkTimeoutSeconds: 10,
    plugins: [
      new CacheableResponsePlugin({ statuses: [0, 200] }),
      new ExpirationPlugin({
        maxEntries: 20,
        maxAgeSeconds: 7 * 24 * 60 * 60, // 7 days
        purgeOnQuotaError: true,
      }),
    ],
  })
);

// ── Activate: delete stale versioned caches ──────────────────────────────────
const CURRENT_CACHES = ["hsc-static-v1", "hsc-pages-v1", "hsc-pdfs-v1"];

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((names) =>
        Promise.all(
          names
            .filter((n) => n.startsWith("hsc-") && !CURRENT_CACHES.includes(n))
            .map((n) => caches.delete(n))
        )
      )
      .then(() => self.clients.claim())
  );
});
