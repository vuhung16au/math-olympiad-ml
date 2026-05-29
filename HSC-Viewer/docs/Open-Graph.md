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
  - Dynamic (default): `https://hsc-math-hub.vercel.app/og/preview-<version>/booklets/hsc-<booklet-name>/<page-number>.png`
  - Static test mode: `/thumbnails/hsc-<booklet-name>.png` or a `raw.githubusercontent.com` URL

## Facebook Sharing Debugger

1. Open [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/).
2. Paste the booklet **page** URL (not the `/og/...png` image URL).
3. Click **Scrape Again** until the preview shows title, description, and image.

Success criteria:
- Preview shows the expected title and description.
- Preview image loads (no broken image).
- `og:image`, `og:image:secure_url`, and `og:image:type` (`image/png`) are present.

## Messenger: Sharing Debugger OK, chat shows only the domain

This pattern is **common** and often **not fixable in app code alone**.

### What we know works on this site

- Server-rendered OG tags on the page URL
- Sharing Debugger shows the full card
- Facebook **Page** composer shows the full card
- **Discord** shows the full card

So Meta’s crawler **can** read the site. Messenger DMs use a **separate** link-preview path; a gray box with only `hsc-math-hub.vercel.app` usually means Messenger did **not** attach the scraped card to that message.

### Step 1 — Rule out Meta account / region limits (5 minutes)

1. In the **same** Messenger chat, send `https://www.apple.com` (link only).
2. In the **same** chat, send a `https://www.youtube.com/watch?v=…` link.

| apple.com | YouTube | Typical meaning |
|-----------|---------|-----------------|
| Domain only (gray strip) | Full card (image + title) | **Messenger DMs are not applying generic Open Graph unfurl** for normal websites. Your site will behave like apple.com, not like broken tags. YouTube is a **special case** (native/partner preview), not proof that OG works for any URL. |
| Rich preview | Rich preview | Meta can unfurl generic URLs in your account; continue Steps 2–3 for site-specific issues. |
| Domain only | Domain only | All generic links degraded — often [EU/UK/EEA ePrivacy](https://mysk.blog/2021/02/08/fb-link-previews/) **or** account/client issue. |

If you match the first row (including in **Australia**), **no site change will fix Messenger DMs** for HSC Math Hub. Apple’s homepage has valid `og:image` tags; if Messenger still shows only the domain, the limit is on Meta’s side. Use Discord, Facebook Page posts, or paste title + screenshot in Messenger.

**Australia note:** EU privacy rules are not the only explanation. Sydney-based users have reported the same apple.com / YouTube split — that points to **Messenger’s DM preview pipeline** (or your client/account), not your site’s metadata.

2. Send the HSC link in **WhatsApp** (same URL).
   - **Rich in WhatsApp, not Messenger** → Messenger-specific; try Step 2–3.
   - **Domain-only in both** → likely region/crawler block; check EU and Vercel Firewall.

### Step 2 — Server checks

```bash
./scripts/diagnose-messenger-og.sh "https://hsc-math-hub.vercel.app/booklets/hsc-functions/57?m=6"
./scripts/warm-og-cache.sh
```

In Vercel: **Project → Firewall → Observability** — look for **403** or **challenge** on `facebookexternalhit` when you send a link in Messenger (not only when you use the debugger).

### Step 3 — A/B test og:image hosting (Vercel env)

In Vercel → Settings → Environment Variables, set:

| Variable | Value | Purpose |
|----------|--------|---------|
| `NEXT_PUBLIC_OG_IMAGE_MODE` | `github` | og:image points at `raw.githubusercontent.com` (static PNG, not serverless) |
| `NEXT_PUBLIC_OG_IMAGE_MODE` | `static` | og:image = `/thumbnails/{slug}.png` on your site |
| (unset) | `dynamic` | Per-page generated PNG (default; best for Discord / FB Pages) |

Redeploy, **Scrape Again** in the debugger, then send in a **new** Messenger chat:

`https://hsc-math-hub.vercel.app/booklets/hsc-functions/57?m=6`

- If **`github` or `static` fixes Messenger** but `dynamic` does not → Messenger is failing on the dynamic `/og/...` fetch (timeout or edge block). Use a **custom domain** and/or keep static covers for Messenger until images are pre-generated to static files.
- If **nothing fixes Messenger** but apple.com works → treat as Meta-side limitation for this account/region.

### Step 4 — Custom domain (recommended for production)

Rich Messenger previews are more reliable on a **custom domain** than on `*.vercel.app`. After adding e.g. `hscmathhub.com` in Vercel:

1. Set `NEXT_PUBLIC_SITE_URL=https://hscmathhub.com`
2. Redeploy, scrape the new URL in the debugger, test Messenger again.

### Optional env vars

- `NEXT_PUBLIC_FB_APP_ID` — clears Sharing Debugger “missing fb:app_id” warning.
- `NEXT_PUBLIC_SITE_URL` — canonical / og:url base when not using `hsc-math-hub.vercel.app`.

When the OG image generator or layout changes, bump `OG_IMAGE_VERSION` in `lib/og-metadata.ts`.

## Discord

1. Paste the example URL into a test channel.
2. Confirm Discord unfurls the card with title, description, and image.

Discord caches aggressively; change `og:image` path version (`OG_IMAGE_VERSION`) to force a new fetch.
