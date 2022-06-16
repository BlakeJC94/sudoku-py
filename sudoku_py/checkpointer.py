"""Classes and methods for saving checkpoints of sudoku puzzles."""
from typing import List, Tuple, Dict

from .puzzle import Puzzle


class EmptyCheckpointer(Exception):
    """Exception when attempting to pop from an empty Checkpointer."""


# TODO rename to Guesser
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
        return f"Checkpointer[stack={len(self.history)}]"

    # TODO update docs
    def stash(self, puzzle: Puzzle, index: int, options: List[int]) -> Puzzle:
        """Creates checkpoint for a (puzzle, index, guess) triplet.

        Args:
            puzzle: Sudoku puzzle to stash.
            guess: Tuple of (index, guess) to stash.
        """
        guess = options.pop()
        self.history.append((puzzle.copy(), index, options.copy()))
        puzzle[index] = guess
        return puzzle

    def pop(self) -> Puzzle:
        """Remove and return last saved (puzzle, guesses) pair.

        Returns:
            Last saved (puzzle, guesses) pair.
        """
        if len(self.history) == 0:
            raise EmptyCheckpointer("Attempted pop of empty Checkpointer")

        puzzle, index, opts = self.history.pop()
        if len(opts) == 1:
            puzzle[index] = opts[0]

        return puzzle
