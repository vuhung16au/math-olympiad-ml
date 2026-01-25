package workerpool

import (
	"testing"

	"github.com/vuhung16au/math-olympiad-ml/pi-calculator/Chudnovsky/internal/config"
)

func TestPool_Package(t *testing.T) {
	wp := New(2)
	if wp == nil {
		t.Fatal("Expected non-nil pool")
	}
	wp.Close()
}

func TestPoolSubmit_Package(t *testing.T) {
	wp := New(2)
	defer wp.Close()

	resultChan := wp.Submit(0, 1, func(a, b int64) config.Result {
		return config.Result{P: nil, Q: nil, T: nil} // Placeholder
	})

	<-resultChan
}

func TestPool_CloseIdempotent(t *testing.T) {
	wp := New(2)
	wp.Close()
	// Should not panic
	wp.Close()
}

func TestPool_SubmitAfterClose(t *testing.T) {
	wp := New(2)
	wp.Close()

	// Submit should handle closed pool gracefully
	resultChan := wp.Submit(0, 1, func(a, b int64) config.Result {
		return config.Result{P: nil, Q: nil, T: nil}
	})

	_, ok := <-resultChan
	if ok {
		t.Error("Expected closed channel after pool close")
	}
}

func TestPool_AutoDetectWorkers(t *testing.T) {
	// Test with 0 workers (should auto-detect)
	wp := New(0)
	if wp == nil {
		t.Fatal("Expected non-nil pool")
	}
	wp.Close()
}
