# Entropy-Guided-Sudoku-Solver-3x3-
This project implements a smart solver for mini 3x3 Sudoku puzzles (yes, the tiny ones), but instead of brute force, it uses entropy-based heuristics and constraint propagation to efficiently crack even the hardest setups — or detect unsolvable ones.
🔍 Constraint Propagation — Pre-fills obvious cells by scanning rows and columns.

🧮 Weighted Entropy Heuristics — Chooses the next cell to fill based on both how constrained it is and how rare its possible values are.

🔁 Recursive Backtracking — Explores the solution space only when the board is still valid.

This method mimics real-world AI strategies used in SAT solvers and search-based optimization.
