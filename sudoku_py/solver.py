"""Classes and methods for solving sudoku puzzles."""
import logging
from typing import List, Tuple, Dict

from .puzzle import Puzzle
from .checkpointer import Checkpointer

logger = logging.getLogger(__name__)


class InvalidPuzzleError(Exception):
    """Raised when no options are found for a cell in a puzzle."""
    pass

# TODO rename checkpointer to guesser
class Solver:
    """Manages solving operations when given a Sudoku object."""

    def __init__(self, max_loops: int = 10000):
        """Constructor.

        Args:
            max_loops: number of loops to do over every cell before giving up.
            patience: number of loops without changes to wait before guessing.
        """
        self.max_loops = max_loops
        self.checkpointer = Checkpointer()

    def __call__(self, puzzle: Puzzle) -> Puzzle:
        """Solves the sudoku puzzle.

        Guesses are managed per loop in a dictionary that maps puzzle indices
        to a list of possible values.

        Args:
            puzzle: Unsolved sudoku puzzle

        Returns:
            Fully solved puzzle if successful, unsolved puzzle if unsuccessful.
        """
        if puzzle.is_solved():
            return puzzle

        puzzle = puzzle.copy()
        for loop in range(self.max_loops):
            try:
                puzzle, change_made = self.fill_singles(puzzle)
            except InvalidPuzzleError:
                puzzle = self.checkpointer.pop()
                continue
            if not change_made:
                logger.info("Multiple possibilities, taking a guess")
                puzzle = self.guess(puzzle)

            logger.info(f"Completed loop {loop + 1}")
            if puzzle.is_solved():
                break

        if not puzzle.is_solved():
            logger.warning("Unsolved after reaching maximum number of loops.")

        return puzzle

    # TODO fix docstrings
    @staticmethod
    def fill_singles(puzzle: Puzzle) -> Tuple[Puzzle, bool]:
        """"""
        change_made = False
        for empty_index in puzzle.get_empty_indices():
            options = puzzle.get_options(empty_index)

            if len(options) == 0:
                raise InvalidPuzzleError("INDETERMENENT, restore previous guess")

            if len(options) == 1:
                puzzle[empty_index] = options[0]
                change_made = True

        return puzzle, change_made

    # TODO update docs
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
        index, options = next((i, opts) for i, opts in guesses if len(opts) == min_options)

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
