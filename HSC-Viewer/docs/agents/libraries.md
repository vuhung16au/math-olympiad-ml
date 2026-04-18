# Libraries Policy

## Purpose

Agents must not add new dependencies without consulting this document. Unapproved packages bloat the bundle, introduce security risk, and may conflict with the existing stack.

## Approved runtime dependencies

| Package | Version | Purpose |
|---|---|---|
| `next` | 16.x | App framework |
| `react` | 19.x | UI rendering |
| `react-dom` | 19.x | DOM rendering |
| `react-pdf` | ^9.0 | PDF document/page components |
| `pdfjs-dist` | ^4.0 | PDF.js engine used by react-pdf |
| `lucide-react` | ^0.344 | Icon set (tree-shakeable) |
| `@vercel/analytics` | ^2.0 | Page view and custom event tracking |

## Approved dev dependencies

| Package | Purpose |
|---|---|
| `@playwright/test` | e2e test runner |
| `tailwindcss` ^4 | Utility CSS |
| `@tailwindcss/postcss` | PostCSS integration for Tailwind v4 |
| `typescript` ^5 | Type checking |
| `eslint` + `eslint-config-next` | Linting |
| `pdf2pic` + `sharp` | Offline thumbnail generation (`scripts/`) |

## Disallowed patterns

| What | Why |
|---|---|
| `Jest` / `vitest` / component tests | Testing strategy is Playwright e2e only |
| `Redux` / `Zustand` / `Jotai` / other global state libraries | React `useState` + cookies is sufficient; see [state-management.md](state-management.md) |
| CSS-in-JS (`styled-components`, `emotion`, etc.) | Tailwind + CSS variables is the styling system |
| `moment.js` / full `lodash` | Use native JS equivalents; no date/utility libraries |
| `axios` | Use native `fetch()` |
| Tailwind color utilities (`bg-purple-700`, etc.) | Use CSS variable references; see [colors.md](colors.md) |
| Any package with a known critical CVE | Run `bun audit` to verify |

## Adding a new dependency

Before adding any package:

1. **Check the bundle impact.** Use [bundlephobia.com](https://bundlephobia.com) to estimate gzipped size. Confirm the JS budget in [performance.md](performance.md) will not be exceeded.
2. **Check for CVEs.** Run `bun audit` after `bun add <package>`.
3. **Prefer tree-shakeable packages.** Import only what you use:
   ```ts
   // Good
   import { ChevronLeft } from 'lucide-react';

   // Bad — imports entire library
   import * as Icons from 'lucide-react';
   ```
4. **Document the addition** by updating the approved table in this file.
5. **Do not add `devDependencies` to `dependencies`** and vice versa.

## Package manager

Use **Bun** exclusively:

```bash
bun add <package>          # runtime dep
bun add -d <package>       # dev dep
bun remove <package>
bun install                # install from lockfile
```

Never use `npm`, `yarn`, or `pnpm` — they will generate conflicting lockfiles.
