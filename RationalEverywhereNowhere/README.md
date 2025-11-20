# Rational Numbers: Everywhere but Nowhere

## Overview

This document explores the paradoxical nature of rational numbers—describing them as being "everywhere but nowhere"—and their deep connections to modern cryptography. While rational numbers are dense in the real numbers (you can find one in any interval, no matter how small), they essentially take up no space on the number line, having measure zero.

## Target Audience

This document is designed for multiple levels of readers:

- **Level 1 (High School Accessible)**: Sections 1-3 introduce rational numbers, density, and countability with intuitive explanations
- **Level 2 (More Depth)**: Sections 4-6 explore measure theory, the paradox, and probability implications
- **Level 3 (Crypto + Maths High Level)**: Sections 7-10 connect rational number properties to cryptography, including lattice-based crypto and Wiener's attack
- **Level 4 (Research Level)**: Section 11 contains problems with hints and solution outlines for deeper exploration

## Document Structure

1. **Abstract** - Overview and target audience
2. **Section 1: Introduction to Rational Numbers** - Historical review from Ancient Greek mathematics to modern post-quantum computing
3. **Section 2: Density (Everywhere)** - Rational numbers are dense in reals
4. **Section 3: Countability** - Rationals are countably infinite
5. **Section 4: Measure Zero (Nowhere)** - Lebesgue measure and measure zero sets
6. **Section 5: The Paradox** - Reconciling "everywhere but nowhere"
7. **Section 6: Probability Implications** - 0% probability of picking a rational
8. **Section 7: Cryptography Connections** - Overview of connections
9. **Section 8: Random Number Generation** - Measure zero as negligible probability
10. **Section 9: Lattice-Based Cryptography** - Diophantine approximation basics
11. **Section 10: Wiener's Attack on RSA** - Rational approximation attacks
12. **Section 11: Problems** - Mathematical and cryptographic problems with hints
13. **Section 12: Conclusion** - Summary and key takeaways

## Build Instructions

### Prerequisites
- LaTeX distribution (TeX Live, MiKTeX, or MacTeX)
- Required packages: tikz, pgfplots, tcolorbox, amsthm, and others

### Building the Document

```bash
# Build PDF
make pdf

# Build and create release copy
make release

# Clean build artifacts
make clean
```

The PDF will be generated as `RationalEverywhereNowhere.pdf` in the root directory, and a release copy will be placed in `release/`.

## Visualizations

The document includes 20+ TikZ diagrams covering:
- Timeline of number systems evolution
- Number line visualizations showing density
- Cantor's enumeration grid
- Measure theory illustrations
- Cryptography concept maps
- Lattice diagrams
- RSA attack flowcharts
- And more...

## References

The document references:
- The Chalk Talk YouTube video on rational numbers
- Wiener's attack on RSA
- Lattice-based cryptography papers
- Number theory textbooks

## License

This work is licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).

## Contact

- GitHub: https://github.com/vuhung16au/
- LinkedIn: https://www.linkedin.com/in/nguyenvuhung/

