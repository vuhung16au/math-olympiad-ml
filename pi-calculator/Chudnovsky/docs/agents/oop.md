# Object-Oriented Programming Policy

## Principle

**Use OOP whenever possible**

## Guidelines

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

## Implementation Example

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

## Related Policies

- [Modular Architecture](modular-architecture.md) - For organizing OOP code into modules
- [File Size Management](file-size-management.md) - For keeping OOP classes manageable
