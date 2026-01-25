# Modular Architecture Policy

## Principle

**Use modular architecture**

## Guidelines

- Break functionality into separate, reusable modules
- Each module should have a single, well-defined responsibility
- Use clear interfaces between modules
- Minimize coupling between modules
- Maximize cohesion within modules
- Prefer composition over inheritance

## Implementation Example

```go
// Separate concerns into different packages
package calculator
package workerpool
package progress
package fileio
```

## Related Policies

- [File Size Management](file-size-management.md) - For organizing code into manageable files
- [Object-Oriented Programming](oop.md) - For structuring modules with OOP principles
