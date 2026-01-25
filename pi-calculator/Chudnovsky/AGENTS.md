# Agent Coding Guidelines

This document outlines the coding standards and best practices for development in this project.

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

## Best Practices

1. **Performance First**: Always consider parallelization opportunities
2. **Code Organization**: Keep files small and focused
3. **Reusability**: Design components to be reusable
4. **Testability**: Write testable, modular code
5. **Documentation**: Document public APIs and complex logic
6. **Error Handling**: Handle errors explicitly and gracefully

## Notes

- These guidelines should be followed whenever practical
- Some exceptions may be necessary for specific use cases
- Always prioritize correctness over performance optimizations
- Profile and measure before optimizing
