# Security Policy

## Principle

**Code must be secure from common vulnerabilities such as buffer overflow**

## Guidelines

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

### Safe Bounds Checking

```go
// Safe bounds checking before array/slice access
func safeAccess(slice []int, index int) (int, error) {
    if index < 0 || index >= len(slice) {
        return 0, fmt.Errorf("index %d out of bounds [0:%d]", index, len(slice))
    }
    return slice[index], nil
}
```

### Input Size Validation

```go
// Validate input size before processing
func processData(data []byte, maxSize int) error {
    if len(data) > maxSize {
        return fmt.Errorf("data size %d exceeds maximum %d", len(data), maxSize)
    }
    // Safe to process
    return nil
}
```

### Safe String Conversion

```go
// Safe string-to-number conversion
func parseNumber(s string) (int64, error) {
    // Use strconv instead of manual parsing to avoid buffer issues
    return strconv.ParseInt(s, 10, 64)
}
```

### Path Sanitization

```go
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

## Common Vulnerabilities to Prevent

- **Buffer Overflow**: Always check bounds before array/slice access
- **Directory Traversal**: Sanitize file paths
- **Memory Exhaustion**: Validate input sizes
- **Information Leakage**: Don't expose sensitive data in errors or logs
- **Resource Exhaustion**: Use context cancellation for long operations

## Related Policies

- [Best Practices](best-practices.md) - For general security best practices
