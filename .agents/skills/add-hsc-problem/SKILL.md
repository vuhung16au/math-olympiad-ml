---
name: add-hsc-problem
description: Helps the user add a new problem to an HSC booklet, determines where to put it based on difficulty and relevancy, and compiles it.
---

# Adding a new problem to an HSC booklet

When the user asks to add a new problem to an HSC booklet (e.g. `HSC-ComplexNumbers`, `HSC-Polynomials`, etc.), follow these steps:

1. **Analyze the Problem**: 
   - Read the problem statement, hints, and solutions provided by the user.
   - Determine its topic (e.g., Complex Numbers, Polynomials, Mechanics, etc.) and difficulty (Basic, Medium, Advanced).
   - Look at the target booklet (e.g., `HSC-ComplexNumbers`).

2. **Determine the Right Location**:
   - Check the `problems/` directory of the specified booklet.
   - Look for files like `part1-basic.tex`, `part1-medium.tex`, `part1-advanced.tex`, `part2-basic.tex`, `part2-medium.tex`, `part2-advanced.tex`.
   - If the problem has brief solutions and hints intended to encourage student ownership (upside down hints, shorter solutions), it belongs in `part2`.
   - If the problem provides full, detailed reasoning for every step without hints inline, it belongs in `part1`.
   - Select the file matching the difficulty (basic, medium, advanced).

3. **Format the Problem**:
   - Convert the user's markdown/text into LaTeX using the booklet's convention.
   - Use the environment structure:
     ```latex
     \begin{problem}[Optional Title]
       ... problem statement ...
     \end{problem}
     
     \begin{hint}
       ... hints ...
     \end{hint}
     
     \begin{solution}[Sketch or Full Solution]
       ... solution ...
     \end{solution}
     
     \begin{takeaways}
       ... takeaways ...
     \end{takeaways}
     ```
   
4. **Insert the Problem**:
   - Use the file replacement/editing tools to append or insert the formatted problem into the appropriate `.tex` file in the `problems/` directory.

5. **Compile and Release**:
   - Run the command `make clean && make pdf && make release` in the booklet's main directory.
   - Verify that there are no LaTeX errors and the build succeeds. 
   - If there are errors, debug the LaTeX syntax, fix it, and rerun the make commands.
