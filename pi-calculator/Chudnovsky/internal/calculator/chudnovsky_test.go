package calculator

import (
	"context"
	"testing"

	"github.com/vuhung16au/math-olympiad-ml/pi-calculator/Chudnovsky/internal/config"
	"github.com/vuhung16au/math-olympiad-ml/pi-calculator/Chudnovsky/internal/workerpool"
)

func TestCalculator_ComputePi(t *testing.T) {
	cfg := config.Default()
	calc := New(cfg, nil)
	ctx := context.Background()

	piStr, err := calc.ComputePi(ctx, 10)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}

	if len(piStr) < 10 {
		t.Errorf("Expected at least 10 characters, got %d", len(piStr))
	}
}

func TestCalculator_ComputePi_InvalidInput(t *testing.T) {
	cfg := config.Default()
	calc := New(cfg, nil)
	ctx := context.Background()

	// Test negative digits
	_, err := calc.ComputePi(ctx, -1)
	if err == nil {
		t.Error("Expected error for negative digits")
	}

	// Test zero digits
	_, err = calc.ComputePi(ctx, 0)
	if err == nil {
		t.Error("Expected error for zero digits")
	}

	// Test exceeding max
	_, err = calc.ComputePi(ctx, cfg.MaxDigits+1)
	if err == nil {
		t.Error("Expected error for exceeding max digits")
	}
}

func TestCalculator_ComputePi_WithPool(t *testing.T) {
	cfg := config.Default()
	pool := workerpool.New(2)
	defer pool.Close()
	calc := New(cfg, pool)
	ctx := context.Background()

	// Test with worker pool for larger calculation
	piStr, err := calc.ComputePi(ctx, 1000)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if len(piStr) < 1000 {
		t.Errorf("Expected at least 1000 characters, got %d", len(piStr))
	}
}

func TestCalculator_ComputePi_ContextCancellation(t *testing.T) {
	cfg := config.Default()
	calc := New(cfg, nil)
	ctx, cancel := context.WithCancel(context.Background())
	cancel() // Cancel immediately

	_, err := calc.ComputePi(ctx, 100)
	if err == nil {
		t.Error("Expected error due to context cancellation")
	}
}

func TestGetNumCPU(t *testing.T) {
	numCPU := GetNumCPU()
	if numCPU < 1 {
		t.Errorf("Expected at least 1 CPU, got %d", numCPU)
	}
}
