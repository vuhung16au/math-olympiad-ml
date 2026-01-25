package calculator

import (
	"context"
	"testing"
	"time"

	"github.com/vuhung16au/math-olympiad-ml/pi-calculator/Chudnovsky/internal/config"
	"github.com/vuhung16au/math-olympiad-ml/pi-calculator/Chudnovsky/internal/workerpool"
)

func BenchmarkComputePQTSequential(b *testing.B) {
	b.ResetTimer()
	start := time.Now()

	for i := 0; i < b.N; i++ {
		ComputePQTSequential(0, 1000)
	}

	elapsed := time.Since(start)
	b.Logf("Execution time: %v, Avg: %v per iteration", elapsed, elapsed/time.Duration(b.N))
}

func BenchmarkComputePQTParallel(b *testing.B) {
	cfg := config.Default()
	pool := workerpool.New(4)
	defer pool.Close()
	ctx := context.Background()

	b.ResetTimer()
	start := time.Now()

	for i := 0; i < b.N; i++ {
		_, _, _, err := ComputePQT(ctx, 0, 1000, cfg, pool)
		if err != nil {
			b.Fatalf("Unexpected error: %v", err)
		}
	}

	elapsed := time.Since(start)
	b.Logf("Execution time: %v, Avg: %v per iteration", elapsed, elapsed/time.Duration(b.N))
}

func BenchmarkCombineResults(b *testing.B) {
	results := make([]config.Result, 10)
	for i := range results {
		results[i] = config.Result{
			P: nil, Q: nil, T: nil, // Placeholder
		}
	}

	b.ResetTimer()
	start := time.Now()

	for i := 0; i < b.N; i++ {
		CombineResults(results)
	}

	elapsed := time.Since(start)
	b.Logf("Execution time: %v, Avg: %v per iteration", elapsed, elapsed/time.Duration(b.N))
}
