"""Classes and methods for saving checkpoints of sudoku puzzles."""
from typing import List, Tuple, Dict

from .puzzle import Puzzle


class EmptyCheckpointer(Exception):
    """Exception when attempting to pop from an empty Checkpointer."""


class Checkpointer:
    """Save states of a Sudoku puzzle."""
    def __init__(self):
        """Constructor."""
        self.history = []

    def stash(self, puzzle: Puzzle, guesses: Dict[int, List[int]]):
        """Creates checkpoint for a (puzzle, guesses) pair.

        Args:
            puzzle: Sudoku puzzle to stash.
            guesses: Dict of guesses to stash.
        """
        self.history.append((puzzle.copy(), guesses))

    def pop(self) -> Tuple[Puzzle, Dict[int, List[int]]]:
        """Remove and return last saved (puzzle, guesses) pair.

        Returns:
            Last saved (puzzle, guesses) pair.
        """
        if len(self.history) == 0:
            raise EmptyCheckpointer("Attempted pop of empty Checkpointer")

        return self.history.pop()
