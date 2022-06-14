"""Classes and methods for solving sudoku puzzles."""
from typing import List, Tuple, Dict

from .puzzle import Puzzle
from .checkpointer import Checkpointer


class Solver:
    """Manages solving operations when given a Sudoku object."""
    def __init__(self, max_loops: int = 10000, patience: int = 2):
        """Constructor.

        Args:
            max_loops: number of loops to do over every cell before giving up.
            patience: number of loops without changes to wait before guessing.
        """
        self.max_loops = max_loops
        self.patience = patience
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
        print("Solving puzzle")
        print(puzzle)

        puzzle = puzzle.copy()
        loops_without_changes = 0
        for loop in range(self.max_loops):

            guesses = {}
            change_made = False
            for index in puzzle.get_empty_indices():
                options = puzzle.get_options(index)

                if len(options) == 0:
                    print("INDETERMENENT, restore previous guess")
                    puzzle, guesses, changed_when_restored = self.restore()
                    if not changed_when_restored:
                        break

                if len(options) == 1:
                    puzzle[index] = options[0]
                    change_made = True

                if len(options) > 1:
                    guesses[index] = options

            print(f"\nCompleted loop {loop + 1}")
            print(puzzle)
            if puzzle.is_solved():
                break

            if not change_made:
                loops_without_changes += 1

            if loops_without_changes >= self.patience:
                print("Multiple possibilities")
                puzzle = self.guess(puzzle, guesses)

        if not puzzle.is_solved():
            print("Unsolved after reaching maximum number of loops.")

        return puzzle

    def guess(
        self,
        puzzle: Puzzle,
        guesses: List[Tuple[int, List[int]]],
    ) -> Puzzle:
        """Select cell with minimal number of options and estimate value
        before creating a checkpoint.

        Possibility selected will be removed before creating a checkpoint.

        Args:
            puzzle: unsolved puzzle.
            guesses: dictionary mapping puzzle indices to possibilities.

        Returns:
            Puzzle with one cell estimated.
        """
        # find puzzle index with smallest number of possibilities
        min_count = min(len(v) for v in guesses.values())
        index = next(k for k, v in guesses.items() if len(v) == min_count)

        # get guess and remove from possibilities
        opts = guesses[index]
        guess = opts.pop()
        guesses[index] = opts  # This might be a bit of paranoia

        # save checkpoint
        self.checkpointer.stash(puzzle, guesses)

        # insert guess
        puzzle[index] = guess
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
