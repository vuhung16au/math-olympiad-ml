# Agent Coding Guidelines

> **Note**: This document has been refactored into separate policy files.  
> See [docs/agents/README.md](docs/agents/README.md) for the complete guidelines.

## Quick Reference

This file is maintained for backward compatibility. For detailed guidelines, please refer to the individual policy files in `docs/agents/`:

- [Multi-Threading](docs/agents/multi-threading.md)
- [Multi-Core Utilization](docs/agents/multi-core.md)
- [Modular Architecture](docs/agents/modular-architecture.md)
- [Object-Oriented Programming](docs/agents/oop.md)
- [File Size Management](docs/agents/file-size-management.md)
- [Security](docs/agents/security.md)
- [Best Practices](docs/agents/best-practices.md)

## Core Principles

### 1. Multi-Threading
- **Use multi-threading whenever possible**
- Leverage goroutines for concurrent operations
- Prefer worker pools for CPU-bound tasks
- Use channels for safe communication between goroutines
- Implement proper synchronization with `sync.WaitGroup`, `sync.Mutex`, or `sync.RWMutex` as needed

### 2. Multi-Core Utilization
- **Use multi-core whenever possible**
- Detect available CPU cores using `runtime.NumCPU()`
- Set `runtime.GOMAXPROCS(numCPU)` to utilize all available cores
- Distribute work across multiple cores using parallel algorithms
- Monitor CPU utilization to ensure effective multi-core usage
- Use worker pools with one worker per CPU core for optimal performance

### 3. Modular Architecture
- **Use modular architecture**
- Break functionality into separate, reusable modules
- Each module should have a single, well-defined responsibility
- Use clear interfaces between modules
- Minimize coupling between modules
- Maximize cohesion within modules
- Prefer composition over inheritance

### 4. Object-Oriented Programming
- **Use OOP whenever possible**
- Define structs with associated methods
- Encapsulate data and behavior together
- Use interfaces to define contracts
- Implement polymorphism through interfaces
- Follow SOLID principles:
  - **S**ingle Responsibility Principle
  - **O**pen/Closed Principle
  - **L**iskov Substitution Principle
  - **I**nterface Segregation Principle
  - **D**ependency Inversion Principle

### 5. File Size Management
- **Break .go files so that all .go files are smaller than 500 lines whenever possible**
- Split large files into logical, cohesive units
- Each file should represent a single concept or component
- Use package organization to group related functionality
- Keep functions focused and concise
- Extract complex logic into separate functions or methods
- Consider creating separate files for:
  - Type definitions and interfaces
  - Implementation of specific features
  - Utility functions
  - Test files

### 6. Security
- **Code must be secure from common vulnerabilities such as buffer overflow**
- Always validate and sanitize user input
- Use bounds checking for array and slice operations
- Prefer Go's built-in safe operations over unsafe pointer arithmetic
- Avoid using `unsafe` package unless absolutely necessary and well-documented
- Validate buffer sizes before operations that could cause overflow
- Use `make()` with explicit capacity when creating slices to prevent unexpected growth
- Check array/slice bounds before indexing: `if index >= 0 && index < len(slice)`
- Validate string lengths before operations that could cause issues
- Use `strconv` package for safe string-to-number conversions instead of manual parsing
- Sanitize file paths to prevent directory traversal attacks
- Validate file sizes before reading to prevent memory exhaustion
- Use context cancellation for long-running operations to prevent resource exhaustion
- Implement proper error handling to avoid information leakage
- Never log sensitive information (passwords, tokens, keys)
- Use constant-time comparisons for security-sensitive operations when applicable

## Implementation Examples

### Multi-Threading Example
```go
// Use worker pools for parallel processing (from internal/workerpool/pool.go)
type Pool struct {
    workers    int
    wg         sync.WaitGroup
    ctx        context.Context
    cancel     context.CancelFunc
    closed     bool
    closeMutex sync.Mutex
}

func (p *Pool) Submit(ctx context.Context, work func() (interface{}, error)) <-chan Result {
    // Submit work to pool for parallel execution
    // Uses channels for safe communication between goroutines
}
```

### Multi-Core Example
```go
// Detect and utilize all CPU cores (from cmd/chudnovsky/main.go)
func init() {
    numCPU := calculator.GetNumCPU()
    runtime.GOMAXPROCS(numCPU)
    logger.Info("Initialized", "cpu_cores", numCPU)
}

// Auto-detect workers from CPU count (from internal/workerpool/pool.go)
func New(workers int) *Pool {
    if workers <= 0 {
        workers = runtime.NumCPU()
        if workers < 1 {
            workers = 1
        }
    }
    // ... create pool with workers
}
```

### Modular Architecture Example
```go
// Separate concerns into different packages
package calculator    // Chudnovsky algorithm implementation
package workerpool    // Parallel computation worker pool
package config        // Configuration management
package formatter     // Output formatting utilities
package security      // Security utilities (path sanitization)
```

### OOP Example
```go
// Use structs with methods (from internal/calculator/chudnovsky.go)
type Calculator struct {
    cfg  *config.Config
    pool PoolInterface
}

func (c *Calculator) ComputePi(ctx context.Context, digits int64) (string, error) {
    // Implementation with context support and error handling
}

// Use interfaces for polymorphism (from internal/config/interfaces.go)
type PoolInterface interface {
    Submit(ctx context.Context, work func() (interface{}, error)) <-chan Result
    Close()
}
```

### Security Example
```go
// Safe bounds checking before array/slice access
func safeAccess(slice []int, index int) (int, error) {
    if index < 0 || index >= len(slice) {
        return 0, fmt.Errorf("index %d out of bounds [0:%d]", index, len(slice))
    }
    return slice[index], nil
}

// Validate input size before processing
func processData(data []byte, maxSize int) error {
    if len(data) > maxSize {
        return fmt.Errorf("data size %d exceeds maximum %d", len(data), maxSize)
    }
    // Safe to process
    return nil
}

// Safe string-to-number conversion
func parseNumber(s string) (int64, error) {
    // Use strconv instead of manual parsing to avoid buffer issues
    return strconv.ParseInt(s, 10, 64)
}

// Sanitize file paths to prevent directory traversal (from internal/security/path.go)
func SanitizePath(path string) (string, error) {
    // Remove any ".." or absolute path components
    cleaned := filepath.Clean(path)
    
    // Check for directory traversal attempts
    if strings.Contains(cleaned, "..") {
        return "", fmt.Errorf("path contains directory traversal: %s", path)
    }
    
    // Validate path stays within working directory
    absPath, err := filepath.Abs(cleaned)
    if err != nil {
        return "", fmt.Errorf("invalid path: %w", err)
    }
    
    // Additional security checks...
    return cleaned, nil
}
```

## Best Practices

1. **Performance First**: Always consider parallelization opportunities
2. **Code Organization**: Keep files small and focused
3. **Reusability**: Design components to be reusable
4. **Testability**: Write testable, modular code
5. **Documentation**: Document public APIs and complex logic
6. **Error Handling**: Handle errors explicitly and gracefully
7. **Security**: Always validate input, check bounds, and protect against common vulnerabilities

## Current Codebase Structure

This project implements the Chudnovsky algorithm for computing π (pi) to arbitrary precision. The codebase follows all the principles outlined above:

### Package Organization
- **`internal/calculator`**: Core Chudnovsky algorithm implementation with parallel computation support
- **`internal/workerpool`**: Worker pool implementation for efficient multi-core utilization
- **`internal/config`**: Centralized configuration management
- **`internal/formatter`**: Output formatting utilities
- **`internal/security`**: Security utilities including path sanitization to prevent directory traversal attacks
- **`cmd/chudnovsky`**: Command-line interface application

### Key Features
- ✅ Multi-threading via worker pools (`internal/workerpool`)
- ✅ Multi-core utilization with auto-detection (`runtime.NumCPU()`, `runtime.GOMAXPROCS()`)
- ✅ Modular architecture with clear separation of concerns
- ✅ OOP design with structs, methods, and interfaces
- ✅ Security measures (path sanitization, input validation, bounds checking)
- ✅ Most files under 500 lines (test files may exceed this for comprehensive coverage)

### Implementation Highlights
- Worker pool automatically scales to available CPU cores
- Context-based cancellation for long-running computations
- Progress callbacks for user feedback
- Comprehensive error handling and validation
- Security-first approach with path sanitization

## Notes

- These guidelines should be followed whenever practical
- Some exceptions may be necessary for specific use cases
- Always prioritize correctness over performance optimizations
- Profile and measure before optimizing
- Test files may exceed 500 lines for comprehensive test coverage
