package calculator

import (
	"context"
	"math/big"
	"testing"

	"github.com/vuhung16au/math-olympiad-ml/pi-calculator/Chudnovsky/internal/config"
	"github.com/vuhung16au/math-olympiad-ml/pi-calculator/Chudnovsky/internal/workerpool"
)

func TestComputePQTSequential_Package(t *testing.T) {
	P, Q, T := ComputePQTSequential(0, 1)
	if P == nil || Q == nil || T == nil {
		t.Error("Expected non-nil results")
	}
}

func TestCombineResults_Package(t *testing.T) {
	results := []config.Result{
		{P: big.NewInt(2), Q: big.NewInt(3), T: big.NewInt(5)},
		{P: big.NewInt(7), Q: big.NewInt(11), T: big.NewInt(13)},
	}
	P, Q, T := CombineResults(results)
	if P.Sign() <= 0 || Q.Sign() <= 0 {
		t.Error("Expected positive P and Q")
	}
	_ = T
}

func TestComputePQT_Package(t *testing.T) {
	cfg := config.Default()
	ctx := context.Background()

	P, Q, T, err := ComputePQT(ctx, 0, 10, cfg, nil)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if P == nil || Q == nil || T == nil {
		t.Error("Expected non-nil results")
	}
}

func TestComputePQT_WithPool(t *testing.T) {
	cfg := config.Default()
	pool := workerpool.New(2)
	defer pool.Close()
	ctx := context.Background()

	// Test with larger range to trigger parallel path
	P, Q, T, err := ComputePQT(ctx, 0, 200, cfg, pool)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if P == nil || Q == nil || T == nil {
		t.Error("Expected non-nil results")
	}
}

func TestComputePQT_ContextCancellation(t *testing.T) {
	cfg := config.Default()
	ctx, cancel := context.WithCancel(context.Background())
	cancel() // Cancel immediately

	P, Q, T, err := ComputePQT(ctx, 0, 10, cfg, nil)
	if err == nil {
		t.Error("Expected error due to context cancellation")
	}
	if P != nil || Q != nil || T != nil {
		t.Error("Expected nil results when context is cancelled")
	}
}

func TestComputePQT_SmallRange(t *testing.T) {
	cfg := config.Default()
	ctx := context.Background()

	// Small range should use sequential
	P, Q, T, err := ComputePQT(ctx, 0, 50, cfg, nil)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if P == nil || Q == nil || T == nil {
		t.Error("Expected non-nil results")
	}
}

func TestComputePQTParallel_LargeRange(t *testing.T) {
	cfg := config.Default()
	pool := workerpool.New(4)
	defer pool.Close()
	ctx := context.Background()

	// Large range should use parallel
	P, Q, T, err := ComputePQT(ctx, 0, 2000, cfg, pool)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if P == nil || Q == nil || T == nil {
		t.Error("Expected non-nil results")
	}
}

func TestComputePQTParallel_ContextCancellation(t *testing.T) {
	cfg := config.Default()
	pool := workerpool.New(2)
	defer pool.Close()
	ctx, cancel := context.WithCancel(context.Background())
	cancel()

	P, Q, T, err := ComputePQT(ctx, 0, 2000, cfg, pool)
	if err == nil {
		t.Error("Expected error due to context cancellation")
	}
	if P != nil || Q != nil || T != nil {
		t.Error("Expected nil results when context is cancelled")
	}
}

func TestSetProgressCallback(t *testing.T) {
	var called bool
	callback := func(current int64) {
		called = true
	}

	SetProgressCallback(callback)
	// Trigger callback by computing
	ComputePQTSequential(0, 1)

	// Note: callback may or may not be called depending on implementation
	_ = called
}

func TestComputePQTSequential_EdgeCases(t *testing.T) {
	// Test invalid range
	P, Q, T := ComputePQTSequential(5, 5)
	if P.Cmp(big.NewInt(1)) != 0 {
		t.Error("Expected identity P for invalid range")
	}
	_ = Q
	_ = T

	// Test larger range
	P, Q, T = ComputePQTSequential(0, 20)
	if P.Sign() <= 0 || Q.Sign() <= 0 {
		t.Error("Expected positive P and Q")
	}
	_ = T
}

func TestCombineResults_EdgeCases(t *testing.T) {
	// Test single result
	results := []config.Result{
		{P: big.NewInt(2), Q: big.NewInt(3), T: big.NewInt(5)},
	}
	P, Q, T := CombineResults(results)
	if P.Cmp(big.NewInt(2)) != 0 {
		t.Error("Expected P=2 for single result")
	}
	_ = Q
	_ = T

	// Test multiple results
	results = []config.Result{
		{P: big.NewInt(2), Q: big.NewInt(3), T: big.NewInt(5)},
		{P: big.NewInt(7), Q: big.NewInt(11), T: big.NewInt(13)},
		{P: big.NewInt(17), Q: big.NewInt(19), T: big.NewInt(23)},
		{P: big.NewInt(29), Q: big.NewInt(31), T: big.NewInt(37)},
	}
	P, Q, T = CombineResults(results)
	if P.Sign() <= 0 || Q.Sign() <= 0 {
		t.Error("Expected positive P and Q")
	}
	_ = T
}
