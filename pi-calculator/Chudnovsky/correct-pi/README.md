# Reference Pi Digits

This directory contains reference files with known correct digits of π (pi) for validation and testing purposes.

## Overview

The reference files in this directory are used to verify the accuracy of the Chudnovsky algorithm implementation. These files contain pre-calculated digits of π from trusted sources, allowing us to compare our computed results against known correct values.

## Reference Files

The `Pi/` subdirectory contains reference files with different precision levels:

- `Pi1KDP.txt` - 1,000 digits of π
- `Pi10KDP.txt` - 10,000 digits of π
- `Pi100KDP.txt` - 100,000 digits of π
- `Pi1MDP.txt` - 1,000,000 digits of π
- `Pi125MDP.txt` - 1,250,000 digits of π
- `one-million.txt` - 1,000,000 digits of π (formatted version)

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

## Source

Reference files are obtained from trusted mathematical sources and verified against multiple implementations to ensure accuracy.

## Usage

These reference files are automatically used by the test suite:

```bash
make test1k    # Compares against Pi1KDP.txt
make test10k   # Compares against Pi10KDP.txt
make test100k  # Compares against Pi100KDP.txt
make test1m    # Compares against Pi1MDP.txt
```

The comparison tool (`compare_pi`) automatically handles format differences and accounts for acceptable rounding errors in the last 1-2 digits.
