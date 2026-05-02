#!/usr/bin/env sh
# Build and copy each HSC booklet PDF to its releases/ directory.
# Repo root is two levels above this script (HSC-Viewer/scripts → …).

set -eu

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT" || exit 1

DIRS='
HSC-Collections
HSC-Combinatorics
HSC-ComplexNumbers
HSC-DifferentialEquations
HSC-Distributions
HSC-Functions
HSC-Induction
HSC-Inequalities
HSC-Integrals
HSC-LastResorts
HSC-Mechanics
HSC-Polynomials
HSC-Polynomials-Extension1
HSC-Probability
HSC-Proofs
HSC-Sequences
HSC-Trigonometry
HSC-Vectors
HSC-Viewer
'

for d in $DIRS; do
	echo ""
	echo "==========> ${d}"

	cd "${ROOT}/${d}" || exit 1
	if ! [ -f Makefile ]; then
		echo "error: missing Makefile in ${d}" >&2
		exit 1
	fi

	if grep -q '^pdf:' Makefile && grep -q '^release:' Makefile; then
		make clean && make pdf && make release
	elif grep -q '^clean:' Makefile; then
		echo "notice: ${d} has no pdf/release targets (e.g. web viewer) — running make clean only."
		make clean
	else
		echo "error: ${d} Makefile has no pdf, release, or clean targets" >&2
		exit 1
	fi

	cd "$ROOT" || exit 1
done

echo ""
echo "All requested directories processed."
