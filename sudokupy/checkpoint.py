from sudokupy.sudoku import Sudoku


class Checkpoint:
    def __init__(self, sudoku: Sudoku, total_sweeps: int = 10000):
        self.hist_index = 0
        self.puzzle_hist = [sudoku.copy_puzzle()]
        self.poss_hist = [None]
        self.total_sweeps = total_sweeps

    def save_state(self, sudoku, possibility_sweep):
        # increase checkpoint index
        self.hist_index += 1
        # save puzzle to history before making guess
        self.puzzle_hist.append(sudoku.copy_puzzle())
        self.poss_hist.append(possibility_sweep.copy())
        pass

    def restore(self):
        # check if input is inconsistent
        if self.hist_index == 0:
            print("Puzzle is not solvable?")
            raise ValueError("hist_index == 0")
        # revert puzzle to current checkpoint and remove from hist
        self.puzzle = self.puzzle_hist.pop().copy()
        possibility_sweep = self.poss_hist.pop().copy()
        # decrease checkpoint index
        self.hist_index -= 1
        return possibility_sweep


