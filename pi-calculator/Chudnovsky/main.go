package main

import (
	"context"
	"flag"
	"fmt"
	"math/big"
	"os"
	"path/filepath"
	"runtime"
	"strconv"
	"strings"
	"sync"
	"sync/atomic"

	"github.com/schollz/progressbar/v3"
)

// Constants for Chudnovsky
var (
	A = big.NewInt(13591409)
	B = big.NewInt(545140134)
	C = big.NewInt(640320)
	C3 = new(big.Int).Exp(big.NewInt(640320), big.NewInt(3), nil)
)

type Result struct {
	P, Q, T *big.Int
}

var (
	progressCounter int64
	progressBar     *progressbar.ProgressBar
	totalTerms      int64
	numCPU          int
	workerPool      *WorkerPool
)

// WorkItem represents a range to compute
type WorkItem struct {
	Start, End int64
	Result     chan Result
}

// WorkerPool manages parallel computation
type WorkerPool struct {
	workers    int
	workChan   chan WorkItem
	wg         sync.WaitGroup
	ctx        context.Context
	cancel     context.CancelFunc
}

// NewWorkerPool creates a new worker pool
func NewWorkerPool(workers int) *WorkerPool {
	ctx, cancel := context.WithCancel(context.Background())
	wp := &WorkerPool{
		workers:  workers,
		workChan: make(chan WorkItem, workers*2),
		ctx:      ctx,
		cancel:   cancel,
	}
	
	// Start worker goroutines
	for i := 0; i < workers; i++ {
		wp.wg.Add(1)
		go wp.worker(i)
	}
	
	return wp
}

// worker processes work items
func (wp *WorkerPool) worker(id int) {
	defer wp.wg.Done()
	for {
		select {
		case <-wp.ctx.Done():
			return
		case work, ok := <-wp.workChan:
			if !ok {
				// Channel closed, exit
				return
			}
			// Yield to scheduler before starting work
			runtime.Gosched()
			p, q, t := computePQTSequential(work.Start, work.End)
			work.Result <- Result{P: p, Q: q, T: t}
		}
	}
}

// Submit submits work to the pool
func (wp *WorkerPool) Submit(start, end int64) <-chan Result {
	resultChan := make(chan Result, 1)
	select {
	case wp.workChan <- WorkItem{Start: start, End: end, Result: resultChan}:
	case <-wp.ctx.Done():
		close(resultChan)
	}
	return resultChan
}

// Close shuts down the worker pool
func (wp *WorkerPool) Close() {
	wp.cancel()  // Signal workers to stop first
	close(wp.workChan)  // Then close the channel
	wp.wg.Wait()  // Wait for all workers to finish
}

func init() {
	numCPU = runtime.NumCPU()
	if numCPU < 1 {
		numCPU = 1
	}
	// Set GOMAXPROCS to use all available CPUs
	runtime.GOMAXPROCS(numCPU)
}

// combineResults combines multiple PQT results in a binary tree fashion
func combineResults(results []Result) (P, Q, T *big.Int) {
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
	p1, q1, t1 := combineResults(results[:mid])
	p2, q2, t2 := combineResults(results[mid:])
	
	P = new(big.Int).Mul(p1, p2)
	Q = new(big.Int).Mul(q1, q2)
	T = new(big.Int).Add(
		new(big.Int).Mul(q2, t1),
		new(big.Int).Mul(p1, t2),
	)
	return P, Q, T
}

// computePQTSequential is the sequential version (used by workers)
func computePQTSequential(a, b int64) (P, Q, T *big.Int) {
	// Safety check: ensure valid range
	if a >= b {
		return big.NewInt(1), big.NewInt(1), big.NewInt(0)
	}
	
	if b-a == 1 {
		// Update progress for base case
		if progressBar != nil {
			atomic.AddInt64(&progressCounter, 1)
			progressBar.Set64(atomic.LoadInt64(&progressCounter))
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
	p1, q1, t1 := computePQTSequential(a, mid)
	p2, q2, t2 := computePQTSequential(mid, b)
	P = new(big.Int).Mul(p1, p2)
	Q = new(big.Int).Mul(q1, q2)
	T = new(big.Int).Add(new(big.Int).Mul(q2, t1), new(big.Int).Mul(p1, t2))
	return P, Q, T
}

// computePQT uses worker pool for parallel computation
func computePQT(a, b int64) (P, Q, T *big.Int) {
	rangeSize := b - a
	
	// Use worker pool for larger ranges, but ensure chunks are small enough
	if rangeSize > 100 && workerPool != nil {
		// Calculate number of chunks - ensure each chunk is small enough to avoid deep recursion
		// Target: each chunk should be < 500 to avoid stack overflow
		maxChunkSize := int64(500) // Limit chunk size to prevent deep recursion
		numChunks := int(rangeSize / maxChunkSize)
		if numChunks < 1 {
			numChunks = 1
		}
		// But also use at least numCPU chunks for parallelism (if range is large enough)
		if rangeSize >= int64(numCPU) && numChunks < numCPU {
			numChunks = numCPU
		}
		// Don't create more chunks than the range size
		if numChunks > int(rangeSize) {
			numChunks = int(rangeSize)
		}
		// Cap at reasonable number
		if numChunks > 64 {
			numChunks = 64
		}
		
		// Ensure we have at least one valid chunk
		if numChunks < 1 {
			return computePQTSequential(a, b)
		}
		
		chunkSize := rangeSize / int64(numChunks)
		// Ensure chunkSize is at least 1
		if chunkSize < 1 {
			chunkSize = 1
			numChunks = int(rangeSize) // Adjust numChunks if needed
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
				resultChans[i] = workerPool.Submit(start, end)
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
			results[i] = <-resultChans[i]
		}
		
		return combineResults(results)
	}
	
	// For small ranges or if no worker pool, use sequential
	return computePQTSequential(a, b)
}

// sanitizePath sanitizes file paths to prevent directory traversal attacks
func sanitizePath(path string) (string, error) {
	// Security: Sanitize file paths to prevent directory traversal
	// Remove any ".." or absolute path components
	cleaned := filepath.Clean(path)
	
	// Check if the cleaned path still contains ".." (directory traversal)
	// filepath.Clean should remove these, but we check for safety
	if strings.Contains(cleaned, "..") {
		return "", fmt.Errorf("path contains directory traversal: %s", path)
	}
	
	// Check if path resolves outside the current working directory
	// Get absolute path to detect traversal
	absPath, err := filepath.Abs(cleaned)
	if err != nil {
		return "", fmt.Errorf("invalid path: %v", err)
	}
	
	// Get current working directory
	cwd, err := os.Getwd()
	if err != nil {
		// If we can't get CWD, just use cleaned path (less secure but functional)
		return cleaned, nil
	}
	
	// Check if the absolute path is outside the current directory
	// This prevents writing to /etc, /root, etc.
	relPath, err := filepath.Rel(cwd, absPath)
	if err != nil {
		return "", fmt.Errorf("path outside working directory: %s", path)
	}
	
	// If relative path starts with "..", it's outside the current directory
	if strings.HasPrefix(relPath, "..") {
		return "", fmt.Errorf("path outside working directory: %s", path)
	}
	
	return cleaned, nil
}

// formatPiOutput formats the pi string to match the correct-pi format
func formatPiOutput(digits int, piStr string) string {
	var result strings.Builder
	
	// Format number of digits with proper suffix
	var digitLabel string
	if digits >= 1000000 {
		if digits%1000000 == 0 {
			digitLabel = fmt.Sprintf("%d Million Digits of Pi", digits/1000000)
		} else {
			digitLabel = fmt.Sprintf("%d Digits of Pi", digits)
		}
	} else if digits >= 1000 {
		if digits%1000 == 0 {
			digitLabel = fmt.Sprintf("%d Thousand Digits of Pi", digits/1000)
		} else {
			digitLabel = fmt.Sprintf("%d Digits of Pi", digits)
		}
	} else {
		digitLabel = fmt.Sprintf("%d Digits of Pi", digits)
	}
	
	// Write header
	result.WriteString(digitLabel + "\n")
	result.WriteString("collected by Vu Hung\n")
	result.WriteString("https://github.com/vuhung16au/math-olympiad-ml/tree/main/pi-calculator/Chudnovsky\n")
	result.WriteString("\n")
	
	// Extract digits after decimal point
	digitsAfterDecimal := piStr
	if strings.Contains(piStr, ".") {
		parts := strings.Split(piStr, ".")
		if len(parts) == 2 {
			result.WriteString("3.\n")
			digitsAfterDecimal = parts[1]
		} else {
			// Security: Bounds check before string slicing
			if len(piStr) >= 2 {
				result.WriteString(piStr[:2] + "\n")
				digitsAfterDecimal = piStr[2:]
			} else {
				result.WriteString(piStr + "\n")
				return result.String()
			}
		}
	} else {
		// If no decimal point, assume it starts with "3"
		if len(piStr) > 0 && piStr[0] == '3' {
			result.WriteString("3.\n")
			digitsAfterDecimal = piStr[1:]
		} else {
			result.WriteString(piStr + "\n")
			return result.String()
		}
	}
	
		// Format digits in groups of 50 per line
		// Security: Bounds are already checked in the loop condition and end calculation
		digitsPerLine := 50
		for i := 0; i < len(digitsAfterDecimal); i += digitsPerLine {
			end := i + digitsPerLine
			if end > len(digitsAfterDecimal) {
				end = len(digitsAfterDecimal)
			}
			// Additional safety check (though already ensured by condition above)
			if i < len(digitsAfterDecimal) && end <= len(digitsAfterDecimal) {
				result.WriteString(digitsAfterDecimal[i:end] + "\n")
			}
		}
	
	return result.String()
}

func main() {
	// Parse command-line flags
	var outputPath string
	var printStdout bool
	flag.StringVar(&outputPath, "o", "results/pi.txt", "Output file path for pi digits")
	flag.BoolVar(&printStdout, "print", false, "Print pi to stdout")
	flag.Parse()

	// Get digits from remaining args
	args := flag.Args()
	if len(args) < 1 {
		fmt.Println("Usage: ./Chudnovsky [flags] <digits>")
		fmt.Println("Flags:")
		flag.PrintDefaults()
		return
	}

	digits, err := strconv.ParseInt(args[0], 10, 64)
	if err != nil {
		fmt.Printf("Error: invalid digits value: %v\n", err)
		return
	}

	// Security: Validate input to prevent memory exhaustion
	// Set reasonable maximum (1 billion digits) to prevent resource exhaustion
	const maxDigits = 1000000000 // 1 billion digits
	if digits < 1 {
		fmt.Printf("Error: digits must be at least 1, got %d\n", digits)
		return
	}
	if digits > maxDigits {
		fmt.Printf("Error: digits exceeds maximum allowed (%d), got %d\n", maxDigits, digits)
		return
	}

	prec := uint(float64(digits) * 3.322) // Convert decimal digits to bits
	terms := digits/14 + 1

	// Initialize progress bar
	fmt.Printf("Computing pi to %d digits...\n", digits)
	totalTerms = terms
	progressBar = progressbar.NewOptions64(int64(terms),
		progressbar.OptionSetDescription("Computing terms"),
		progressbar.OptionSetWidth(50),
	)
	atomic.StoreInt64(&progressCounter, 0)

	// Only create worker pool for large calculations (to avoid overhead for small ones)
	// For 1000 digits, terms = ~72, which is too small to benefit from worker pool
	if terms > 1000 {
		fmt.Printf("Using %d CPU cores for parallel computation\n", numCPU)
		workerPool = NewWorkerPool(numCPU)
		defer workerPool.Close()
	} else {
		workerPool = nil // Don't use worker pool for small calculations
	}

	// Compute P, Q, T
	_, Q, T := computePQT(0, terms)
	progressBar.Finish()

	// Final Calculation: pi = (426880 * sqrt(10005) * Q) / T
	fmt.Println("Computing final value...")
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

	// Format output to match correct-pi format
	formattedOutput := formatPiOutput(int(digits), piStr)

	// Save to file
	// Security: Sanitize file path to prevent directory traversal attacks
	sanitizedPath, err := sanitizePath(outputPath)
	if err != nil {
		fmt.Printf("Error: invalid output path: %v\n", err)
		return
	}
	
	outputDir := filepath.Dir(sanitizedPath)
	if outputDir != "." && outputDir != "" {
		if err := os.MkdirAll(outputDir, 0755); err != nil {
			fmt.Printf("Error creating output directory: %v\n", err)
			return
		}
	}

	if err := os.WriteFile(sanitizedPath, []byte(formattedOutput), 0644); err != nil {
		fmt.Printf("Error writing to file: %v\n", err)
		return
	}

	fmt.Printf("Pi saved to: %s\n", sanitizedPath)

	// Print to stdout if requested
	if printStdout {
		fmt.Println(piStr)
	}
}