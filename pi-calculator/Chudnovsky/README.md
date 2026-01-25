# Chudnovsky Pi Calculator

A high-performance, multi-core implementation of the Chudnovsky algorithm for calculating π (pi) to arbitrary precision, written in Go.

## Overview

This project implements the **Chudnovsky algorithm**, the fastest known algorithm for computing π to high precision. The implementation features:

- ⚡ **Multi-core parallelization** for large calculations
- 📊 **Progress bar** for long-running computations
- ✅ **Automatic verification** against reference digits
- 🎯 **Optimized performance** with automatic sequential/parallel mode selection
- 📁 **Flexible output** with customizable file paths
- 🔍 **Comparison tool** for accuracy validation

## Quick Start

```bash
# Build the project
make build

# Calculate 1,000 digits of π
make test1k

# Calculate 1,000,000 digits of π (uses all CPU cores)
make test1m
```

For detailed instructions, see [QUICKSTART.md](QUICKSTART.md).

## Why Chudnovsky Algorithm?

The Chudnovsky algorithm is widely considered the **fastest and most efficient** algorithm for computing π to high precision. Here's how it compares to other well-known algorithms:

### Comparison with Other Algorithms

#### 1. **Machin's Formula** (1706)
- **Convergence**: Linear convergence (~1 digit per iteration)
- **Complexity**: O(n² log n) for n digits
- **Speed**: Slow for high precision
- **Use Case**: Historical significance, educational purposes

#### 2. **Ramanujan's Series** (1914)
- **Convergence**: ~8 digits per term
- **Complexity**: O(n² log n)
- **Speed**: Faster than Machin, but slower than Chudnovsky
- **Use Case**: Good for moderate precision

#### 3. **Bailey-Borwein-Plouffe (BBP) Formula** (1995)
- **Convergence**: Can compute nth digit without previous digits
- **Complexity**: O(n log n)
- **Speed**: Fast for extracting specific digits
- **Use Case**: Extracting specific digits, not full computation
- **Limitation**: Requires hexadecimal representation

#### 4. **Chudnovsky Algorithm** (1989)
- **Convergence**: ~14 digits per term (fastest convergence rate)
- **Complexity**: O(n log³ n) with binary splitting
- **Speed**: **Fastest for high-precision full computation**
- **Use Case**: World record calculations, high-precision applications

### Why Chudnovsky is the Best

1. **Fastest Convergence Rate**
   - Produces approximately **14 decimal digits per term**
   - Other algorithms typically produce 1-8 digits per term
   - This means fewer terms needed for the same precision

2. **Optimal for High Precision**
   - The algorithm scales exceptionally well for millions or billions of digits
   - Used for most world record π calculations since the 1990s
   - Efficient memory usage with binary splitting technique

3. **Mathematical Elegance**
   - Based on hypergeometric series with rapid convergence
   - Formula: π = (426880 × √10005) / Σ(k=0 to ∞) [(-1)^k × (6k)! × (13591409 + 545140134k)] / [(3k)! × (k!)^3 × 640320^(3k+3/2)]
   - Binary splitting allows efficient parallel computation

4. **Parallelization Friendly**
   - Binary splitting naturally divides work into independent chunks
   - Can efficiently utilize multiple CPU cores
   - Our implementation uses worker pools for multi-core acceleration

5. **Proven Track Record**
   - Used in world record calculations (trillions of digits)
   - Industry standard for high-precision π computation
   - Trusted by major computational projects

### Performance Comparison (Approximate)

For computing **1 million digits**:

| Algorithm | Terms Needed | Relative Speed |
|-----------|--------------|----------------|
| Machin's | ~1,000,000 | 100x slower |
| Ramanujan | ~125,000 | 10x slower |
| BBP | N/A (different approach) | - |
| **Chudnovsky** | **~71,429** | **1x (fastest)** |

### Conclusion

The Chudnovsky algorithm represents the **state-of-the-art** for high-precision π computation. While other algorithms have their merits (BBP for digit extraction, Ramanujan for moderate precision), Chudnovsky is the clear winner for computing π to millions or billions of digits with maximum efficiency.

## Features

### Performance Optimizations

- **Automatic Mode Selection**: Uses sequential computation for small calculations (< 1,000 terms) to avoid overhead, and parallel computation for large calculations
- **Multi-Core Support**: Automatically detects and utilizes all available CPU cores
- **Worker Pool Pattern**: Efficient work distribution across CPU cores
- **Binary Splitting**: Optimal algorithm for combining partial results

### User Experience

- **Progress Bar**: Real-time progress indication for long calculations
- **Flexible Output**: Save to custom file paths or print to stdout
- **Formatted Output**: Human-readable format with headers and 50-digit lines
- **Automatic Verification**: Built-in comparison tool for accuracy validation

### Code Quality

- **Modular Architecture**: Clean separation of concerns
- **Object-Oriented Design**: Worker pool pattern with proper encapsulation
- **File Size Management**: Code organized to stay under 500 lines per file
- **Comprehensive Testing**: Multiple test targets for different precision levels

## Installation

### Prerequisites

- Go 1.16 or higher
- Make (for build automation)

### Build

```bash
# Clone the repository
git clone <repository-url>
cd Chudnovsky

# Build the project
make build

# Or build manually
go build -o Chudnovsky main.go
go build -o compare_pi compare_pi.go
```

## Usage

### Basic Usage

```bash
# Calculate 1,000 digits (saves to results/pi.txt by default)
./Chudnovsky 1000

# Calculate with custom output file
./Chudnovsky -o results/my-pi.txt 10000

# Calculate and print to stdout
./Chudnovsky -print 1000
```

### Test Targets

```bash
make test1k     # 1,000 digits (~0.1 seconds)
make test10k    # 10,000 digits (~0.1 seconds)
make test100k   # 100,000 digits (~few seconds)
make test1m     # 1,000,000 digits (~minutes, multi-core)
make test10m    # 10,000,000 digits (~hours, multi-core)
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

## Project Structure

```
Chudnovsky/
├── main.go              # Main calculator implementation
├── compare_pi.go        # Comparison tool for verification
├── Makefile             # Build automation
├── QUICKSTART.md        # Quick start guide
├── AGENTS.md            # Coding guidelines
├── README.md            # This file
├── correct-pi/          # Reference digits for verification
│   ├── Pi/              # Reference files (1K, 10K, 100K, 1M digits)
│   └── README.md        # Reference files documentation
└── results/             # Output directory (generated)
```

## Results Location

All calculated results are saved to the `results/` directory:

```
results/
├── pi.txt          # Default output
├── pi-1k.txt       # From make test1k
├── pi-10k.txt      # From make test10k
├── pi-100k.txt     # From make test100k
├── pi-1m.txt       # From make test1m
└── pi-10m.txt      # From make test10m
```

## Verification

The project includes automatic verification against reference digits:

```bash
# Automatic verification (recommended)
make test1k

# Manual verification
./compare_pi results/pi-1k.txt correct-pi/Pi/Pi1KDP.txt 1000
```

The comparison tool accounts for acceptable rounding errors in the last 1-2 digits.

## Performance

### Small Calculations (< 1,000 digits)
- **Mode**: Sequential computation
- **Speed**: < 1 second
- **CPU**: Single core

### Medium Calculations (1,000 - 100,000 digits)
- **Mode**: Sequential computation
- **Speed**: Seconds to minutes
- **CPU**: Single core

### Large Calculations (> 100,000 digits)
- **Mode**: **Multi-core parallel computation**
- **Speed**: Minutes to hours (depending on digits)
- **CPU**: All available cores
- **Progress**: Real-time progress bar

## Contributing

Please read [AGENTS.md](AGENTS.md) for coding guidelines, including:
- Multi-threading and multi-core utilization
- Modular architecture principles
- Object-oriented programming practices
- File size management

## License

[Add your license here]

## Author

Vu Hung  
https://github.com/vuhung16au

## References

- Chudnovsky, D. V. & Chudnovsky, G. V. (1989). "The Computation of Classical Constants"
- For more information about π algorithms, see `correct-pi/README.md`

## See Also

- [QUICKSTART.md](QUICKSTART.md) - Detailed getting started guide
- [AGENTS.md](AGENTS.md) - Coding guidelines and architecture
- [correct-pi/README.md](correct-pi/README.md) - Reference files documentation
