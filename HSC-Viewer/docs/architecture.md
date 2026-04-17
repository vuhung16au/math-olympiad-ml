# Architecture Notes

## Rendering Model

The app uses the Next.js App Router with a mostly static output:
- `/` renders the booklet library grid
- `/booklets/[slug]` is statically generated for every available booklet
- PDF rendering happens client-side with `react-pdf`

## Data Source

Booklet metadata lives in `lib/booklets.ts`.
Each PDF is loaded from the raw GitHub URL for the corresponding release artifact.

## UI Structure

- `components/layout/*` contains the shared shell
- `components/pages/GridView.tsx` renders the home library
- `components/pages/PDFViewer.tsx` renders the active PDF reader
- `components/ui/*` contains reusable controls and states

## Analytics

Vercel Analytics handles:
- automatic page views
- custom booklet open events
- page navigation, zoom, print, download, and fullscreen actions

## Thumbnail Strategy

Thumbnails are generated offline with `scripts/generate-thumbnails.js` and stored in `public/thumbnails/`.
If an image is missing, the UI falls back to a styled placeholder card.
