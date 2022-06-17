"""Classes and methods for saving checkpoints of sudoku puzzles."""
from typing import List, Tuple, Dict

from .puzzle import Puzzle
from .exceptions import EmptyCheckpointer


class Checkpointer:
    """Save states of a Sudoku puzzle."""

    def __init__(self):
        """Constructor."""
        self.history = []

    def __len__(self) -> int:
        return len(self.history)

    def __getitem__(self, index: int) -> Tuple[Puzzle, int, List[int]]:
        return self.history[index]

    def __str__(self) -> str:
        return f"Checkpointer[n_checkpoints={len(self.history)}]"

    def stash(self, puzzle: Puzzle, index: int, options: List[int]) -> Puzzle:
        """Pops an element from options and guesses value at puzzle index, then creates checkpoint
        for a (puzzle, index, guess) triplet.

        Args:
            puzzle: Sudoku puzzle to stash.
            index: Cell index to make the guess.
            options: List of valid options to guess at cell index.

        Returns:
            Puzzle with guess made at selected cell from an element of options.
        """
        assert (
            len(options) >= 2
        ), "`Checkpointer.stash` requires an input with at least 2 options."
        guess = options.pop()
        self.history.append((puzzle.copy(), index, options.copy()))
        puzzle[index] = guess
        return puzzle

    def pop(self) -> Puzzle:
        """Remove and return last saved (puzzle, index, options) triplet.

        Equivalent to traversing another branch of the decision tree at the last bifurcation.

        Returns:
            Last saved (puzzle, index, options) triplet.
        """
        if len(self.history) == 0:
            raise EmptyCheckpointer("Attempted pop of empty Checkpointer")

        puzzle, index, opts = self.history.pop()
        if len(opts) == 1:
            puzzle[index] = opts[0]

        return puzzle
