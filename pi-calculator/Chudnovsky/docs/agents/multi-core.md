# Multi-Core Utilization Policy

## Principle

**Use multi-core whenever possible**

## Guidelines

- Detect available CPU cores using `runtime.NumCPU()`
- Set `runtime.GOMAXPROCS(numCPU)` to utilize all available cores
- Distribute work across multiple cores using parallel algorithms
- Monitor CPU utilization to ensure effective multi-core usage
- Use worker pools with one worker per CPU core for optimal performance

## Implementation Example

```go
// Detect and utilize all CPU cores
func init() {
    numCPU := runtime.NumCPU()
    runtime.GOMAXPROCS(numCPU)
    // Create worker pool with one worker per core
    workerPool = NewWorkerPool(numCPU)
}
```

## Related Policies

- [Multi-Threading](multi-threading.md) - For concurrent programming patterns
- [Modular Architecture](modular-architecture.md) - For organizing parallel code
