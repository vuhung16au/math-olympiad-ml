package main

import (
	"context"
	"math/big"
	"os"
	"path/filepath"
	"strings"
	"testing"
	"time"

	"github.com/vuhung16au/math-olympiad-ml/pi-calculator/Chudnovsky/internal/calculator"
	"github.com/vuhung16au/math-olympiad-ml/pi-calculator/Chudnovsky/internal/config"
	"github.com/vuhung16au/math-olympiad-ml/pi-calculator/Chudnovsky/internal/formatter"
	"github.com/vuhung16au/math-olympiad-ml/pi-calculator/Chudnovsky/internal/security"
	"github.com/vuhung16au/math-olympiad-ml/pi-calculator/Chudnovsky/internal/workerpool"
)

// TestComputePQTSequential tests the core computation logic
func TestComputePQTSequential(t *testing.T) {
	tests := []struct {
		name     string
		a        int64
		b        int64
		validate func(t *testing.T, P, Q, T *big.Int)
	}{
		{
			name: "Base case: a=0, b=1",
			a:    0,
			b:    1,
			validate: func(t *testing.T, P, Q, T *big.Int) {
				if P.Cmp(big.NewInt(1)) != 0 {
					t.Errorf("Expected P=1, got %s", P.String())
				}
				if Q.Cmp(big.NewInt(1)) != 0 {
					t.Errorf("Expected Q=1, got %s", Q.String())
				}
				// T should be A (13591409) for a=0
				expectedT := big.NewInt(13591409)
				if T.Cmp(expectedT) != 0 {
					t.Errorf("Expected T=%s, got %s", expectedT.String(), T.String())
				}
			},
		},
		{
			name: "Base case: a=1, b=2",
			a:    1,
			b:    2,
			validate: func(t *testing.T, P, Q, T *big.Int) {
				// P = (6*1-5)(2*1-1)(6*1-1) = 1 * 1 * 5 = 5
				expectedP := big.NewInt(5)
				if P.Cmp(expectedP) != 0 {
					t.Errorf("Expected P=5, got %s", P.String())
				}
				// Q should be positive
				if Q.Sign() <= 0 {
					t.Errorf("Expected Q > 0, got %s", Q.String())
				}
				// T should be negative (a=1 is odd)
				if T.Sign() >= 0 {
					t.Errorf("Expected T < 0 (a is odd), got %s", T.String())
				}
			},
		},
		{
			name: "Invalid range: a >= b",
			a:    5,
			b:    5,
			validate: func(t *testing.T, P, Q, T *big.Int) {
				if P.Cmp(big.NewInt(1)) != 0 {
					t.Errorf("Expected P=1 (identity), got %s", P.String())
				}
				if Q.Cmp(big.NewInt(1)) != 0 {
					t.Errorf("Expected Q=1 (identity), got %s", Q.String())
				}
				if T.Cmp(big.NewInt(0)) != 0 {
					t.Errorf("Expected T=0 (identity), got %s", T.String())
				}
			},
		},
		{
			name: "Small range: a=0, b=3",
			a:    0,
			b:    3,
			validate: func(t *testing.T, P, Q, T *big.Int) {
				// Should compute successfully
				if P.Sign() <= 0 {
					t.Errorf("Expected P > 0, got %s", P.String())
				}
				if Q.Sign() <= 0 {
					t.Errorf("Expected Q > 0, got %s", Q.String())
				}
			},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			P, Q, T := calculator.ComputePQTSequential(tt.a, tt.b)
			tt.validate(t, P, Q, T)
		})
	}
}

// TestCombineResults tests the result combination logic
func TestCombineResults(t *testing.T) {
	tests := []struct {
		name     string
		results  []config.Result
		validate func(t *testing.T, P, Q, T *big.Int)
	}{
		{
			name: "Single result",
			results: []config.Result{
				{P: big.NewInt(2), Q: big.NewInt(3), T: big.NewInt(5)},
			},
			validate: func(t *testing.T, P, Q, T *big.Int) {
				if P.Cmp(big.NewInt(2)) != 0 {
					t.Errorf("Expected P=2, got %s", P.String())
				}
				if Q.Cmp(big.NewInt(3)) != 0 {
					t.Errorf("Expected Q=3, got %s", Q.String())
				}
				if T.Cmp(big.NewInt(5)) != 0 {
					t.Errorf("Expected T=5, got %s", T.String())
				}
			},
		},
		{
			name: "Two results",
			results: []config.Result{
				{P: big.NewInt(2), Q: big.NewInt(3), T: big.NewInt(5)},
				{P: big.NewInt(7), Q: big.NewInt(11), T: big.NewInt(13)},
			},
			validate: func(t *testing.T, P, Q, T *big.Int) {
				// P = 2 * 7 = 14
				expectedP := big.NewInt(14)
				if P.Cmp(expectedP) != 0 {
					t.Errorf("Expected P=14, got %s", P.String())
				}
				// Q = 3 * 11 = 33
				expectedQ := big.NewInt(33)
				if Q.Cmp(expectedQ) != 0 {
					t.Errorf("Expected Q=33, got %s", Q.String())
				}
				// T = 11*5 + 2*13 = 55 + 26 = 81
				expectedT := big.NewInt(81)
				if T.Cmp(expectedT) != 0 {
					t.Errorf("Expected T=81, got %s", T.String())
				}
			},
		},
		{
			name: "Three results (recursive)",
			results: []config.Result{
				{P: big.NewInt(2), Q: big.NewInt(3), T: big.NewInt(5)},
				{P: big.NewInt(7), Q: big.NewInt(11), T: big.NewInt(13)},
				{P: big.NewInt(17), Q: big.NewInt(19), T: big.NewInt(23)},
			},
			validate: func(t *testing.T, P, Q, T *big.Int) {
				// Should combine successfully
				if P.Sign() <= 0 {
					t.Errorf("Expected P > 0, got %s", P.String())
				}
				if Q.Sign() <= 0 {
					t.Errorf("Expected Q > 0, got %s", Q.String())
				}
			},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			P, Q, T := calculator.CombineResults(tt.results)
			tt.validate(t, P, Q, T)
		})
	}
}

// TestSanitizePath tests path sanitization security function
func TestSanitizePath(t *testing.T) {
	// Get current working directory for relative path tests
	cwd, err := os.Getwd()
	if err != nil {
		t.Fatalf("Failed to get current working directory: %v", err)
	}

	tests := []struct {
		name        string
		path        string
		shouldError bool
		validate    func(t *testing.T, result string, err error)
	}{
		{
			name:        "Valid relative path",
			path:        "results/test.txt",
			shouldError: false,
			validate: func(t *testing.T, result string, err error) {
				if err != nil {
					t.Errorf("Expected no error, got %v", err)
				}
				if !strings.Contains(result, "test.txt") {
					t.Errorf("Expected path to contain 'test.txt', got %s", result)
				}
			},
		},
		{
			name:        "Directory traversal attempt",
			path:        "../../../etc/passwd",
			shouldError: true,
			validate: func(t *testing.T, result string, err error) {
				if err == nil {
					t.Error("Expected error for directory traversal, got nil")
				}
			},
		},
		{
			name:        "Path with .. in middle",
			path:        "results/../test.txt",
			shouldError: false, // filepath.Clean will normalize this
			validate: func(t *testing.T, result string, err error) {
				if err != nil {
					t.Errorf("Expected no error (normalized path), got %v", err)
				}
			},
		},
		{
			name:        "Absolute path in current directory",
			path:        filepath.Join(cwd, "test.txt"),
			shouldError: false,
			validate: func(t *testing.T, result string, err error) {
				if err != nil {
					t.Errorf("Expected no error for path in current directory, got %v", err)
				}
			},
		},
		{
			name:        "Simple filename",
			path:        "test.txt",
			shouldError: false,
			validate: func(t *testing.T, result string, err error) {
				if err != nil {
					t.Errorf("Expected no error, got %v", err)
				}
			},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := security.SanitizePath(tt.path)
			tt.validate(t, result, err)
			if tt.shouldError && err == nil {
				t.Error("Expected error but got none")
			}
			if !tt.shouldError && err != nil {
				t.Errorf("Unexpected error: %v", err)
			}
		})
	}
}

// TestFormatPiOutput tests the output formatting function
func TestFormatPiOutput(t *testing.T) {
	tests := []struct {
		name     string
		digits   int
		piStr    string
		validate func(t *testing.T, output string)
	}{
		{
			name:   "Small number of digits",
			digits: 10,
			piStr:  "3.1415926535",
			validate: func(t *testing.T, output string) {
				if !strings.Contains(output, "10 Digits of Pi") {
					t.Errorf("Expected '10 Digits of Pi' in output")
				}
				if !strings.Contains(output, "collected by Vu Hung") {
					t.Errorf("Expected attribution in output")
				}
				if !strings.Contains(output, "3.") {
					t.Errorf("Expected '3.' in output")
				}
				if !strings.Contains(output, "1415926535") {
					t.Errorf("Expected digits in output")
				}
			},
		},
		{
			name:   "Thousand digits",
			digits: 1000,
			piStr:  "3.1415926535",
			validate: func(t *testing.T, output string) {
				if !strings.Contains(output, "1 Thousand Digits of Pi") {
					t.Errorf("Expected '1 Thousand Digits of Pi' in output")
				}
			},
		},
		{
			name:   "Million digits",
			digits: 1000000,
			piStr:  "3.1415926535",
			validate: func(t *testing.T, output string) {
				if !strings.Contains(output, "1 Million Digits of Pi") {
					t.Errorf("Expected '1 Million Digits of Pi' in output")
				}
			},
		},
		{
			name:   "Digits grouped in 50s",
			digits: 100,
			piStr:  "3." + strings.Repeat("1", 100),
			validate: func(t *testing.T, output string) {
				lines := strings.Split(output, "\n")
				digitLines := 0
				for _, line := range lines {
					if len(line) == 50 && strings.Contains(line, "1") {
						digitLines++
					}
				}
				if digitLines < 2 {
					t.Errorf("Expected at least 2 lines of 50 digits, got %d", digitLines)
				}
			},
		},
		{
			name:   "String without decimal point",
			digits: 5,
			piStr:  "314159",
			validate: func(t *testing.T, output string) {
				if !strings.Contains(output, "3.") {
					t.Errorf("Expected '3.' in output")
				}
			},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			output := formatter.FormatPiOutput(tt.digits, tt.piStr)
			tt.validate(t, output)
		})
	}
}

// TestWorkerPool tests worker pool functionality
func TestWorkerPool(t *testing.T) {
	t.Run("Create and close worker pool", func(t *testing.T) {
		wp := workerpool.New(2)
		if wp == nil {
			t.Fatal("Expected non-nil worker pool")
		}
		wp.Close()
	})

	t.Run("Submit and receive work", func(t *testing.T) {
		wp := workerpool.New(2)
		defer wp.Close()

		// Submit a small computation
		resultChan := wp.Submit(0, 1, func(a, b int64) config.Result {
			p, q, t := calculator.ComputePQTSequential(a, b)
			return config.Result{P: p, Q: q, T: t}
		})
		result := <-resultChan

		if result.P == nil || result.Q == nil || result.T == nil {
			t.Error("Expected non-nil result values")
		}
		if result.P.Cmp(big.NewInt(1)) != 0 {
			t.Errorf("Expected P=1, got %s", result.P.String())
		}
	})

	t.Run("Multiple submissions", func(t *testing.T) {
		wp := workerpool.New(2)
		defer wp.Close()

		// Submit multiple work items
		ch1 := wp.Submit(0, 1, func(a, b int64) config.Result {
			p, q, t := calculator.ComputePQTSequential(a, b)
			return config.Result{P: p, Q: q, T: t}
		})
		ch2 := wp.Submit(1, 2, func(a, b int64) config.Result {
			p, q, t := calculator.ComputePQTSequential(a, b)
			return config.Result{P: p, Q: q, T: t}
		})

		r1 := <-ch1
		r2 := <-ch2

		if r1.P == nil || r2.P == nil {
			t.Error("Expected non-nil results")
		}
	})
}

// TestComputePQT tests the main computation function
func TestComputePQT(t *testing.T) {
	cfg := config.Default()
	ctx := context.Background()

	t.Run("Small range without worker pool", func(t *testing.T) {
		P, Q, T, err := calculator.ComputePQT(ctx, 0, 5, cfg, nil)
		if err != nil {
			t.Fatalf("Unexpected error: %v", err)
		}
		if P == nil || Q == nil || T == nil {
			t.Error("Expected non-nil results")
		}
		if P.Sign() <= 0 || Q.Sign() <= 0 {
			t.Error("Expected positive P and Q")
		}
	})

	t.Run("Larger range with worker pool", func(t *testing.T) {
		pool := workerpool.New(2)
		defer pool.Close()

		P, Q, T, err := calculator.ComputePQT(ctx, 0, 200, cfg, pool) // Large enough to trigger worker pool
		if err != nil {
			t.Fatalf("Unexpected error: %v", err)
		}
		if P == nil || Q == nil || T == nil {
			t.Error("Expected non-nil results")
		}
		if P.Sign() <= 0 || Q.Sign() <= 0 {
			t.Error("Expected positive P and Q")
		}
	})
}

// TestConstants tests that constants are properly initialized
func TestConstants(t *testing.T) {
	// Test that computation works, which validates constants are initialized
	P, Q, T := calculator.ComputePQTSequential(0, 1)
	if P == nil || Q == nil || T == nil {
		t.Fatal("Expected non-nil results (validates constants are initialized)")
	}
}

// TestComputePQTSequentialEdgeCases tests edge cases
func TestComputePQTSequentialEdgeCases(t *testing.T) {
	t.Run("Even index (a=2)", func(t *testing.T) {
		_, _, T := calculator.ComputePQTSequential(2, 3)
		// T should be positive for even a
		if T.Sign() < 0 {
			t.Error("Expected T >= 0 for even a")
		}
	})

	t.Run("Larger range", func(t *testing.T) {
		P, Q, _ := calculator.ComputePQTSequential(0, 10)
		if P.Sign() <= 0 || Q.Sign() <= 0 {
			t.Error("Expected positive P and Q")
		}
	})

	t.Run("Range starting from non-zero", func(t *testing.T) {
		P, Q, _ := calculator.ComputePQTSequential(5, 10)
		if P.Sign() <= 0 || Q.Sign() <= 0 {
			t.Error("Expected positive P and Q")
		}
	})
}

// TestFormatPiOutputEdgeCases tests edge cases in formatting
func TestFormatPiOutputEdgeCases(t *testing.T) {
	t.Run("Empty string", func(t *testing.T) {
		output := formatter.FormatPiOutput(0, "")
		if output == "" {
			t.Error("Expected non-empty output")
		}
	})

	t.Run("Single character", func(t *testing.T) {
		output := formatter.FormatPiOutput(1, "3")
		if !strings.Contains(output, "3") {
			t.Error("Expected '3' in output")
		}
	})

	t.Run("String starting with 3 but no decimal", func(t *testing.T) {
		output := formatter.FormatPiOutput(5, "314159")
		if !strings.Contains(output, "3.") {
			t.Error("Expected '3.' in output")
		}
	})

	t.Run("String not starting with 3", func(t *testing.T) {
		output := formatter.FormatPiOutput(5, "12345")
		if output == "" {
			t.Error("Expected non-empty output")
		}
	})

	t.Run("Multiple decimal points", func(t *testing.T) {
		output := formatter.FormatPiOutput(10, "3.14.159")
		if output == "" {
			t.Error("Expected non-empty output")
		}
	})
}

// TestSanitizePathEdgeCases tests more edge cases
func TestSanitizePathEdgeCases(t *testing.T) {
	t.Run("Empty path", func(t *testing.T) {
		result, err := security.SanitizePath("")
		if err != nil {
			t.Logf("Empty path error (may be expected): %v", err)
		}
		_ = result
	})

	t.Run("Path with only dots", func(t *testing.T) {
		result, err := security.SanitizePath("...")
		if err == nil {
			t.Logf("Path with dots normalized to: %s", result)
		}
	})

	t.Run("Nested directory traversal", func(t *testing.T) {
		_, err := security.SanitizePath("results/../../etc/passwd")
		if err == nil {
			t.Error("Expected error for nested directory traversal")
		}
	})
}

// TestCombineResultsEdgeCases tests edge cases
func TestCombineResultsEdgeCases(t *testing.T) {
	t.Run("Four results", func(t *testing.T) {
		results := []config.Result{
			{P: big.NewInt(2), Q: big.NewInt(3), T: big.NewInt(5)},
			{P: big.NewInt(7), Q: big.NewInt(11), T: big.NewInt(13)},
			{P: big.NewInt(17), Q: big.NewInt(19), T: big.NewInt(23)},
			{P: big.NewInt(29), Q: big.NewInt(31), T: big.NewInt(37)},
		}
		P, Q, _ := calculator.CombineResults(results)
		if P.Sign() <= 0 || Q.Sign() <= 0 {
			t.Error("Expected positive P and Q")
		}
	})

	t.Run("Five results (odd number)", func(t *testing.T) {
		results := []config.Result{
			{P: big.NewInt(2), Q: big.NewInt(3), T: big.NewInt(5)},
			{P: big.NewInt(7), Q: big.NewInt(11), T: big.NewInt(13)},
			{P: big.NewInt(17), Q: big.NewInt(19), T: big.NewInt(23)},
			{P: big.NewInt(29), Q: big.NewInt(31), T: big.NewInt(37)},
			{P: big.NewInt(41), Q: big.NewInt(43), T: big.NewInt(47)},
		}
		P, Q, _ := calculator.CombineResults(results)
		if P.Sign() <= 0 || Q.Sign() <= 0 {
			t.Error("Expected positive P and Q")
		}
	})
}

// TestWorkerPoolEdgeCases tests worker pool edge cases
func TestWorkerPoolEdgeCases(t *testing.T) {
	t.Run("Single worker", func(t *testing.T) {
		wp := workerpool.New(1)
		defer wp.Close()
		// Test that it works
		_ = wp
	})

	t.Run("Close multiple times", func(t *testing.T) {
		wp := workerpool.New(2)
		wp.Close()
		// Should not panic on second close
		wp.Close()
	})

	t.Run("Submit work after close", func(t *testing.T) {
		wp := workerpool.New(2)
		wp.Close()
		// Submit should handle closed pool gracefully without panicking
		defer func() {
			if r := recover(); r != nil {
				t.Errorf("Submit() panicked after close: %v", r)
			}
		}()
		resultChan := wp.Submit(0, 1, func(a, b int64) config.Result {
			p, q, t := calculator.ComputePQTSequential(a, b)
			return config.Result{P: p, Q: q, T: t}
		})
		// Channel should be closed
		_, ok := <-resultChan
		if ok {
			t.Error("Expected closed channel after pool close")
		}
	})
}

// Benchmark tests with execution time reporting
func BenchmarkComputePQTSequential(b *testing.B) {
	b.ResetTimer()
	start := time.Now()

	for i := 0; i < b.N; i++ {
		calculator.ComputePQTSequential(0, 1000)
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
		_, _, _, err := calculator.ComputePQT(ctx, 0, 1000, cfg, pool)
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
			P: big.NewInt(int64(i + 1)),
			Q: big.NewInt(int64(i + 2)),
			T: big.NewInt(int64(i + 3)),
		}
	}

	b.ResetTimer()
	start := time.Now()

	for i := 0; i < b.N; i++ {
		calculator.CombineResults(results)
	}

	elapsed := time.Since(start)
	b.Logf("Execution time: %v, Avg: %v per iteration", elapsed, elapsed/time.Duration(b.N))
}

func BenchmarkFormatPiOutput(b *testing.B) {
	piStr := "3." + strings.Repeat("1415926535", 100)

	b.ResetTimer()
	start := time.Now()

	for i := 0; i < b.N; i++ {
		formatter.FormatPiOutput(1000, piStr)
	}

	elapsed := time.Since(start)
	b.Logf("Execution time: %v, Avg: %v per iteration", elapsed, elapsed/time.Duration(b.N))
}

// Integration test
func TestEndToEndCalculation(t *testing.T) {
	cfg := config.Default()
	ctx := context.Background()

	calc := calculator.New(cfg, nil)
	piStr, err := calc.ComputePi(ctx, 100)
	if err != nil {
		t.Fatalf("Failed to compute pi: %v", err)
	}

	if len(piStr) < 100 {
		t.Errorf("Expected at least 100 characters, got %d", len(piStr))
	}

	if !strings.HasPrefix(piStr, "3.14") {
		t.Errorf("Expected pi to start with 3.14, got %s", piStr[:10])
	}
}
