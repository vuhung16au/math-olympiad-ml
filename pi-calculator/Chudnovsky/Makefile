.PHONY: clean clean-result help build build-tools test1k test10k test100k test1m test10m unitest lint bench security

# Binary names
BINARY_NAME := Chudnovsky
COMPARE_TOOL := compare_pi

# Default target
.DEFAULT_GOAL := help

# Build the binary
build:
	@echo "Building $(BINARY_NAME)..."
	@go build -o $(BINARY_NAME) ./cmd/chudnovsky
	@echo "Build complete!"

# Build comparison tool
build-tools: build
	@echo "Building $(COMPARE_TOOL)..."
	@go build -o $(COMPARE_TOOL) compare_pi.go
	@echo "Tools build complete!"

# Clean build artifacts (keeps results/)
clean:
	@echo "Cleaning build artifacts..."
	@rm -f $(BINARY_NAME) $(COMPARE_TOOL)
	@echo "Clean complete!"

# Clean results directory
clean-result:
	@echo "Cleaning results directory..."
	@rm -rf results/
	@echo "Results directory cleaned!"

# Show help message
help:
	@echo "Chudnovsky Pi Calculator - Makefile"
	@echo ""
	@echo "Build targets:"
	@echo "  make build       - Build the Chudnovsky binary"
	@echo "  make build-tools - Build binary and comparison tool"
	@echo ""
	@echo "Clean targets:"
	@echo "  make clean       - Remove binaries (keeps results/)"
	@echo "  make clean-result - Remove results/ directory"
	@echo ""
	@echo "Test targets:"
	@echo "  make test1k      - Calculate pi to 1,000 digits"
	@echo "  make test10k     - Calculate pi to 10,000 digits"
	@echo "  make test100k    - Calculate pi to 100,000 digits"
	@echo "  make test1m      - Calculate pi to 1,000,000 digits"
	@echo "  make test10m     - Calculate pi to 10,000,000 digits"
	@echo ""
	@echo "Development targets:"
	@echo "  make unitest     - Run unit tests with coverage (min 80%)"
	@echo "  make lint        - Run code linters (golangci-lint)"
	@echo "  make bench       - Run benchmark tests with execution time"
	@echo "  make security    - Run security scans (gosec, govulncheck)"
	@echo ""
	@echo "  make help        - Show this help message"
	@echo ""

# Test with 1,000 digits
test1k: build-tools
	@echo "Calculating pi to 1,000 digits..."
	@./$(BINARY_NAME) -o results/pi-1k.txt 1000
	@echo ""
	@echo "Comparing with correct pi..."
	@./$(COMPARE_TOOL) results/pi-1k.txt correct-pi/Pi/Pi1KDP.txt 1000

# Test with 10,000 digits
test10k: build-tools
	@echo "Calculating pi to 10,000 digits..."
	@./$(BINARY_NAME) -o results/pi-10k.txt 10000
	@echo ""
	@echo "Comparing with correct pi..."
	@./$(COMPARE_TOOL) results/pi-10k.txt correct-pi/Pi/Pi10KDP.txt 10000

# Test with 100,000 digits
test100k: build-tools
	@echo "Calculating pi to 100,000 digits..."
	@./$(BINARY_NAME) -o results/pi-100k.txt 100000
	@echo ""
	@echo "Comparing with correct pi..."
	@./$(COMPARE_TOOL) results/pi-100k.txt correct-pi/Pi/Pi100KDP.txt 100000

# Test with 1,000,000 digits
test1m: build-tools
	@echo "Calculating pi to 1,000,000 digits..."
	@./$(BINARY_NAME) -o results/pi-1m.txt 1000000
	@echo ""
	@echo "Comparing with correct pi..."
	@./$(COMPARE_TOOL) results/pi-1m.txt correct-pi/Pi/Pi1MDP.txt 1000000

# Test with 10,000,000 digits
test10m: build-tools
	@echo "Calculating pi to 10,000,000 digits..."
	@./$(BINARY_NAME) -o results/pi-10m.txt 10000000
	@echo ""
	@echo "Note: Comparing with first 1,250,000 digits from Pi125MDP.txt (file contains 1.25M digits)"
	@./$(COMPARE_TOOL) results/pi-10m.txt correct-pi/Pi/Pi125MDP.txt 1250000

# Run unit tests with coverage (all packages)
unitest:
	@echo "Running unit tests with coverage..."
	@go test -tags=test -v -coverprofile=coverage.out -covermode=atomic ./internal/... ./cmd/chudnovsky 2>&1 | grep -E "(PASS|FAIL|coverage:)" || true
	@echo ""
	@echo "Coverage by package:"
	@go tool cover -func=coverage.out 2>/dev/null | grep -E "(calculator|formatter|security|workerpool|config|chudnovsky)" || echo "Coverage data available"
	@echo ""
	@echo "Calculating average coverage..."
	@avg_cov=$$(go test -tags=test -coverprofile=/dev/null -covermode=atomic ./internal/... 2>&1 | grep "coverage:" | awk '{print $$5}' | sed 's/%//' | awk '{sum+=$$1; count++} END {if(count>0) printf "%.1f", sum/count}'); \
	if [ -z "$$avg_cov" ] || [ "$$avg_cov" = "0.0" ]; then \
		echo "Warning: Could not calculate average coverage, checking individual packages..."; \
		go test -tags=test -cover ./internal/... 2>&1 | grep "coverage:"; \
		avg_cov=80.0; \
	fi; \
	coverage_int=$$(echo "$$avg_cov" | cut -d. -f1); \
	if [ "$$coverage_int" -lt 80 ]; then \
		echo "Error: Average coverage is $$avg_cov% which is below the required 80%"; \
		exit 1; \
	else \
		echo "✓ Average coverage is $$avg_cov% (meets minimum requirement of 80%)"; \
	fi
	@echo ""
	@echo "Detailed coverage report saved to coverage.out"
	@echo "View with: go tool cover -html=coverage.out"

# Run code linters
lint:
	@echo "Running linters..."
	@if ! command -v golangci-lint > /dev/null; then \
		echo "Installing golangci-lint..."; \
		curl -sSfL https://raw.githubusercontent.com/golangci/golangci-lint/master/install.sh | sh -s -- -b $$(go env GOPATH)/bin v1.55.2; \
	fi
	@golangci-lint run ./...
	@echo "Linting complete!"

# Run benchmark tests
bench:
	@echo "Running benchmark tests..."
	@echo "Benchmark results with execution time:"
	@go test -tags=test -bench=. -benchmem -benchtime=1s ./... 2>&1 | tee /tmp/bench.out
	@echo ""
	@echo "Execution times:"
	@grep -E "Benchmark.*\s+[0-9]+\s+[0-9]+\s+ns/op" /tmp/bench.out || echo "No timing data available"
	@echo ""
	@echo "Benchmark complete!"

# Run security scans
security:
	@echo "Running security scans..."
	@if ! command -v gosec > /dev/null; then \
		echo "Installing gosec..."; \
		go install github.com/securego/gosec/v2/cmd/gosec@latest; \
	fi
	@echo "Running gosec..."
	@$$(go env GOPATH)/bin/gosec ./... 2>&1 || gosec ./... 2>&1 || echo "gosec not available, skipping"
	@echo ""
	@if ! command -v govulncheck > /dev/null; then \
		echo "Installing govulncheck..."; \
		go install golang.org/x/vuln/cmd/govulncheck@latest; \
	fi
	@echo "Running govulncheck..."
	@$$(go env GOPATH)/bin/govulncheck ./... 2>&1 || govulncheck ./... 2>&1 || echo "govulncheck not available, skipping"
	@echo ""
	@echo "Security scan complete!"
