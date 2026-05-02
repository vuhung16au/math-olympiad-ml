# Shared list of HSC booklet / project dirs (relative to repo root).
# shellcheck disable=SC2034 # sourced by sibling scripts

_LIB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
readonly HSC_REPO_ROOT="$(cd "$_LIB_DIR/../.." && pwd)"
unset _LIB_DIR

HSC_BOOKLETS=(
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
	HSC-Math-Extension-2-Book
	HSC-Mechanics
	HSC-Polynomials
	HSC-Polynomials-Extension1
	HSC-Probability
	HSC-Proofs
	HSC-Sequences
	HSC-Trigonometry
	HSC-Vectors
)
