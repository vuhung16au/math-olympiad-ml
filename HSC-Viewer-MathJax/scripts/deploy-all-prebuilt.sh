#!/bin/sh
set -eu

MANIFEST=".generated/manifest.json"

if [ ! -f "$MANIFEST" ]; then
  echo "Missing $MANIFEST" >&2
  echo "Generate the booklet HTML first:" >&2
  echo "  TIMEOUT_MS=900000 make generate-html-all" >&2
  exit 1
fi

FALLBACK_FILES="$(
  bun -e '
    import fs from "node:fs";
    import { BOOKLETS } from "./lib/booklets";

    const visibleSlugs = new Set(
      BOOKLETS.filter((entry) => entry.isAvailable).map((entry) => entry.slug),
    );
    const manifest = JSON.parse(fs.readFileSync(".generated/manifest.json", "utf8"));
    const fallbackFiles = manifest
      .filter((entry) => visibleSlugs.has(entry.slug))
      .map((entry) => entry.htmlPath)
      .filter((filePath) => fs.existsSync(filePath))
      .filter((filePath) => fs.readFileSync(filePath, "utf8").includes("Generated fallback"));
    process.stdout.write(fallbackFiles.join("\n"));
  '
)"

if [ -n "$FALLBACK_FILES" ]; then
  echo "Refusing to deploy because some generated booklets are still fallback HTML." >&2
  echo "Fallback files:" >&2
  printf '%s\n' "$FALLBACK_FILES" >&2
  echo "Regenerate all booklets with a long timeout first:" >&2
  echo "  TIMEOUT_MS=900000 make generate-html-all" >&2
  exit 1
fi

echo "Building a prebuilt deployment for all booklets."
bunx vercel build --prod

echo "Deploying the prebuilt output to Vercel."
bunx vercel deploy --prebuilt --prod
