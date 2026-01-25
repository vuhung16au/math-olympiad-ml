// Package calculator implements the Chudnovsky algorithm for computing π (pi) to arbitrary precision.
// The Chudnovsky algorithm is the fastest known method for computing π to high precision,
// producing approximately 14 decimal digits per term using binary splitting.
package calculator

import (
	"context"
	"math/big"
	"runtime"
	"sync/atomic"

	"github.com/vuhung16au/math-olympiad-ml/pi-calculator/Chudnovsky/internal/config"
)

// ProgressCallback is a function type for reporting computation progress.
// It is called with the current number of terms computed.
type ProgressCallback func(current int64)

var (
	// progressCallback is set by the calculator to report progress
	progressCallback ProgressCallback
	progressCounter  int64
)

// SetProgressCallback sets the callback function for progress updates.
// The callback will be invoked each time a term is computed.
func SetProgressCallback(callback ProgressCallback) {
	progressCallback = callback
}

// Result represents a PQT computation result from the Chudnovsky algorithm.
type Result = config.Result

// CombineResults combines multiple PQT results in a binary tree fashion.
// This is used to merge partial results from parallel computation.
// The function recursively splits the results array and combines them,
// ensuring efficient merging of parallel computation results.
//
//nolint:gocritic // P, Q, T are exported return values, capitalization is intentional
func CombineResults(results []Result) (P, Q, T *big.Int) {
	if len(results) == 1 {
		return results[0].P, results[0].Q, results[0].T
	}
	if len(results) == 2 {
		P = new(big.Int).Mul(results[0].P, results[1].P)
		Q = new(big.Int).Mul(results[0].Q, results[1].Q)
		T = new(big.Int).Add(
			new(big.Int).Mul(results[1].Q, results[0].T),
			new(big.Int).Mul(results[0].P, results[1].T),
		)
		return P, Q, T
	}

	// Split in half and combine recursively
	mid := len(results) / 2
	p1, q1, t1 := CombineResults(results[:mid])
	p2, q2, t2 := CombineResults(results[mid:])

	P = new(big.Int).Mul(p1, p2)
	Q = new(big.Int).Mul(q1, q2)
	T = new(big.Int).Add(
		new(big.Int).Mul(q2, t1),
		new(big.Int).Mul(p1, t2),
	)
	return P, Q, T
}

// ComputePQTSequential computes P, Q, T values sequentially using binary splitting.
// This is the base computation function used by workers.
// It implements the Chudnovsky algorithm's recursive computation.
//
// Parameters:
//   - a: Start index (inclusive)
//   - b: End index (exclusive)
//
// Returns:
//   - P, Q, T: The computed values for the Chudnovsky series
//
//nolint:gocritic // P, Q, T are exported return values, capitalization is intentional
func ComputePQTSequential(a, b int64) (P, Q, T *big.Int) {
	// Safety check: ensure valid range
	if a >= b {
		return big.NewInt(1), big.NewInt(1), big.NewInt(0)
	}

	if b-a == 1 {
		// Update progress for base case
		if progressCallback != nil {
			atomic.AddInt64(&progressCounter, 1)
			progressCallback(atomic.LoadInt64(&progressCounter))
		}
		P = big.NewInt(1)
		Q = big.NewInt(1)
		if a > 0 {
			// P = (6a-5)(2a-1)(6a-1)
			p1 := big.NewInt(6*a - 5)
			p2 := big.NewInt(2*a - 1)
			p3 := big.NewInt(6*a - 1)
			P.Mul(p1, p2).Mul(P, p3)

			// Q = a^3 * C^3 / 24
			a3 := new(big.Int).Mul(big.NewInt(a*a), big.NewInt(a))
			Q.Mul(a3, C3).Div(Q, big.NewInt(24))
		}
		// T = P * (A + Ba)
		term := new(big.Int).Mul(B, big.NewInt(a))
		term.Add(term, A)
		T = new(big.Int).Mul(P, term)
		if a%2 == 1 {
			T.Neg(T)
		}
		// Yield frequently to allow scheduler to switch
		if a%50 == 0 {
			runtime.Gosched()
		}
		return P, Q, T
	}

	// For sequential computation, split recursively
	mid := (a + b) / 2
	p1, q1, t1 := ComputePQTSequential(a, mid)
	p2, q2, t2 := ComputePQTSequential(mid, b)
	P = new(big.Int).Mul(p1, p2)
	Q = new(big.Int).Mul(q1, q2)
	T = new(big.Int).Add(new(big.Int).Mul(q2, t1), new(big.Int).Mul(p1, t2))
	return P, Q, T
}

// ComputePQT computes P, Q, T values using parallel computation when beneficial.
// It automatically chooses between sequential and parallel computation based on
// the range size and available worker pool.
//
// Parameters:
//   - ctx: Context for cancellation support
//   - a: Start index (inclusive)
//   - b: End index (exclusive)
//   - cfg: Configuration containing computation parameters
//   - pool: Worker pool interface for parallel computation (can be nil for sequential)
//
// Returns:
//   - P, Q, T: The computed values
//   - err: Error if computation fails or context is cancelled
//
//nolint:gocritic // P, Q, T are exported return values, capitalization is intentional
func ComputePQT(ctx context.Context, a, b int64, cfg *config.Config, pool PoolInterface) (P, Q, T *big.Int, err error) {
	rangeSize := b - a

	// Check context cancellation
	select {
	case <-ctx.Done():
		return nil, nil, nil, ctx.Err()
	default:
	}

	// Use worker pool for larger ranges, but ensure chunks are small enough
	if rangeSize > cfg.MinRangeForWorkerPool && pool != nil {
		return computePQTParallel(ctx, a, b, rangeSize, cfg, pool)
	}

	// For small ranges or if no worker pool, use sequential
	P, Q, T = ComputePQTSequential(a, b)
	return P, Q, T, nil
}

// PoolInterface defines the interface for worker pools
type PoolInterface interface {
	Submit(start, end int64, computeFn func(a, b int64) Result) <-chan Result
}

// computePQTParallel computes PQT using parallel worker pool
//
//nolint:gocritic // P, Q, T are return values, capitalization is intentional
func computePQTParallel(ctx context.Context, a, b, rangeSize int64, cfg *config.Config, pool PoolInterface) (P, Q, T *big.Int, err error) {
	// Calculate number of chunks - ensure each chunk is small enough to avoid deep recursion
	maxChunkSize := cfg.MaxChunkSize
	numChunks := int(rangeSize / maxChunkSize)
	if numChunks < 1 {
		numChunks = 1
	}
	// Cap at reasonable number
	if numChunks > 64 {
		numChunks = 64
	}

	// Ensure we have at least one valid chunk
	if numChunks < 1 {
		P, Q, T = ComputePQTSequential(a, b)
		return P, Q, T, nil
	}

	chunkSize := rangeSize / int64(numChunks)
	// Ensure chunkSize is at least 1
	if chunkSize < 1 {
		chunkSize = 1
		numChunks = int(rangeSize)
	}

	results := make([]Result, numChunks)
	resultChans := make([]<-chan Result, numChunks)

	// Submit all work items - ensure valid ranges
	for i := 0; i < numChunks; i++ {
		start := a + int64(i)*chunkSize
		end := start + chunkSize
		if i == numChunks-1 {
			end = b // Last chunk gets remainder
		}
		// Ensure valid range (start < end)
		if start >= end {
			end = start + 1
			if end > b {
				end = b
			}
		}
		if start < b {
			startCopy, endCopy := start, end
			resultChans[i] = pool.Submit(startCopy, endCopy, func(a, b int64) Result {
				p, q, t := ComputePQTSequential(a, b)
				return Result{P: p, Q: q, T: t}
			})
		} else {
			// Empty chunk - return identity
			identityChan := make(chan Result, 1)
			identityChan <- Result{P: big.NewInt(1), Q: big.NewInt(1), T: big.NewInt(0)}
			close(identityChan)
			resultChans[i] = identityChan
		}
	}

	// Collect results
	for i := 0; i < numChunks; i++ {
		select {
		case <-ctx.Done():
			return nil, nil, nil, ctx.Err()
		case results[i] = <-resultChans[i]:
		}
	}

	P, Q, T = CombineResults(results)
	return P, Q, T, nil
}
