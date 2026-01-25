# Quick Start Guide

Get started with the Chudnovsky Pi Calculator in minutes!

## Prerequisites

- **Go 1.16+** installed on your system
- **Make** (usually pre-installed on Linux/macOS)
- **Git** (for cloning the repository)

## Building the Project

### Option 1: Using Make (Recommended)

```bash
# Build the main binary
make build

# Build both the calculator and comparison tool
make build-tools
```

### Option 2: Manual Build

```bash
# Build the main calculator
go build -o Chudnovsky main.go

# Build the comparison tool
go build -o compare_pi compare_pi.go
```

## Running the Calculator

### Basic Usage

```bash
# Calculate 1,000 digits of π (saves to results/pi.txt by default)
./Chudnovsky 1000

# Calculate with custom output file
./Chudnovsky -o results/my-pi.txt 10000

# Calculate and print to stdout
./Chudnovsky -print 1000
```

### Command-Line Options

```
Usage: ./Chudnovsky [flags] <digits>

Flags:
  -o string
        Output file path for pi digits (default "results/pi.txt")
  -print
        Print pi to stdout
```

### Examples

```bash
# Calculate 1,000 digits
./Chudnovsky 1000

# Calculate 10,000 digits to a specific file
./Chudnovsky -o /tmp/pi-10k.txt 10000

# Calculate 1,000,000 digits (this will take longer!)
./Chudnovsky -o results/pi-1m.txt 1000000

# Calculate and display on screen
./Chudnovsky -print 100
```

## Running Tests

The Makefile provides convenient test targets that calculate π and automatically verify against reference files:

```bash
# Quick test: 1,000 digits (~0.1 seconds)
make test1k

# Medium test: 10,000 digits (~0.1 seconds)
make test10k

# Large test: 100,000 digits (~few seconds)
make test100k

# Very large test: 1,000,000 digits (~minutes, uses multi-core)
make test1m

# Extreme test: 10,000,000 digits (~hours, uses multi-core)
make test10m
```

## Where Are the Results?

### Output Location

By default, results are saved to the `results/` directory:

```
results/
├── pi.txt          # Default output file
├── pi-1k.txt       # From make test1k
├── pi-10k.txt      # From make test10k
├── pi-100k.txt     # From make test100k
├── pi-1m.txt       # From make test1m
└── pi-10m.txt      # From make test10m
```

### Output Format

The output files are formatted in a human-readable format:

```
1000 Digits of Pi
collected by Vu Hung
https://github.com/vuhung16au

3.
14159265358979323846264338327950288419716939937510
58209749445923078164062862089986280348253421170679
82148086513282306647093844609550582231725359408128
...
```

Digits are grouped in lines of 50 characters for easy reading.

## Performance Characteristics

### Small Calculations (< 1,000 digits)
- **Speed**: Very fast (< 1 second)
- **Mode**: Sequential computation (no worker pool overhead)
- **Use Case**: Quick tests, learning

### Medium Calculations (1,000 - 100,000 digits)
- **Speed**: Fast (seconds to minutes)
- **Mode**: Sequential computation
- **Use Case**: Standard precision needs

### Large Calculations (> 100,000 digits)
- **Speed**: Fast (minutes to hours, depending on digits)
- **Mode**: **Multi-core parallel computation**
- **CPU Usage**: Automatically uses all available CPU cores
- **Use Case**: High-precision calculations, benchmarks

The program automatically detects the calculation size and optimizes accordingly:
- Small calculations: Fast sequential mode
- Large calculations: Multi-core parallel mode with progress bar

## Verifying Results

### Automatic Verification (Recommended)

The test targets automatically verify results:

```bash
make test1k  # Calculates AND verifies automatically
```

### Manual Verification

Use the comparison tool directly:

```bash
# Compare calculated result with reference
./compare_pi results/pi-1k.txt correct-pi/Pi/Pi1KDP.txt 1000
```

The comparison tool:
- Extracts digits from formatted files automatically
- Accounts for rounding errors in the last 1-2 digits
- Reports accuracy percentage and first mismatch (if any)

## Other Useful Commands

```bash
# Show all available Make targets
make help

# Clean build artifacts and results
make clean

# Build everything
make build-tools
```

## Troubleshooting

### "command not found: go"
- Install Go from https://golang.org/dl/
- Ensure Go is in your PATH

### "make: command not found"
- Linux: Usually pre-installed, or install via `sudo apt-get install make`
- macOS: Install Xcode Command Line Tools: `xcode-select --install`
- Windows: Use WSL or install Make for Windows

### Out of Memory Errors
- For very large calculations (> 10M digits), ensure sufficient RAM
- The algorithm is memory-efficient, but billions of digits require significant memory

### Slow Performance
- For large calculations, ensure multi-core mode is active (check for "Using X CPU cores" message)
- Small calculations (< 1,000 digits) use sequential mode by design (faster for small sizes)

## Next Steps

- Read `correct-pi/README.md` to learn why Chudnovsky is the best algorithm
- Check `AGENTS.md` for coding guidelines and architecture principles
- Explore the source code to understand the implementation

## Getting Help

```bash
# Show calculator usage
./Chudnovsky

# Show Makefile help
make help

# Show comparison tool usage
./compare_pi
```

Happy π calculating! 🥧
