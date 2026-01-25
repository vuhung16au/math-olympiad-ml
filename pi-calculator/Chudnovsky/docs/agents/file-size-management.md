# File Size Management Policy

## Principle

**Break .go files so that all .go files are smaller than 500 lines whenever possible**

## Guidelines

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

## Benefits

- Improved code readability
- Easier maintenance and debugging
- Better code organization
- Simplified code reviews
- Reduced merge conflicts

## Related Policies

- [Modular Architecture](modular-architecture.md) - For organizing code into modules
- [Object-Oriented Programming](oop.md) - For structuring code with OOP principles
