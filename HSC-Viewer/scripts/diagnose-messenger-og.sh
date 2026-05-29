#!/usr/bin/env bash
# Quick checks when Sharing Debugger works but Messenger shows only the domain.
set -euo pipefail

PAGE_URL="${1:-https://hsc-math-hub.vercel.app/booklets/hsc-functions/57?m=6}"
UA='facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)'

echo "=== Page HTML (og:image) ==="
curl -sSL -A "$UA" "$PAGE_URL" | rg 'property="og:(image|title|url)"' | head -6

echo ""
echo "=== OG image HEAD (from og:image in HTML) ==="
IMG="$(curl -sSL -A "$UA" "$PAGE_URL" | rg -o 'property="og:image" content="[^"]+"' | head -1 | sed 's/.*content="//;s/"$//')"
if [[ -n "$IMG" ]]; then
  curl -sSIL -A "$UA" "$IMG" | rg -i '^(HTTP/|content-type:|content-length:|x-vercel-cache:|x-og-renderer:)'
else
  echo "No og:image found"
fi

echo ""
echo "=== Static thumbnail on site ==="
curl -sSIL -A "$UA" "https://hsc-math-hub.vercel.app/thumbnails/hsc-functions.png" | head -5

echo ""
echo "=== GitHub-hosted thumbnail (og:image mode=github) ==="
curl -sSIL -A "$UA" \
  "https://raw.githubusercontent.com/vuhung16au/math-olympiad-ml/main/HSC-Viewer/public/thumbnails/hsc-functions.png" | head -5

echo ""
echo "Manual checks:"
echo "  1. In Messenger, send https://www.apple.com — if no rich preview, likely EU/account limits."
echo "  2. Send the same HSC link in WhatsApp — if WhatsApp is rich but Messenger is not, likely Messenger/EU."
echo "  3. Vercel → Project → Firewall → check for blocked facebookexternalhit."
echo "  4. Set NEXT_PUBLIC_OG_IMAGE_MODE=github in Vercel, redeploy, scrape, retry Messenger."
