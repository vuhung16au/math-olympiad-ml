# Open Graph (OG) preview testing

This doc describes how to verify Open Graph preview cards for booklet pages.

## Known-good example URL

- `https://hsc-math-hub.vercel.app/booklets/hsc-last-resorts/97`

## Verify OG meta tags directly (HTML)

The OG tags must be present in the **initial HTML** response (server-rendered).

1. Fetch the HTML for the example URL.
2. Confirm the HTML contains (at minimum) the following meta tags:
   - `og:title`
   - `og:description`
   - `og:url`
   - `og:image`
   - `og:type`
   - `og:site_name`
   - `og:image:width` (1200)
   - `og:image:height` (630)

Also confirm:
- `og:image` is an **absolute** URL and matches the shape:
  - `https://hsc-math-hub.vercel.app/og/booklets/hsc-<booklet-name>/<page-number>.png`

## Facebook

1. Open Facebook Sharing Debugger.
2. Paste the example URL and request a re-scrape.

Success criteria:
- Preview shows the expected title and description.
- Preview image loads (no broken image).
- No warnings about missing required OG tags.

## Discord

1. Paste the example URL into a test channel.
2. Confirm Discord unfurls the card with:
   - Title
   - Description
   - Image

### Cache refresh notes (Discord)

Discord caches link previews. If you update the image generator or want Discord to fetch a new image:

- Do **not** change the page URL.
- Force a new image by changing the `og:image` URL (for example by adding a version query string like `?v=2`), or by bumping route versioning for the image endpoint.

