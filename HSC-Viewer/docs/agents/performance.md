# Performance Budgets Policy

## Purpose

Performance directly affects usability, especially on mobile. Agents must not introduce changes that regress the budgets below.

## Budgets

### Runtime (measured on a mid-range Android device, simulated 4G)

| Metric | Budget | Tool |
|---|---|---|
| First Contentful Paint (FCP) | ≤ 1.5 s | Lighthouse / WebPageTest |
| Time to Interactive (TTI) | ≤ 3 s | Lighthouse |
| PDF first page render | ≤ 500 ms after PDF bytes available | `performance.mark()` |
| Page navigation (page N → page N+1) | ≤ 300 ms | `performance.mark()` |

### Build output

| Asset | Budget |
|---|---|
| Total JS (gzipped, initial page load) | ≤ 200 KB |
| Total CSS (gzipped) | ≤ 20 KB |
| Largest individual chunk | ≤ 100 KB gzipped |

## Rules for agents

- **Check `bun run build` output** for bundle sizes before submitting. Next.js prints chunk sizes in the build log.
- **Do not add new heavyweight dependencies** (e.g., full lodash, moment.js, large UI libraries) without justification. Prefer tree-shakeable imports.
- **Lazy-load heavy components.** The PDF renderer (`react-pdf` + `pdfjs-dist`) is already dynamically imported. Other large components must follow the same pattern:
  ```ts
  const PDFViewer = dynamic(() => import('@/components/pages/PDFViewer'), { ssr: false });
  ```
- **Do not block the main thread** during PDF rendering. Offload heavy decode/render work to web workers where `pdfjs-dist` supports it.
- **Avoid layout thrash.** Do not read and write layout properties (e.g., `offsetWidth`, `getBoundingClientRect`) in the same synchronous block.
- **Compress images.** Thumbnails in `public/thumbnails/` must be WebP with maximum dimension 400 px. Use `scripts/generate-thumbnails.js` to regenerate after changes.

## How to measure locally

```bash
# Build and check chunk sizes
cd HSC-Viewer
bun run build

# Run Lighthouse against the local dev server
bunx serve@latest out &
bunx lighthouse http://localhost:3000 --view
```

## CI enforcement

If Lighthouse CI is configured, the build must not merge if any budget is exceeded. Agents must not bypass or disable budget checks.
