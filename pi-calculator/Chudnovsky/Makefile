.PHONY: clean clean-result help build build-tools test1k test10k test100k test1m test10m

# Binary names
BINARY_NAME := Chudnovsky
COMPARE_TOOL := compare_pi

# Default target
.DEFAULT_GOAL := help

# Build the binary
build:
	@echo "Building $(BINARY_NAME)..."
	@go build -o $(BINARY_NAME) main.go
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
	@echo "Available targets:"
	@echo "  make build       - Build the Chudnovsky binary"
	@echo "  make clean       - Remove binaries (keeps results/)"
	@echo "  make clean-result - Remove results/ directory"
	@echo "  make test1k      - Calculate pi to 1,000 digits"
	@echo "  make test10k   - Calculate pi to 10,000 digits"
	@echo "  make test100k  - Calculate pi to 100,000 digits"
	@echo "  make test1m    - Calculate pi to 1,000,000 digits"
	@echo "  make test10m   - Calculate pi to 10,000,000 digits"
	@echo "  make help      - Show this help message"
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
