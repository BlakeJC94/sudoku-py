# sudoku-py

Small Sudoku library for practicing programming in Python.

* Basic CLI endpoint to generate and solve puzzles from the command line,
* API to handle sudoku puzzles in Python,
    * Load puzzles from `txt` files or as a Python List,
    * Includes methods to verify valid puzzles,
* Basic iterative non-random solver,
    * Finds all possible solutions if requested,
* Generate random puzzles,
    * Optionally specify the difficulty,


## Installation

Clone the repo to your system and install
```bash
$ git clone https://github.com/BlakeJC94/sudoku-py.git
$ cd sudoku-py
$ pip install .
```

## Quickstart

This package comes equipped with a command-line endpoint:
```
$ sudoku --help
# usage: sudoku [-h] [-d DIFFICULTY] [-i INPUT] [-o OUTPUT] [-a] [-l LOOPS]
#
# Generate and solve sudoku puzzles.
#
# optional arguments:
#   -h, --help            show this help message and exit
#   -d DIFFICULTY, --difficulty DIFFICULTY
#                         Difficulty for puzzle generator (any number between 1 and 5, default is 3).
#   -i INPUT, --input INPUT
#                         Path to file. Will attempt to solve puzzle at this location if specified.
#   -o OUTPUT, --output OUTPUT
#                         Output file path (print outputs to stdout if not given).
#   -a, --all-solutions   Whether to solve for all solutions for an input.
#   -l LOOPS, --loops LOOPS
#                         Maximum number of loops for Solver (default value is 10000).
#   -s SEED, --seed SEED  Random number generation seed.
```

Generate a random puzzle:
```
# difficulty can optionally be specified with `-d` (value between 1 and 5)
$ sudoku
#   ┌───────┬───────┬───────┐
#   │ 6 . 8 │ 7 . 3 │ . 9 5 │
#   │ 4 . 5 │ 9 8 1 │ 2 . . │
#   │ 1 . 7 │ . 2 5 │ . . . │
#   ├───────┼───────┼───────┤
#   │ 9 . . │ . 7 . │ . . 3 │
#   │ . . . │ 1 9 . │ 8 5 . │
#   │ . . 1 │ 5 . 2 │ . . 7 │
#   ├───────┼───────┼───────┤
#   │ . 7 9 │ . . 8 │ 3 . . │
#   │ . 8 4 │ . 1 . │ 5 6 9 │
#   │ . . . │ 3 5 9 │ 7 . . │
#   └───────┴───────┴───────┘
```

Solve a puzzle:
```
# outputs can be written by using `-o`
$ sudoku -i input.txt
#   ┌───────┬───────┬───────┐
#   │ 5 9 1 │ 3 8 2 │ 6 7 4 │
#   │ 3 8 6 │ 7 4 1 │ 9 2 5 │
#   │ 7 2 4 │ 6 5 9 │ 1 8 3 │
#   ├───────┼───────┼───────┤
#   │ 6 3 8 │ 4 9 5 │ 2 1 7 │
#   │ 4 5 2 │ 1 7 8 │ 3 9 6 │
#   │ 1 7 9 │ 2 3 6 │ 4 5 8 │
#   ├───────┼───────┼───────┤
#   │ 9 6 5 │ 8 2 4 │ 7 3 1 │
#   │ 2 1 3 │ 5 6 7 │ 8 4 9 │
#   │ 8 4 7 │ 9 1 3 │ 5 6 2 │
#   └───────┴───────┴───────┘
```


## Generating Puzzles

Using the Python endpoint,
```python
>>> from sudoku_py import Generator
>>> generator = Generator()
>>> puzzle = generator.spawn(seed=123)
>>> print(puzzle)
#   ┌───────┬───────┬───────┐
#   │ . 3 . │ . . 7 │ . 4 . │
#   │ . . 9 │ . 8 4 │ . . . │
#   │ 7 6 . │ 2 . 3 │ 8 . . │
#   ├───────┼───────┼───────┤
#   │ . 5 3 │ . 7 . │ . . . │
#   │ 9 . . │ . 6 . │ . . . │
#   │ 8 2 . │ 4 . . │ 1 7 9 │
#   ├───────┼───────┼───────┤
#   │ . . 2 │ . 5 . │ 4 . . │
#   │ . 9 5 │ . . 8 │ . . 7 │
#   │ 4 . . │ . 2 6 │ . . . │
#   └───────┴───────┴───────┘
```

## Solving Puzzles

Write the puzzle you'd like to solve as a `txt` file
    - Zeros indicate empty cells
    - Can be written in a comma-separated style (block separators optional)
    - Templates are provided in `./templates`

Example: contents of `input.txt`,
```
0,0,1|0,0,2|0,7,0
3,0,0|7,4,1|0,0,5
7,2,0|0,0,9|0,8,3
-----+-----+-----
0,0,8|0,0,5|0,1,0
4,5,0|0,0,0|0,9,6
0,7,0|2,0,0|4,0,0
-----+-----+-----
9,6,0|8,0,0|0,3,1
2,0,0|5,6,7|0,0,9
0,4,0|9,0,0|5,0,0
```

Using the Python endpoint,
```python
## Load the puzzle from data
>>> from sudoku_py import Puzzle, Solver
>>> unsolved_puzzle = Puzzle('input.txt')
>>> print(unsolved_puzzle)
#   ┌───────┬───────┬───────┐
#   │ . . 1 │ . . 2 │ . 7 . │
#   │ 3 . . │ 7 4 1 │ . . 5 │
#   │ . . . │ . . 9 │ . . 3 │
#   ├───────┼───────┼───────┤
#   │ . . 8 │ . . 5 │ . 1 . │
#   │ 4 . . │ . . . │ . . 6 │
#   │ . . . │ 2 . . │ 4 . . │
#   ├───────┼───────┼───────┤
#   │ 9 6 . │ . . . │ . 3 1 │
#   │ 2 . . │ 5 6 . │ . . 9 │
#   │ . 4 . │ 9 . . │ 5 . . │
#   └───────┴───────┴───────┘
>>> solver = Solver(max_loops=5000)
## Call Solver on Puzzle
>>> solved_puzzle = solver(unsolved_puzzle)
>>> print(solved_puzzle)
#   ┌───────┬───────┬───────┐
#   │ 5 9 1 │ 3 8 2 │ 6 7 4 │
#   │ 3 8 6 │ 7 4 1 │ 9 2 5 │
#   │ 7 2 4 │ 6 5 9 │ 1 8 3 │
#   ├───────┼───────┼───────┤
#   │ 6 3 8 │ 4 9 5 │ 2 1 7 │
#   │ 4 5 2 │ 1 7 8 │ 3 9 6 │
#   │ 1 7 9 │ 2 3 6 │ 4 5 8 │
#   ├───────┼───────┼───────┤
#   │ 9 6 5 │ 8 2 4 │ 7 3 1 │
#   │ 2 1 7 │ 5 6 3 │ 8 4 9 │
#   │ 8 4 3 │ 9 1 7 │ 5 6 2 │
#   └───────┴───────┴───────┘
## Save output (fancy output with `solved_puzzle.save('output.txt', unicode=True)`)
>>> solved_puzzle.save('output.txt')
## Find all solutions
>>> solutions = solver(unsolved_puzzle, all_solutions=True)
>>> print(f'Number of solutions found: {len(solutions)}')
# Number of solutions found: 1
```

Example: Content of `output.txt`,
```
+-------+-------+-------+
| 5 9 1 | 3 8 2 | 6 7 4 |
| 3 8 6 | 7 4 1 | 9 2 5 |
| 7 2 4 | 6 5 9 | 1 8 3 |
+-------+-------+-------+
| 6 3 8 | 4 9 5 | 2 1 7 |
| 4 5 2 | 1 7 8 | 3 9 6 |
| 1 7 9 | 2 3 6 | 4 5 8 |
+-------+-------+-------+
| 9 6 5 | 8 2 4 | 7 3 1 |
| 2 1 7 | 5 6 3 | 8 4 9 |
| 8 4 3 | 9 1 7 | 5 6 2 |
+-------+-------+-------+
```

## Possible extensions

- [x] Random puzzle generator
- [x] Optionally find multiple solutions if they exist
- [x] CLI endpoint with `argparse`
- [ ] Samurai sudoku interface?
- [ ] GUI?


## Contributing

This is a small personal project, but pull requests are welcome.
