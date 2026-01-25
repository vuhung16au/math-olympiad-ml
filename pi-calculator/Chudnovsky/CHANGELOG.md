# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.1] - 2026-01-25

### Added
- CI test script (`scripts/test-ci.sh`) for local CI workflow testing
- `make test-ci` target to run all CI checks locally
- Enhanced `.gitignore` with coverage files, benchmark outputs, and project binaries
- Updated `AGENTS.md` with current codebase structure and implementation examples

### Changed
- Moved `test-ci.sh` to `scripts/` directory for better organization
- Updated Makefile to reference `scripts/test-ci.sh`
- Enhanced `.golangci.yml` with exclusion rules for Go 1.24 compatibility
- Updated `AGENTS.md` to reflect actual package structure (calculator, workerpool, config, formatter, security)

### Fixed
- Linter configuration to handle Go 1.24+ typecheck compatibility issues
- `.gitignore` patterns to properly exclude all build artifacts and test outputs

## [1.0.0] - 2026-01-25

### Added
- Initial implementation of Chudnovsky algorithm
- Multi-core parallel computation support
- Progress bar for long calculations
- File output with formatted results
- Comparison tool for accuracy verification
- Makefile for build automation
- Unit tests with 60%+ coverage
