from sympy import symbols, solve, Eq, pprint

# Define the variable
x = symbols('x')

# Define the equation
eq = Eq(x**5 - 5*x**3 + 5*x - 4, 0)

# Solve the equation
solutions = solve(eq, x)

# Print solutions in radical form
for idx, sol in enumerate(solutions):
    print(f"Solution {idx+1}:")
    pprint(sol)
    print()
