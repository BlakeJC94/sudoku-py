from pathlib import Path
from typing import Optional, List, Union

from copy import deepcopy

from sudokupy.utils import load_from_file


class Sudoku:
    """Represents a Sudoku puzzle."""
    def __init__(self, input: Union[List[int], str, Path]):
        """Constructor.

        Args:
            input: either location of file containing puzzle to solve or a list of integers.
        """
        if isinstance(input, str):
            input = Path(input)

        if isinstance(input, Path):
            self.puzzle = load_from_file(input)
        elif isinstance(input, list):
            self.puzzle = deepcopy(input)
        else:
            raise ValueError("Unknown input type.")

        self.dim = len(self)
        self.check()

    def __len__(self):
        return int(len(self.puzzle)**(1/4))

    def change_value(self, value: int, row: int, col: int):
        ind = col + row * self.dim**2
        self.puzzle[ind] = value

    def check(self):
        assert len(self) in [2, 3], "Only 2D or 3D puzzles supported."
        for row_index, col_index in zip(range(len(self)**2), range(len(self)**2)):
            row = set(self.get_row(row_index)).difference(set([0]))
            col = set(self.get_col(col_index)).difference(set([0]))
            # block = set(self.get_block(index)).difference(set([0]))

            row_and_col = len(row.intersection(col))
            # row_and_block = len(row.intersection(block))
            # col_and_block = len(col.intersection(block))
            # if row_and_col > 0 or row_and_block > 0 or col_and_block > 0:
            if row_and_col > 0:
                breakpoint()
                raise ValueError("Invalid Sudoku.")

    def copy_puzzle(self):
        return deepcopy(self.puzzle)

    def _get_row_str(self, row_index, row):
        # TODO
        row_str = ''
        return row_str

    def print(self, output_path: Optional[Path] = None):
        # TODO rewrite
        # if no path given, print to stdout
        print(self.puzzle)
        pass

    def get_row(self, row_index):
        assert row_index in range(self.dim**2), "row_index out of bounds"
        start, end = row_index * (self.dim**2), (row_index + 1) * (self.dim**2)
        row = self.puzzle[start:end]
        return tuple(row)

    def get_col(self, col_index):
        assert col_index in range(self.dim**2), "col_index out of bounds"
        col = self.puzzle[col_index::self.dim**2]
        return tuple(col)

    def get_block(self, block_index):
        assert block_index in range(self.dim**2), "block_index out of bounds"
        start = self.dim * (block_index % self.dim) + (self.dim**3) * (block_index//self.dim)
        offsets = [(i % self.dim) + (i // self.dim) * self.dim**2 for i in range(self.dim**2)]
        block = [self.puzzle[start + i] for i in offsets]
        return tuple(block)



