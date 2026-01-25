// Package config provides configuration management for the Chudnovsky calculator.
// It centralizes all configurable parameters to avoid hard-coded values throughout the codebase.
package config

// Config holds configuration for the Chudnovsky calculator.
// All hard-coded values should be moved here for better maintainability.
type Config struct {
	// MaxDigits is the maximum number of digits allowed (prevents memory exhaustion)
	MaxDigits int64

	// WorkerPoolSize is the number of workers in the pool (0 = auto-detect from CPU count)
	WorkerPoolSize int

	// MaxChunkSize limits chunk size to prevent deep recursion
	MaxChunkSize int64

	// MinRangeForWorkerPool is the minimum range size to use worker pool
	MinRangeForWorkerPool int64

	// DigitsPerTerm is the approximate digits per term in Chudnovsky algorithm
	DigitsPerTerm int64

	// BitsPerDigit is the conversion factor from decimal digits to bits
	BitsPerDigit float64

	// ProgressBarEnabled controls whether to show progress bar
	ProgressBarEnabled bool
}

// Default returns the default configuration with sensible values.
// These defaults are optimized for most use cases but can be customized.
func Default() *Config {
	return &Config{
		MaxDigits:             1000000000, // 1 billion digits
		WorkerPoolSize:        0,          // Auto-detect
		MaxChunkSize:          500,
		MinRangeForWorkerPool: 1000,
		DigitsPerTerm:         14,
		BitsPerDigit:          3.322,
		ProgressBarEnabled:    true,
	}
}
