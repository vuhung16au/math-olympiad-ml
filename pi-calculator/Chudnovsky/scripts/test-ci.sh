#!/bin/bash

# CI Test Script
# This script runs all the same checks as the GitHub Actions CI workflow locally
# Should be executed from the project root folder

set -e  # Exit on any error

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Get the project root (parent of scripts directory)
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Change to project root to ensure we're in the right directory
cd "$PROJECT_ROOT"

echo "=========================================="
echo "Testing CI Workflow Locally"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track if any step fails
FAILED=0

# Step 1: Run unit tests
echo -e "${YELLOW}[1/4] Running unit tests...${NC}"
if make unitest; then
    echo -e "${GREEN}✓ Unit tests passed${NC}"
else
    echo -e "${RED}✗ Unit tests failed${NC}"
    FAILED=1
fi
echo ""

# Step 2: Run linter
echo -e "${YELLOW}[2/4] Running linter...${NC}"
if make lint; then
    echo -e "${GREEN}✓ Linter passed${NC}"
else
    echo -e "${RED}✗ Linter failed${NC}"
    FAILED=1
fi
echo ""

# Step 3: Run integration test
echo -e "${YELLOW}[3/4] Running integration test (1K digits)...${NC}"
if make test1k; then
    echo -e "${GREEN}✓ Integration test passed${NC}"
else
    echo -e "${RED}✗ Integration test failed${NC}"
    FAILED=1
fi
echo ""

# Step 4: Check formatting
echo -e "${YELLOW}[4/4] Checking code formatting...${NC}"
UNFORMATTED=$(gofmt -s -l . | wc -l)
if [ "$UNFORMATTED" -eq 0 ]; then
    echo -e "${GREEN}✓ Code is properly formatted${NC}"
else
    echo -e "${RED}✗ Code is not formatted. Found $UNFORMATTED files${NC}"
    echo "Run 'go fmt ./...' to fix formatting issues"
    echo ""
    echo "Unformatted files:"
    gofmt -s -l .
    FAILED=1
fi
echo ""

# Summary
echo "=========================================="
if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All CI checks passed!${NC}"
    echo "=========================================="
    exit 0
else
    echo -e "${RED}✗ Some CI checks failed${NC}"
    echo "=========================================="
    exit 1
fi
