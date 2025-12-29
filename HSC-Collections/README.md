# HSC Mathematics Extension 2: Collection of Hard Problems

## Attribution
© 2025 Vu Hung Nguyen
Preferred attribution: "Vu Hung Nguyen (2025). math-olympiad-ml — HSC-Collections. Available at https://github.com/vuhung16au/math-olympiad-ml/"

This repository contains a curated collection of challenging problems from the HSC Mathematics Extension 2 curriculum, designed to test deep understanding, creative problem-solving skills, and the ability to synthesize multiple mathematical concepts.

## Licensing
Non-code content in this folder is licensed under Creative Commons Attribution 4.0 International (CC BY 4.0). See [LICENSE.md](LICENSE.md).

CC links: https://creativecommons.org/licenses/by/4.0/ and https://creativecommons.org/licenses/by/4.0/legalcode

Software/code remains MIT-licensed per the repository root LICENSE.

## Overview

This collection presents carefully selected problems that represent the level of difficulty and sophistication expected in the most challenging HSC Extension 2 examinations. Each problem is presented with hints to guide thinking, followed by detailed solutions and key takeaways to reinforce learning.

## What This Collection Is About

This collection focuses on **HSC Mathematics Extension 2 (hard problems)**. The problems span various topics including:

- Complex numbers and their geometric interpretations
- Integration techniques and applications
- Vector geometry in three dimensions
- Mechanics and particle motion
- Inequalities and optimization

Each problem is designed to challenge students beyond standard textbook exercises and requires a deep understanding of mathematical concepts and creative problem-solving approaches.

## Target Audience

This collection is designed for:

- **Students** preparing for HSC Mathematics Extension 2 who want to challenge themselves with difficult problems and develop advanced problem-solving skills
- **Tutors** seeking high-quality problems to use in their teaching and to help students prepare for challenging examinations
- **Educators** looking for challenging problems to incorporate into their curriculum and to assess students' understanding at an advanced level

## How to Build PDF File

### Prerequisites

- Docker (for LaTeX compilation)
- Make (optional, for using the Makefile)

### Using Docker Directly

```bash
docker run --rm -v "$(pwd):/workdir" -w /workdir texlive/texlive:latest \
    pdflatex -interaction=nonstopmode HSC-Collections.tex
```

Run the command twice to resolve all cross-references.

### Using Make (Linux/macOS/Git Bash)

The repository includes a `Makefile` with the following targets:

- `make all` or `make pdf`: Compile the LaTeX document to PDF
- `make clean`: Remove auxiliary files (`.aux`, `.log`, `.out`, `.toc`, `.pdf`)
- `make release`: Compile the PDF and copy it to the `releases/` directory

Example:
```bash
make pdf
```

### Using PowerShell Script (Windows)

For Windows users, use the PowerShell script:

```powershell
.\build.ps1 pdf      # Compile PDF
.\build.ps1 clean    # Clean auxiliary files
.\build.ps1 release # Build and copy to releases/
```

### Using Batch Script (Windows)

Alternatively, use the batch file:

```cmd
build.bat pdf      # Compile PDF
build.bat clean    # Clean auxiliary files
build.bat release  # Build and copy to releases/
```

## How to Use This Collection

### For Students

1. **Attempt the problems first**: Before looking at hints or solutions, try to solve each problem independently. This develops problem-solving skills and mathematical intuition.

2. **Use hints strategically**: If you're stuck, read the hint provided. Hints are designed to guide your thinking without giving away the solution.

3. **Study the solutions**: After attempting the problem (or if you're completely stuck), read through the detailed solution. Pay attention to the approach and techniques used.

4. **Review the takeaways**: The key takeaways highlight important concepts, techniques, and insights from each problem. Use these to reinforce your learning.

5. **Practice similar problems**: Try to find or create similar problems to practice the techniques you've learned.

### For Tutors

1. **Select appropriate problems**: Choose problems that match your students' current level and the topics you're covering.

2. **Use as assessment**: These problems can serve as challenging assessment tasks or exam preparation materials.

3. **Guide problem-solving**: Use the hints to guide students' thinking without immediately revealing solutions.

4. **Discuss solutions**: Walk through the solutions with students, emphasizing the problem-solving process and key techniques.

### For Educators

1. **Curriculum integration**: Incorporate these problems into your curriculum as extension activities or assessment tasks.

2. **Differentiation**: Use these problems to challenge advanced students while providing appropriate support through hints.

3. **Professional development**: Study the solutions and approaches to enhance your own problem-solving skills and teaching methods.

## File Structure

- `HSC-Collections.tex`: Main LaTeX document containing problem statements, hints, and solutions
- `Makefile`: Build automation for Linux/macOS/Git Bash
- `build.ps1`: PowerShell build script for Windows
- `build.bat`: Batch build script for Windows
- `README.md`: This file
- `.gitignore`: Excludes LaTeX auxiliary files from version control
- `styles/`: Directory containing custom LaTeX style files
  - `dl101-colors.sty`: Color scheme definitions
  - `dl101-boxes.sty`: Box and environment definitions
  - `dl101-hints.sty`: Hint environment (upside-down style)
  - `dl101-hsc-problems.sty`: Problem, solution, and takeaways environments
- `samples/`: Directory containing original problem files
- `releases/`: Directory containing compiled PDF releases

## Author

Vu Hung Nguyen  

- LinkedIn: https://www.linkedin.com/in/nguyenvuhung/
- GitHub: https://github.com/vuhung16au/
- Repository: https://github.com/vuhung16au/math-olympiad-ml/tree/main/HSC-Collections

