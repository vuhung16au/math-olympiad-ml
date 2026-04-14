# Tech Stack (TO-BE)

Related docs:
- `docs/architecture.md`
- `docs/use-cases.md`
- `README.md`

## Frontend

- Next.js App Router
- React + TypeScript
- CSS (global styles, Tailwind-ready architecture)

## Backend

- Next.js Route Handlers (`app/api/*`)
- Node.js runtime on Vercel

## Fractal Core

- Existing TypeScript package in `src/`
- `IFS` and `LSystem` remain publishable outputs via `lib/` and `esm/`

## Tooling

- TypeScript
- ESLint
- Prettier
- Playwright

## Deployment

- Vercel preview + production
- Single deployment unit for web app
- Package publishing remains independent from web deploy
