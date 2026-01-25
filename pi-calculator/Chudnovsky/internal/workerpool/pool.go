// Package workerpool provides a worker pool implementation for parallel computation.
// It efficiently distributes work across multiple goroutines to utilize all CPU cores.
package workerpool

import (
	"context"
	"runtime"
	"sync"

	"github.com/vuhung16au/math-olympiad-ml/pi-calculator/Chudnovsky/internal/config"
)

// Pool manages parallel computation using a worker pool pattern.
// It distributes work across multiple goroutines for efficient CPU utilization.
// The pool is thread-safe and supports graceful shutdown.
type Pool struct {
	workers    int
	wg         sync.WaitGroup
	ctx        context.Context
	cancel     context.CancelFunc
	closed     bool
	closeMutex sync.Mutex
}

// New creates a new worker pool with the specified number of workers.
// If workers is 0 or negative, it defaults to the number of CPU cores.
//
// Parameters:
//   - workers: Number of worker goroutines (0 = auto-detect from CPU count)
//
// Returns a new Pool instance ready to accept work.
func New(workers int) *Pool {
	if workers <= 0 {
		workers = runtime.NumCPU()
		if workers < 1 {
			workers = 1
		}
	}

	ctx, cancel := context.WithCancel(context.Background())
	wp := &Pool{
		workers: workers,
		ctx:     ctx,
		cancel:  cancel,
	}

	return wp
}

// Submit submits work to the pool and returns a channel to receive the result.
// The computeFn will be executed in a goroutine to distribute work across cores.
//
// Parameters:
//   - start: Start index (inclusive) for computation
//   - end: End index (exclusive) for computation
//   - computeFn: Function to execute for the given range
//
// Returns a channel that will receive the computation result.
// The channel will be closed if the pool is closed.
func (wp *Pool) Submit(start, end int64, computeFn func(a, b int64) config.Result) <-chan config.Result {
	resultChan := make(chan config.Result, 1)

	// Check if pool is closed
	wp.closeMutex.Lock()
	closed := wp.closed
	wp.closeMutex.Unlock()

	if closed {
		close(resultChan)
		return resultChan
	}

	// Execute computation in a goroutine for parallelism
	wp.wg.Add(1)
	go func() {
		defer wp.wg.Done()
		select {
		case <-wp.ctx.Done():
			close(resultChan)
			return
		default:
			result := computeFn(start, end)
			resultChan <- result
		}
	}()

	return resultChan
}

// Close shuts down the worker pool (idempotent).
// It signals all workers to stop and waits for them to finish.
// Safe to call multiple times.
func (wp *Pool) Close() {
	if wp == nil {
		return
	}
	wp.closeMutex.Lock()
	defer wp.closeMutex.Unlock()

	if wp.closed {
		return // Already closed
	}
	wp.closed = true

	wp.cancel()  // Signal workers to stop first
	wp.wg.Wait() // Wait for all workers to finish
}
