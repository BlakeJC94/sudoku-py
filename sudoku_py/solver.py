"""Classes and methods for solving sudoku puzzles."""
import logging
from typing import List, Tuple, Dict, Union
from warnings import warn

from .puzzle import Puzzle
from .checkpointer import Checkpointer
from .exceptions import InvalidPuzzleError, UnsolvedWarning, EmptyCheckpointer

logger = logging.getLogger(__name__)


# TODO experiment with yield and next(..)
class Solver:
    """Manages solving operations when given a Sudoku object."""

    def __init__(self, loops: int = 10000):
        """Constructor.

        Args:
            loops: number of loops to do over every cell before giving up.
            patience: number of loops without changes to wait before guessing.
        """
        self.loops = loops
        self.checkpointer = Checkpointer()

    def __call__(
        self,
        puzzle: Puzzle,
        all_solutions=False,
    ) -> Union[Puzzle, List[Puzzle]]:
        """Solves the sudoku puzzle.

        Guesses are managed per loop in a dictionary that maps puzzle indices
        to a list of possible values.

        Args:
            puzzle: Unsolved sudoku puzzle

        Returns:
            Fully solved puzzle if successful, unsolved puzzle if unsuccessful. If `all_solutions`
            is True, returns a list of all solutions.
        """
        if puzzle.is_solved():
            return puzzle

        solutions = []
        input_puzzle = puzzle.copy()
        puzzle = puzzle.copy()
        for loop in range(self.loops):
            try:
                puzzle_output = self.fill_singles(puzzle)
            except InvalidPuzzleError:
                try:
                    puzzle = self.checkpointer.pop()
                    continue
                except EmptyCheckpointer:
                    break

            if puzzle_output == puzzle:
                logger.debug("Multiple possibilities, taking a guess")
                puzzle_output = self.guess(puzzle_output)

            puzzle = puzzle_output

            logger.debug("Completed loop %d", loop + 1)
            if puzzle.is_solved():
                solutions.append(puzzle.copy())
                if all_solutions:
                    try:
                        puzzle = self.checkpointer.pop()
                        continue
                    except EmptyCheckpointer:
                        break
                else:
                    break

        if len(solutions) == 0:
            warn("Unsolved after reaching maximum number of loops.", UnsolvedWarning)
            return input_puzzle

        if all_solutions:
            return solutions

        return solutions[0]

    @staticmethod
    def fill_singles(puzzle: Puzzle) -> Puzzle:
        """Iterate over puzzle cells sequentially, fill cells that only have one possibility.

        Args:
            puzzle: An unsolved puzzle

        Return:
            Puzzle with some cells filled in.
        """
        if puzzle.is_solved():
            return puzzle

        puzzle_output = puzzle.copy()
        for empty_index in puzzle.get_empty_indices():
            options = puzzle.get_options(empty_index)

            if len(options) == 0:
                raise InvalidPuzzleError("INDETERMENENT, restore previous guess")

            if len(options) == 1:
                puzzle_output[empty_index] = options[0]

        return puzzle_output

    def guess(self, puzzle: Puzzle) -> Puzzle:
        """Select cell with minimal number of options and estimate value
        before creating a checkpoint.

        Possibility selected will be removed before creating a checkpoint.

        Args:
            puzzle: unsolved puzzle.

        Returns:
            Puzzle with one cell estimated.
        """
        guesses = []
        for empty_index in puzzle.get_empty_indices():
            options = puzzle.get_options(empty_index)
            if len(options) > 1:
                guesses.append((empty_index, options))

        # find puzzle index with smallest number of possibilities
        min_options = min(len(options) for _, options in guesses)
        index, options = next(
            (i, opts) for i, opts in guesses if len(opts) == min_options
        )

        # save checkpoint
        puzzle = self.checkpointer.stash(puzzle, index, options)
        return puzzle

    def restore(self) -> Tuple[Puzzle, Dict[int, List[int]], bool]:
        """Restore the last checkpoint and fill in cells that only have a single option.

        Returns:
            Restored puzzle, guesses, and flag to indicate if a change was made when restoring.
        """
        puzzle, guesses = self.checkpointer.pop()
        changed_when_restored = False
        try:
            index = next(iter(k for k, v in guesses.items() if len(v) == 1))
            puzzle[index] = guesses[index].pop()
            changed_when_restored = True
        except StopIteration:
            pass

        return puzzle, guesses, changed_when_restored
