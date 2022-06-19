"""Main entrypoint for sudoku-py from the command line."""
import argparse
from pathlib import Path
from math import ceil, log10
from typing import Optional

from .generator import Generator
from .solver import Solver
from .puzzle import Puzzle


def main():
    parser = argparse.ArgumentParser(
        description="Generate and solve sudoku puzzles.",
        add_help=True,
    )

    parser.add_argument(
        "-d",
        "--difficulty",
        type=int,
        help="Difficulty for puzzle generator (any number between 1 and 5, default is 3).",
        required=False,
        default=3,
    )

    # if no args, generate a sudoku and put it in stdout
    # if input, load the file and solve it
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        help="Path to file. Will attempt to solve puzzle at this location if specified.",
        required=False,
    )
    # if output, write to file (or multiple files).
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Output file path (print outputs to stdout if not given).",
        required=False,
    )

    # if all-solutions, generate all solutions (stdout or file)
    parser.add_argument(
        "-a",
        "--all-solutions",
        action="store_true",
        help="Whether to solve for all solutions for an input.",
    )
    parser.add_argument(
        "-l",
        "--loops",
        type=int,
        help="Maximum number of loops for Solver (default value is 10000).",
        required=False,
        default=10000,
    )

    args = parser.parse_args()

    if args.input is None:
        generator = Generator(difficulty=args.difficulty, loops=args.loops)
        _generate_puzzle(generator, output=args.output)
    else:
        solver = Solver(loops=args.loops)
        _solve_puzzle(args.input, solver, args.all_solutions, args.output)

    return 0


def _solve_puzzle(
    puzzle_input: Optional[str],
    solver: Solver,
    all_solutions: bool,
    output: Optional[str],
) -> int:
    puzzle = Puzzle(puzzle_input)
    solved = solver(puzzle, all_solutions=all_solutions)

    # TODO refactor once `yield` is used `Solver.__call__`
    if isinstance(solved, Puzzle):
        solved = [solved]

    if output is not None:
        output = Path(output)

    n_solutions = len(solved)
    for i, solution in enumerate(solved, start=1):
        if output:
            if n_solutions > 1:
                index_name = "_" + str(i).zfill(ceil(log10(n_solutions)))
                output = list(output.parts[:-1]) + [
                    output.stem + index_name + output.suffix
                ]
                output = Path("".join(output))

            solution.save(output)
        else:
            if n_solutions > 1:
                print(f"Solution {i} :")
            print(solution)

    return 0


def _generate_puzzle(
    generator: Generator,
    output: Optional[str] = None,
) -> int:
    puzzle = generator.spawn()
    if output is None:
        print(puzzle)
    else:
        puzzle.save(output)
    return 0
