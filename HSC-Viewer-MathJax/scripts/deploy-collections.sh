#!/bin/sh
set -eu

BOOKLET_HTML=".generated/booklets/hsc-collections.html"

if [ ! -f "$BOOKLET_HTML" ]; then
  echo "Missing $BOOKLET_HTML" >&2
  echo "Generate the real HTML first:" >&2
  echo "  make generate-html-one BOOKLET=HSC-Collections" >&2
  exit 1
fi

if rg -q "Generated fallback" "$BOOKLET_HTML"; then
  echo "Refusing to deploy fallback HTML for HSC-Collections." >&2
  echo "Regenerate the booklet with a long timeout first:" >&2
  echo "  make generate-html-one BOOKLET=HSC-Collections" >&2
  exit 1
fi

echo "Building a prebuilt deployment for HSC-Collections only."
VISIBLE_BOOKLETS=hsc-collections bunx vercel build --prod

echo "Deploying the prebuilt output to Vercel."
bunx vercel deploy --prebuilt --prod --env VISIBLE_BOOKLETS=hsc-collections
