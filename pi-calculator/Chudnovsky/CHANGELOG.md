# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Modular architecture with internal packages (calculator, workerpool, formatter, security)
- Structured logging using log/slog
- Configuration struct for centralized settings
- Interfaces for better testability
- Benchmark tests with execution time reporting
- CPU and memory profiling support
- CI/CD pipeline with GitHub Actions
- Code linter configuration (golangci-lint)
- Comprehensive GoDoc documentation
- Error wrapping with fmt.Errorf %w
- Context support for cancellation
- Security scanning tools (gosec, govulncheck)

### Changed
- Refactored code into modular packages following Go best practices
- Replaced fmt.Printf with structured logging
- Improved error handling with proper error wrapping
- Updated module name to use proper Go module path

### Fixed
- Worker pool cleanup to prevent hangs
- Path sanitization security improvements
- Test coverage improvements

## [1.0.0] - 2026-01-25

### Added
- Initial implementation of Chudnovsky algorithm
- Multi-core parallel computation support
- Progress bar for long calculations
- File output with formatted results
- Comparison tool for accuracy verification
- Makefile for build automation
- Unit tests with 60%+ coverage
