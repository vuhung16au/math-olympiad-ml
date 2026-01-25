# Contributing

Thank you for your interest in contributing to the Chudnovsky Pi Calculator!

## Development Setup

1. Clone the repository
2. Install Go 1.22+
3. Run `make build` to build the project
4. Run `make unitest` to run tests

## Code Style

- Follow Go standard formatting (`go fmt`)
- Keep files under 500 lines (see `docs/agents/file-size-management.md`)
- Use structured logging (`log/slog`)
- Wrap errors with `fmt.Errorf("message: %w", err)`
- Add GoDoc comments to all public functions

## Testing

- Run `make unitest` - requires 60%+ coverage
- Run `make test1k` - integration test
- Add tests for new functionality
- Update tests when changing behavior

## Pull Request Process

1. Create a feature branch
2. Make your changes
3. Ensure all tests pass (`make unitest`)
4. Run linter (`make lint`)
5. Update documentation if needed
6. Submit PR with clear description

## Code Review

- All PRs require review
- Tests must pass
- Coverage must not decrease
- Follow project guidelines in `docs/agents/`
