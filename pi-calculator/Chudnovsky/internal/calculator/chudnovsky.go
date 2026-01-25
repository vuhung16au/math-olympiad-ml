package calculator

import (
	"context"
	"fmt"
	"math/big"
	"runtime"

	"github.com/vuhung16au/math-olympiad-ml/pi-calculator/Chudnovsky/internal/config"
)

// Calculator implements the Chudnovsky algorithm for computing π (pi).
// It provides a high-level interface for computing π to arbitrary precision
// using the fastest known algorithm.
type Calculator struct {
	cfg  *config.Config
	pool PoolInterface
}

// New creates a new Chudnovsky calculator with the given configuration.
// The pool parameter can be nil to use sequential computation only.
func New(cfg *config.Config, pool PoolInterface) *Calculator {
	return &Calculator{
		cfg:  cfg,
		pool: pool,
	}
}

// ComputePi computes π to the specified number of digits.
// It returns the formatted π string and any error encountered.
//
// Parameters:
//   - ctx: Context for cancellation support
//   - digits: Number of decimal digits to compute (must be between 1 and MaxDigits)
//
// Returns:
//   - string: The computed π value as a formatted string
//   - error: Error if computation fails, input is invalid, or context is cancelled
func (c *Calculator) ComputePi(ctx context.Context, digits int64) (string, error) {
	// Validate input
	if digits < 1 {
		return "", fmt.Errorf("digits must be at least 1, got %d", digits)
	}
	if digits > c.cfg.MaxDigits {
		return "", fmt.Errorf("digits exceeds maximum allowed (%d), got %d", c.cfg.MaxDigits, digits)
	}

	// Calculate precision and terms
	prec := uint(float64(digits) * c.cfg.BitsPerDigit)
	terms := digits/c.cfg.DigitsPerTerm + 1

	// Compute P, Q, T
	_, Q, T, err := ComputePQT(ctx, 0, terms, c.cfg, c.pool)
	if err != nil {
		return "", fmt.Errorf("failed to compute PQT: %w", err)
	}

	// Final Calculation: pi = (426880 * sqrt(10005) * Q) / T
	bigQ := new(big.Float).SetInt(Q)
	bigT := new(big.Float).SetInt(T)

	valE := new(big.Float).SetPrec(prec).SetInt64(10005)
	sqrtE := new(big.Float).SetPrec(prec).Sqrt(valE)

	multi := new(big.Float).SetPrec(prec).SetInt64(426880)
	num := new(big.Float).SetPrec(prec).Mul(multi, sqrtE)
	num.Mul(num, bigQ)

	pi := new(big.Float).SetPrec(prec).Quo(num, bigT)

	// Format pi as string
	piStr := fmt.Sprintf("%.*f", int(digits), pi)
	return piStr, nil
}

// GetNumCPU returns the number of CPU cores available.
// It ensures at least 1 CPU is returned even if detection fails.
func GetNumCPU() int {
	numCPU := runtime.NumCPU()
	if numCPU < 1 {
		return 1
	}
	return numCPU
}
