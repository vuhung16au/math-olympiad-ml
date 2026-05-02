#!/usr/bin/env bash
# Run a full rebuild (clean then primary build) for every HSC-* booklet/project.
# LaTeX booklets: make clean && make pdf. HSC-Viewer (Next.js): make clean && make build.

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
	if [[ ! -d "$dir" ]]; then
		echo "SKIP (missing directory)"
		failed+=("$name (missing dir)")
		continue
	fi
	if [[ ! -f "$dir/Makefile" ]]; then
		echo "SKIP (no Makefile)"
		failed+=("$name (no Makefile)")
		continue
	fi

	if [[ "$name" == "HSC-Viewer" ]]; then
		echo "(clean + build)"
		if (cd "$dir" && make clean && make build); then
			echo "    OK"
		else
			echo "    FAIL"
			failed+=("$name")
		fi
	else
		echo "(clean + pdf)"
		if (cd "$dir" && make clean && make pdf); then
			echo "    OK"
		else
			echo "    FAIL"
			failed+=("$name")
		fi
	fi
	echo ""
done

if ((${#failed[@]})); then
	echo "Failures (${#failed[@]}):"
	for x in "${failed[@]}"; do echo "  - $x"; done
	exit 1
fi

echo "All booklet builds succeeded."
exit 0
