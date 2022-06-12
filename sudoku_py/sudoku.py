from pathlib import Path
from typing import Union


class Sudoku:
    """Representation of a sudoku puzzle.

    Puzzles are internally stored as a flat list of numbers

    """
    def __init__(self, puzzle_file: Union[str, Path]):
        """Constructor for the Sudoku class.

        Args:
            puzzle_file: Location of data to load.
        """
        if isinstance(puzzle_file, str):
            puzzle_file = Path(puzzle_file)
        # TODO move asserts for path to load_puzzle method
        # assert input_path.exists(), "Expected `input_path` to point to a file that exists"
        self.puzzle_file = puzzle_file
        # self.output_path = './output.txt'  # TODO expose in `save` method

        self.puzzle = self.load_puzzle_file()

        assert len(self.puzzle) in [16, 81], \
            "`Sudoku` only supports puzzles of order 2 or 3."
        self.order = 2 if len(self.puzzle) == 16 else 3  # TODO change dim to order

        self.size = self.order**2  # row/col/block size
        self.total = self.size**2  # total number of elements in sudoku puzzle

        # TODO move these all to Solver class
        # self.hist_index = 0
        # self.puzzle_hist = list()
        # self.puzzle_hist.append(self.puzzle)
        # self.poss_hist = list()
        # self.poss_hist.append(['']*len(self.puzzle))
        # self.total_sweeps = 10000

    def load_puzzle_file(self):
        """Load puzzle from supplied `puzzle_file`."""
        assert self.puzzle_file.exists(
        ), "Expected `puzzle_file` to point to a file that exists."

        with open(self.puzzle_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        puzzle = []
        # TODO use regular expressions to make this loading more robust
        for line in lines:
            if line[0] != "-":
                row = line.strip().replace("|", ",").split(",")
                row = [int(d) for d in row]
                puzzle.extend(row)

        return puzzle

    def get_row(self, index):
        """Returns elements in row `index`."""
        row_number = (index // self.size)
        start, end = row_number * self.size, (row_number + 1) * self.size
        return self.puzzle[start:end].copy()

    def get_col(self, index):
        """Returns elements in row `index`."""
        start = index % self.size
        return self.puzzle[start::self.size].copy()

    def get_block(self, index):
        # find topleft corner index
        row_number = index // (self.order ** 3)
        col_number = index % self.size
        block_index = (self.order ** 3) * row_number + self.order * (col_number // self.order)

        block = []
        for i in range(self.size):
            selected_index = block_index + (i % self.order) + i % self.size
            row_add = i % self.order
            col_add = i // self.order
            selected_index = block_index + row_add + col_add * self.size
            block.append(self.puzzle[selected_index])

        return block
