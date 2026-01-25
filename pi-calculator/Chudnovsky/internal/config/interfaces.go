package config

import (
	"context"
	"math/big"
)

// PiCalculator defines the interface for computing π (pi).
// This interface allows for different implementations and better testability.
type PiCalculator interface {
	Compute(ctx context.Context, digits int64) (string, error)
}

// ProgressReporter defines the interface for reporting computation progress.
// Implementations can provide visual feedback during long-running calculations.
type ProgressReporter interface {
	Update(current, total int64)
	Finish()
	SetDescription(desc string)
}

// Result represents a PQT computation result from the Chudnovsky algorithm.
// P, Q, and T are the three values computed for each term in the series.
type Result struct {
	P, Q, T *big.Int
}

// PQTComputer defines the interface for computing PQT values.
// This abstraction allows for different computation strategies (sequential, parallel, etc.).
type PQTComputer interface {
	ComputePQT(ctx context.Context, a, b int64) (P, Q, T *big.Int)
}
