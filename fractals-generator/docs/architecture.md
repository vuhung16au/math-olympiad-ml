# Architecture

This project runs as a dual-target system:

- publishable fractal package
- Next.js web application
- Tech stack details: see `docs/techstack.md`
- Fractal applications: see `docs/use-cases.md`
- Getting started: see `README.md` and `QUICKSTART.md`

```mermaid
flowchart LR
  user[UserBrowser] --> ui[NextJsUI]
  ui --> api[NextJsApiRoutes]
  ui --> core[SharedFractalCore]
  api --> core
  core --> packageOut[lib_and_esm_outputs]
  ui --> canvas[CanvasRenderer]
```

## Modules

- `src/`: package core (`IFS`, `LSystem`, types)
- `app/`: Next.js UI and API routes
- `scripts/`: artifact generation + Playwright sweep
- `docs/`: architecture, stack, use-cases, math notes

## API Contract

- `POST /api/render`
  - request: family + preset + params + width/height
  - response: image pixel array + render metadata
- `GET /api/v1/[family]/[preset]`
  - response: PNG bytes (`image/png`)
  - supports all families and all presets from `/api/presets`
  - query params:
    - `width`, `height` in pixels (default `1280x720`)
    - `backgroundColor` (default `white`, supports `white`, `black`, hex like `#0f172a`)
    - `mainColorScheme` (default `acu`, supported: `acu`, `matrix`, `emerald`, `ink`)
    - family-specific params (for example `etMaxIterations`, `ifsIterations`, `lsIterations`)
  - errors:
    - `400` invalid width/height
    - `404` unknown family or preset

## Rendering Flow (`/api/v1`)

```mermaid
flowchart LR
  request[HttpGetRequest] --> route[V1RouteHandler]
  route --> family[FamilyResolver]
  route --> preset[PresetLookup]
  route --> renderer[SharedRenderer]
  renderer --> encoder[PngEncoder]
  encoder --> response[PngHttpResponse]
```

## Boundaries

- Keep package logic reusable and independent of Next.js runtime details.
- Keep web UI focused on orchestration and rendering controls.
- Keep script automation stable for regression artifacts.
