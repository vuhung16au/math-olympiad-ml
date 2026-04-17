# HSC Math Hub Quickstart

## Run Locally

```bash
cd HSC-Viewer
make install
make dev
```

Open http://localhost:3000.

## Build

```bash
cd HSC-Viewer
make build
```

## Lint

```bash
cd HSC-Viewer
make lint
```

## Generate Thumbnails

```bash
cd HSC-Viewer
make thumbnails
```

This downloads each published PDF and renders the first page into `public/thumbnails/`.

Requirements:
- `convert` from ImageMagick must be installed and available in `PATH`
- network access to `raw.githubusercontent.com`

## Deploy To Vercel

```bash
cd HSC-Viewer
make deploy
```

`vercel` CLI is already installed in the current environment.

## Notes

- PDFs are loaded directly from `raw.githubusercontent.com` so browsers receive the correct content type.
- `HSC-Sequences` is intentionally disabled until its PDF exists under `releases/`.
- Vercel Analytics is enabled for page views and PDF interaction events.
