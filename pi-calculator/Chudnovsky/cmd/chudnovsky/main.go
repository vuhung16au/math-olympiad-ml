package main

import (
	"context"
	"flag"
	"fmt"
	"log/slog"
	"os"
	"os/signal"
	"path/filepath"
	"runtime"
	"runtime/pprof"
	"strconv"
	"syscall"
	"time"

	"github.com/schollz/progressbar/v3"
	"github.com/vuhung16au/math-olympiad-ml/pi-calculator/Chudnovsky/internal/calculator"
	"github.com/vuhung16au/math-olympiad-ml/pi-calculator/Chudnovsky/internal/config"
	"github.com/vuhung16au/math-olympiad-ml/pi-calculator/Chudnovsky/internal/formatter"
	"github.com/vuhung16au/math-olympiad-ml/pi-calculator/Chudnovsky/internal/security"
	"github.com/vuhung16au/math-olympiad-ml/pi-calculator/Chudnovsky/internal/workerpool"
)

var (
	logger *slog.Logger
	cfg    *config.Config
)

func init() {
	// Initialize structured logger
	logger = slog.New(slog.NewTextHandler(os.Stdout, &slog.HandlerOptions{
		Level: slog.LevelInfo,
	}))

	// Initialize configuration
	cfg = config.Default()

	// Set GOMAXPROCS to use all available CPUs
	numCPU := calculator.GetNumCPU()
	runtime.GOMAXPROCS(numCPU)
	logger.Info("Initialized", "cpu_cores", numCPU)
}

func main() {
	// Parse command-line flags
	var (
		outputPath  string
		printStdout bool
		cpuProfile  string
		memProfile  string
	)

	flag.StringVar(&outputPath, "o", "results/pi.txt", "Output file path for pi digits")
	flag.BoolVar(&printStdout, "print", false, "Print pi to stdout")
	flag.StringVar(&cpuProfile, "cpuprofile", "", "write cpu profile to file")
	flag.StringVar(&memProfile, "memprofile", "", "write memory profile to file")
	flag.Parse()

	// Setup profiling
	if cpuProfile != "" {
		// #nosec G304 -- cpuProfile is a user-provided flag for profiling
		f, err := os.Create(cpuProfile)
		if err != nil {
			logger.Error("Failed to create CPU profile", "error", err)
			os.Exit(1)
		}
		defer func() {
			if err := f.Close(); err != nil {
				logger.Error("Failed to close CPU profile", "error", err)
			}
		}()
		if err := pprof.StartCPUProfile(f); err != nil {
			if closeErr := f.Close(); closeErr != nil {
				logger.Debug("Failed to close CPU profile file", "error", closeErr)
			}
			logger.Error("Failed to start CPU profile", "error", err)
			//nolint:gocritic // exitAfterDefer: os.Exit is intentional here for error handling
			os.Exit(1)
		}
		defer pprof.StopCPUProfile()
	}

	if memProfile != "" {
		defer func() {
			// #nosec G304 -- memProfile is a user-provided flag for profiling
			f, err := os.Create(memProfile)
			if err != nil {
				logger.Error("Failed to create memory profile", "error", err)
				return
			}
			defer func() {
				if err := f.Close(); err != nil {
					logger.Error("Failed to close memory profile", "error", err)
				}
			}()
			runtime.GC()
			if err := pprof.WriteHeapProfile(f); err != nil {
				logger.Error("Failed to write memory profile", "error", err)
			}
		}()
	}

	// Get digits from remaining args
	args := flag.Args()
	if len(args) < 1 {
		fmt.Println("Usage: ./Chudnovsky [flags] <digits>")
		fmt.Println("Flags:")
		flag.PrintDefaults()
		os.Exit(1)
	}

	digits, err := strconv.ParseInt(args[0], 10, 64)
	if err != nil {
		logger.Error("Invalid digits value", "error", err)
		os.Exit(1)
	}

	// Validate input
	if digits < 1 {
		logger.Error("Digits must be at least 1", "digits", digits)
		os.Exit(1)
	}
	if digits > cfg.MaxDigits {
		logger.Error("Digits exceeds maximum", "digits", digits, "max", cfg.MaxDigits)
		os.Exit(1)
	}

	// Create context with cancellation support
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	// Handle interrupt signals
	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, os.Interrupt, syscall.SIGTERM)
	go func() {
		<-sigChan
		logger.Info("Received interrupt signal, cancelling computation...")
		cancel()
	}()

	// Calculate terms
	terms := digits/cfg.DigitsPerTerm + 1
	logger.Info("Starting computation", "digits", digits, "terms", terms)

	// Initialize progress bar
	var progressBar *progressbar.ProgressBar
	if cfg.ProgressBarEnabled {
		progressBar = progressbar.NewOptions64(int64(terms),
			progressbar.OptionSetDescription("Computing terms"),
			progressbar.OptionSetWidth(50),
		)

		// Set progress callback
		calculator.SetProgressCallback(func(current int64) {
			if progressBar != nil {
				if setErr := progressBar.Set64(current); setErr != nil {
					logger.Debug("Failed to update progress bar", "error", setErr)
				}
			}
		})
		defer func() {
			if finishErr := progressBar.Finish(); finishErr != nil {
				logger.Debug("Failed to finish progress bar", "error", finishErr)
			}
		}()
	}

	// Create worker pool if needed
	var pool *workerpool.Pool
	if terms > cfg.MinRangeForWorkerPool {
		poolSize := cfg.WorkerPoolSize
		if poolSize == 0 {
			poolSize = calculator.GetNumCPU()
		}
		pool = workerpool.New(poolSize)
		defer pool.Close()
		logger.Info("Using worker pool", "workers", poolSize)
	}

	// Create calculator
	calc := calculator.New(cfg, pool)

	// Measure execution time
	startTime := time.Now()

	// Compute pi
	piStr, err := calc.ComputePi(ctx, digits)
	if err != nil {
		logger.Error("Failed to compute pi", "error", err)
		os.Exit(1)
	}

	elapsed := time.Since(startTime)
	logger.Info("Computation complete", "duration", elapsed, "digits_per_second", float64(digits)/elapsed.Seconds())

	// Format output
	formattedOutput := formatter.FormatPiOutput(int(digits), piStr)

	// Sanitize and save file
	sanitizedPath, err := security.SanitizePath(outputPath)
	if err != nil {
		logger.Error("Invalid output path", "error", err)
		os.Exit(1)
	}

	outputDir := filepath.Dir(sanitizedPath)
	if outputDir != "." && outputDir != "" {
		// #nosec G301 -- 0755 is appropriate for directory creation
		if err := os.MkdirAll(outputDir, 0o755); err != nil {
			logger.Error("Failed to create output directory", "error", err, "path", outputDir)
			os.Exit(1)
		}
	}

	// #nosec G306 -- 0644 is appropriate for readable output files
	if err := os.WriteFile(sanitizedPath, []byte(formattedOutput), 0o644); err != nil {
		logger.Error("Failed to write file", "error", err, "path", sanitizedPath)
		os.Exit(1)
	}

	logger.Info("Pi saved successfully", "path", sanitizedPath, "digits", digits, "duration", elapsed)

	// Print to stdout if requested
	if printStdout {
		fmt.Println(piStr)
	}
}
