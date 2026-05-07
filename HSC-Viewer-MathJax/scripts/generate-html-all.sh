#!/bin/sh
set -eu

TIMEOUT_MS="${TIMEOUT_MS:-600000}"

echo "Running full HTML conversion for all booklets with MAKE4HT_TIMEOUT_MS=${TIMEOUT_MS}."
MAKE4HT_TIMEOUT_MS="${TIMEOUT_MS}" bun scripts/generate-booklets.ts
