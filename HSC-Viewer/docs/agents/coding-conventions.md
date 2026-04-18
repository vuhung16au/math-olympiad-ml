# Coding Conventions

## Purpose

Consistent naming, structure, and TypeScript usage makes the codebase easier for both humans and agents to navigate. Follow these conventions in all new and modified code.

## TypeScript

- **Strict mode is on** (`"strict": true` in `tsconfig.json`). All code must compile without errors under strict mode.
- **No `any`** — use specific types, `unknown` with a type guard, or a well-named interface.
- **No `@ts-ignore`** without a comment on the same line explaining why it is unavoidable.
- **No `@ts-nocheck`** — ever.
- **Prefer `type` for object shapes and unions; use `interface` for extendable contracts** (both are fine; be consistent within a file).
- **Prefer named exports** from `lib/`. No default exports from library modules. Components may use default exports (Next.js App Router requires them for pages).

```ts
// Good — lib module
export function trackBookletOpened(title: string) { ... }
export type ReadingTheme = 'light' | 'dark' | 'sepia';

// Bad — lib module
export default function trackBookletOpened(...) { ... }
```

## Naming

| Thing | Convention | Example |
|---|---|---|
| React components | `PascalCase` | `PDFViewer`, `ThumbnailCard` |
| Component files | `PascalCase.tsx` | `PDFViewer.tsx` |
| Hooks | `camelCase` prefixed with `use` | `usePdfState` |
| Lib modules | `kebab-case.ts` | `pdf-helpers.ts`, `analytics.ts` |
| Constants (primitive scalars) | `SCREAMING_SNAKE_CASE` | `ONE_YEAR_SECONDS`, `APP_NAME` |
| Constant objects/maps | `SCREAMING_SNAKE_CASE` | `PREF_KEYS`, `PDF_DEFAULTS`, `BOOKLETS` |
| Types / interfaces | `PascalCase` | `Booklet`, `PDFState`, `ReadingTheme` |
| Local variables & params | `camelCase` | `currentPage`, `bookletTitle` |
| CSS custom properties | `--kebab-case` | `--color-purple`, `--sidebar-width` |
| Route segments | `kebab-case` | `/booklets/hsc-collections` |

## File structure

```
components/
  layout/      ← shell (AppShell, Header, Sidebar, MobileMenu)
  pages/       ← full-page view components (GridView, PDFViewer)
  ui/          ← reusable leaf controls (PDFControls, ErrorBoundary, LoadingSpinner, ThumbnailCard)
  common/      ← shared cross-cutting components (Footer)
lib/
  analytics.ts      ← Vercel Analytics helpers only
  booklets.ts       ← booklet data and types
  constants.ts      ← app-wide constants (colors, breakpoints, defaults)
  pdf-helpers.ts    ← pure PDF utility functions
  preferences.ts    ← cookie read/write helpers
app/
  page.tsx                    ← home (renders GridView)
  booklets/[slug]/page.tsx    ← booklet viewer (renders PDFViewer)
  layout.tsx                  ← root layout
```

Do not create files outside this structure without updating [docs/agents/architecture.md](architecture.md).

## Imports

Order (enforced by ESLint where configured):

1. React and Next.js imports
2. Third-party libraries
3. Internal `@/` path alias imports (types and components)
4. Relative imports (same directory)
5. CSS imports last

```ts
// Good
import { useCallback, useState } from 'react';
import { track } from '@vercel/analytics';
import type { Booklet } from '@/lib/booklets';
import PDFControls from '@/components/ui/PDFControls';
import { PDF_DEFAULTS, PREF_KEYS } from '@/lib/constants';
import 'react-pdf/dist/Page/AnnotationLayer.css';
```

Always use the `@/` path alias for imports from the project root. Never use relative `../../` paths crossing more than one directory level.

## React / Next.js

- Mark components that use browser APIs, hooks, or event handlers with `"use client"` at the top of the file.
- Components that are purely data-driven and renderable on the server must **not** carry `"use client"`.
- Do not import server-only modules (`fs`, `path`, etc.) in client components.
- Dynamic imports for heavy client components:
  ```ts
  const PDFViewer = dynamic(() => import('@/components/pages/PDFViewer'), { ssr: false });
  ```

## Formatting

- 2-space indentation.
- Single quotes for strings.
- Trailing commas in multi-line objects and arrays.
- Run `bun run lint` before submitting changes. Fix all errors; warnings should be addressed where feasible.
