# 3x3 Panel Puzzle Solver

This Python program solves a 3x3 panel puzzle by finding valid combinations of commands that transform the initial panel state into a target state (all cells set to `1`).
This usefully solves the puzzle in `Resident Eval (1996)`. [The description of the problem](https://www.evilresource.com/resident-evil/guides/puzzles/solving-guardhouse-drug-storeroom-door-code).
Each command toggles specific cells using XOR, and the solution brute-forces all possible command combinations up to a specified maximum length.

## Features

- **Interactive Input**: Enter the initial 3x3 panel configuration directly
- **Customizable Combination Length**: Set the maximum length of command sequences to explore (default: 3)
- **Predefined Commands**: 9 unique commands that toggle specific cell patterns
- **Brute-Force Algorithm**: Exhaustively checks all valid command combinations to find solutions

## Installation

1. Ensure Python 3.x is installed
2. Download or copy the script `panel_solver.py`

## Usage

1. Run the script:

   ```bash
   python panel_solver.py
   ```

2. Enter the initial panel row by row (3 rows of 0/1 separated by spaces)
3. Specify the maximum combination length (press Enter to use default value 3)

*Example input:*

```bash
Enter initial panel (3 rows of 3 digits 0/1 separated by spaces):
Row 1: 1 1 0
Row 2: 1 0 0
Row 3: 0 0 0
Maximum combination length [3]: 2
```
