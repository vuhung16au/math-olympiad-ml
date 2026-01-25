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
// Use worker pools for parallel processing
type WorkerPool struct {
    workers  int
    workChan chan WorkItem
    wg       sync.WaitGroup
}

func (wp *WorkerPool) worker() {
    defer wp.wg.Done()
    for work := range wp.workChan {
        processWork(work)
        runtime.Gosched() // Yield to scheduler
    }
}
```

### Multi-Core Example
```go
// Detect and utilize all CPU cores
func init() {
    numCPU := runtime.NumCPU()
    runtime.GOMAXPROCS(numCPU)
    // Create worker pool with one worker per core
    workerPool = NewWorkerPool(numCPU)
}
```

### Modular Architecture Example
```go
// Separate concerns into different packages
package calculator
package workerpool
package progress
package fileio
```

### OOP Example
```go
// Use structs with methods
type Calculator struct {
    precision uint
    workers   int
}

func (c *Calculator) Compute(input Input) (Output, error) {
    // Implementation
}

// Use interfaces for polymorphism
type Processor interface {
    Process(data Data) Result
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

// Sanitize file paths to prevent directory traversal
func sanitizePath(path string) (string, error) {
    // Remove any ".." or absolute path components
    cleaned := filepath.Clean(path)
    if filepath.IsAbs(cleaned) {
        return "", fmt.Errorf("absolute paths not allowed")
    }
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

## Notes

- These guidelines should be followed whenever practical
- Some exceptions may be necessary for specific use cases
- Always prioritize correctness over performance optimizations
- Profile and measure before optimizing
