#!/usr/bin/env bash
# Run make release where available. HSC-Viewer has no release target — skipped.

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=/dev/null
. "$SCRIPT_DIR/lib-hsc-booklets.sh"

failed=()

echo "Repo root: $HSC_REPO_ROOT"
echo ""

for name in "${HSC_BOOKLETS[@]}"; do
	dir="$HSC_REPO_ROOT/$name"
	printf '==> %-30s ' "$name"

	if [[ "$name" == "HSC-Viewer" ]]; then
		echo "SKIP (no release target)"
		continue
	fi

	if [[ ! -d "$dir" ]]; then
		echo "SKIP (missing directory)"
		failed+=("$name (missing dir)")
		continue
	fi
	if [[ ! -f "$dir/Makefile" ]]; then
		echo "SKIP (no Makefile)"
		continue
	fi

	echo "make release"
	if (cd "$dir" && make release); then
		echo "    OK"
	else
		echo "    FAIL"
		failed+=("$name")
	fi
	echo ""
done

if ((${#failed[@]})); then
	echo "Failures (${#failed[@]}):"
	for x in "${failed[@]}"; do echo "  - $x"; done
	exit 1
fi

echo "All release targets succeeded."
exit 0
