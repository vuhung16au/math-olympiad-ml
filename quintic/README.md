# Quintic Equation Solver

This project demonstrates how to solve quintic equations (polynomial equations of degree 5) using Python and SymPy.

## Problem

Solve the following quintic equation:

\[ x^5 - 5x^3 + 5x - 4 = 0 \]

This equation is defined in `solver.py` (lines 7-8):

```python
eq = Eq(x**5 - 5*x**3 + 5*x - 4, 0)
```

The goal is to find all solutions (real and complex) to this equation.

## Overview

The solver uses SymPy, a Python library for symbolic mathematics, to find solutions to quintic equations. Quintic equations have the general form:

\[ ax^5 + bx^4 + cx^3 + dx^2 + ex + f = 0 \]

The solver can find both exact symbolic solutions (when possible) and approximate numerical solutions.

## How to Use Python to Solve Quintic Equations

The `solver.py` script demonstrates the approach:

1. **Import SymPy**: Use SymPy's symbolic computation capabilities
2. **Define the variable**: Create a symbolic variable `x`
3. **Define the equation**: Construct the quintic equation using `Eq()`
4. **Solve**: Use `solve()` to find all solutions
5. **Display results**: Print solutions in a readable format

The current solver solves the equation: \( x^5 - 5x^3 + 5x - 4 = 0 \)

You can modify the equation in `solver.py` to solve different quintic equations.

**Note**: Not all quintic equations have closed-form solutions in radicals. SymPy will provide:

- Exact symbolic solutions when possible
- Numerical approximations when exact solutions are not feasible
- Complex solutions when appropriate

## Setting Up Virtual Environment with Python 3.9

Follow these steps to create a virtual environment using Python 3.9:

1. **Check Python 3.9 availability**:

   ```bash
   python3.9 --version
   ```

   If Python 3.9 is not installed, you'll need to install it first.

2. **Create the virtual environment**:

   ```bash
   python3.9 -m venv .venv
   ```

   This creates a virtual environment in the `.venv` directory.

3. **Activate the virtual environment**:

   On macOS/Linux:

   ```bash
   source .venv/bin/activate
   ```

   On Windows:

   ```bash
   .venv\Scripts\activate
   ```

4. **Verify activation**:
   Your terminal prompt should show `(.venv)` at the beginning, indicating the virtual environment is active.

5. **Upgrade pip** (recommended):

   ```bash
   pip install --upgrade pip
   ```

6. **Install dependencies**:

   ```bash
   pip install sympy
   ```

   Or if you have a `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

## Running the Solver Using Virtual Environment

Once your virtual environment is set up and activated:

1. **Ensure the virtual environment is activated**:

   ```bash
   source .venv/bin/activate  # macOS/Linux
   # or
   .venv\Scripts\activate     # Windows
   ```

2. **Run the solver**:

   ```bash
   python solver.py
   ```

3. **Expected output**:
   The script will display all solutions to the quintic equation, formatted using SymPy's pretty printing.

4. **Deactivate the virtual environment** (when done):

   ```bash
   deactivate
   ```

## Example Usage

```bash
# Create and activate virtual environment
python3.9 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install sympy

# Run the solver
python solver.py

# Deactivate when finished
deactivate
```

## Dependencies

- **sympy**: Symbolic mathematics library for solving equations

## Customization

To solve a different quintic equation, edit `solver.py` and modify the equation in line 7:

```python
eq = Eq(x**5 - 5*x**3 + 5*x - 4, 0)  # Change this equation
```

You can solve any quintic equation by modifying the coefficients and constant terms.
