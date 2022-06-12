from typing import List

from .sudoku import Sudoku
from .checkpointer import Checkpointer


class Solver:
    """Manages solving operations when given a Sudoku object."""
    def __init__(self, total_sweeps: int = 10000):
        """Constructor

        Args:
        TODO
        """
        self.total_sweeps = total_sweeps  # TODO rename to max_iterations
        self.checkpointer = Checkpointer()

    # TODO combine get_row, get_col, get_block in Sudoku
    # TODO move this method to Sudoku
    def get_possibilities(self, sudoku: Sudoku, index: int) -> List[int]:
        """""" # TODO
        possibilities = set(range(1, sudoku.size + 1))

        row = set(sudoku.get_row(index))
        col = set(sudoku.get_col(index))
        block = set(sudoku.get_block(index))

        present = block.union(row).union(col)
        return list(possibilities.difference(present))

    # TODO change `possibility_sweep` to a dict (or list of tuples?)
    # TODO implement __getitem__ in Sudoku
    # TODO implment `solved` attritute in Sudoku
    # TODO refactor solve method
    def solve(self, sudoku: Sudoku):
        """""" # TODO
        print("Solving puzzle")
        print(sudoku)
        sweep, sweep_num = True, 0
        while sweep:  # TODO replace with for loop
            # start sweep
            change_made = False
            sweep_num += 1
            if sweep_num > self.total_sweeps:
                print("exceeded total_sweeps")
                break

            possibility_sweep = [''] * len(sudoku.puzzle)
            # TODO implement `get_empty_cells` in Sudoku and change this loop
            for puzzle_index in range(len(possibility_sweep)):
                if sudoku.puzzle[puzzle_index] == 0:

                    possibilities = self.get_possibilities(
                        sudoku, puzzle_index)

                    if len(possibilities) > 1:
                        possibility_sweep[puzzle_index] = possibilities

                    elif len(possibilities) == 1:
                        sudoku.puzzle[puzzle_index] = possibilities[0]
                        change_made = True

                    elif len(possibilities) == 0:
                        print("INDETERMENENT, restore previous guess")
                        sudoku, possibility_sweep = self.checkpointer.pop()
                        # if one possibility in checkpoint, make change
                        single_counts = {
                            k: v
                            for k, v in possibility_sweep.items()
                            if len(v) == 1
                        }
                        if len(single_counts) > 0:
                            # breakpoint()
                            # TODO!! change poss checkpoint to tuiple
                            selected_index = possibility_counts.index(1)
                            possibilities = possibility_sweep[selected_index]
                            sudoku.puzzle[selected_index] = possibilities[0]
                            change_made = True

                        break

            print(f"\nCompleted sweep {sweep_num}")

            if not change_made:
                if min(sudoku.puzzle) > 0:
                    print("Puzzle solved!")
                    print(sudoku)
                    sweep = False
                else:
                    print("Multiple possibilities")
                    print(sudoku)
                    sudoku = self.guess(sudoku, possibility_sweep)

    # TODO refactor this guff
    def guess(self, sudoku, possibility_sweep):
        """""" # TODO
        # find puzzle index with smallest number of possibilities
        possibility_counts = list(map(len, possibility_sweep))
        non_zero_counts = [i for i in possibility_counts if i != 0]
        selected_puzzle_index = possibility_counts.index(min(non_zero_counts))
        # get guess and remove from possibilities
        guess = possibility_sweep[selected_puzzle_index][-1]
        possibility_sweep[selected_puzzle_index].pop()
        # save state
        self.checkpointer.stash(sudoku, possibility_sweep)
        # insert guess
        sudoku.puzzle[selected_puzzle_index] = guess
        return sudoku
