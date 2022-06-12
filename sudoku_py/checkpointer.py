from typing import List, Tuple, Dict

from .sudoku import Sudoku


class EmptyCheckpointer(Exception):
    """Exception when attempting to pop from an empty Checkpointer."""


class Checkpointer:
    """Save states of a Sudoku puzzle."""
    def __init__(self):
        """Constructor.

        Args:
        """ # TODO
        self.history = []

    def stash(self, sudoku: Sudoku, guesses: Dict[int, List[int]]):
        """"""  # TODO should make a guess in Solver before stashing
        self.history.append((sudoku.copy(), guesses))

    def pop(self) -> Tuple[Sudoku, Dict[int, List[int]]]:
        """"""  # TODO
        if len(self.history) == 0:
            raise EmptyCheckpointer("Attempted pop of empty Checkpointer")

        return self.history.pop()
