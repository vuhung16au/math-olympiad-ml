#!/bin/sh
set -eu

BOOKLET="${BOOKLET:-}"
TIMEOUT_MS="${TIMEOUT_MS:-600000}"

if [ -z "${BOOKLET}" ]; then
  echo "Usage: BOOKLET=HSC-Collections sh scripts/generate-html-one.sh" >&2
  exit 1
fi

echo "Running full HTML conversion for ${BOOKLET} with MAKE4HT_TIMEOUT_MS=${TIMEOUT_MS}."
BOOKLET="${BOOKLET}" MAKE4HT_TIMEOUT_MS="${TIMEOUT_MS}" bun scripts/generate-booklet.ts
