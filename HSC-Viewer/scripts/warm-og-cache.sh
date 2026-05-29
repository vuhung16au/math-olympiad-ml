#!/usr/bin/env bash
# Pre-warm OG PNGs on Vercel CDN so Messenger's first scrape is fast.
set -euo pipefail

BASE="${OG_WARM_BASE_URL:-https://hsc-math-hub.vercel.app}"
UA="facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)"
VERSION="${OG_IMAGE_VERSION:-6}"

warm() {
  local path="$1"
  local code
  code="$(curl -sS -o /dev/null -w "%{http_code}" -A "$UA" "${BASE}${path}")"
  echo "${code} ${path}"
}

warm "/og/preview-${VERSION}/booklets/hsc-functions/57.png"
warm "/booklets/hsc-functions/57?m=${VERSION}"
