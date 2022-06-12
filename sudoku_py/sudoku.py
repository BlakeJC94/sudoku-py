from __future__ import annotations
from pathlib import Path
from typing import Union, List


class Sudoku:
    """Representation of a sudoku puzzle.

    Puzzles are internally stored as a flat list of numbers

    """
    def __init__(self, input: Union[str, Path]):
        """Constructor for the Sudoku class.

        Args:
            puzzle_file: Location of data to load.
        """
        self.puzzle = self.load(input)  # TODO rename puzzle to data

        assert len(self.puzzle) in [16, 81], \
            "`Sudoku` only supports puzzles of order 2 or 3."
        self.order = 2 if len(self.puzzle) == 16 else 3

        self.size = self.order**2  # row/col/block size
        self.total = self.size**2  # total number of elements in sudoku puzzle

    def load(self, input):  # TODO update docs
        """Load puzzle from supplied `puzzle_file`."""
        if isinstance(input, list):
            return [int(element) for element in input]

        # if the input isn't a list, it's probably a path
        if isinstance(input, str):
            input = Path(input)

        assert isinstance(input, Path) and input.exists(), \
            "Expected `input` to point to a file that exists."

        with open(input, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        puzzle = []
        # TODO use regular expressions to make this loading more robust
        for line in lines:
            if line[0] != "-":
                row = line.strip().replace("|", ",").split(",")
                row = [int(d) for d in row]
                puzzle.extend(row)

        return puzzle

    def __eq__(self, sudoku: Sudoku) -> bool:
        return all(i == j for i, j in zip(self.puzzle, sudoku.puzzle))

    def __len__(self) -> int:
        return self.size

    def __str__(self) -> str:
        puzzle_string = ""

        for row_index in range(self.size):
            row_string = self._get_row_str(row_index)
            puzzle_string += row_string + '\n'

        return puzzle_string

    def _get_row_str(self, row_index) -> str:
        row_string = ""

        row = self.get_row(row_index)
        for index, element in enumerate(row):
            row_string += str(element)
            if (index + 1) % self.order == 0:
                if index + 1 == self.size:
                    row_string += '\n'
                else:
                    row_string += '|'
            else:
                row_string += ','

        return row_string

    def save_to_file(self, output_path: Union[str, Path]):
        """Save current puzzle state to file.
        TODO"""
        if isinstance(output_path, str):
            output_path = Path(output_path)

        output = str(self)
        with open(output_path, 'r', encoding='utf-8') as f:
            f.write(output)

    def copy(self) -> Sudoku:
        return Sudoku(input=self.puzzle)

    def get_row(self, index) -> List[int]:
        """Returns elements in row `index`."""
        row_number = (index // self.size)
        start, end = row_number * self.size, (row_number + 1) * self.size
        return self.puzzle[start:end].copy()

    def get_col(self, index) -> List[int]:
        """Returns elements in row `index`."""
        start = index % self.size
        return self.puzzle[start::self.size].copy()

    def get_block(self, index) -> List[int]:
        # find topleft corner index
        row_number = index // (self.order**3)
        col_number = index % self.size
        block_index = (self.order**3) * row_number + self.order * (
            col_number // self.order)

        block = []
        for i in range(self.size):
            selected_index = block_index + (i % self.order) + i % self.size
            row_add = i % self.order
            col_add = i // self.order
            selected_index = block_index + row_add + col_add * self.size
            block.append(self.puzzle[selected_index])

        return block
