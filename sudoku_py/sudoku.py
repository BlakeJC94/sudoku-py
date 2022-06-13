"""Classes for storing and managing puzzle data."""
from __future__ import annotations

import re
from pathlib import Path
from typing import List, Union


class Puzzle:
    """Representation of a sudoku puzzle.

    Puzzles are internally stored as a flat list of numbers

    """
    def __init__(self, input_data: Union[str, Path]):
        """Constructor.

        Args:
            input_data: Either a list of numbers representing a puzzle, or
                a path to a file containing a puzzle.
        """
        self.data = self.load(input_data)

        assert len(self.data) in [16, 81], \
            "`Sudoku` only supports puzzles of order 2 or 3."
        self.order = 2 if len(self.data) == 16 else 3

        self.size = self.order ** 2  # row/col/block size
        self.total = self.size ** 2  # total number of elements in sudoku puzzle

    @staticmethod
    def load(input_data: Union[str, Path, List[int]]) -> List[int]:
        """Load puzzle from supplied input.

        Args:
            input: see __init__ docs.
        """
        if isinstance(input_data, list):
            return [int(element) for element in input_data]

        if isinstance(input_data, str):
            input_data = Path(input_data)

        assert isinstance(input_data, Path) and input_data.exists(), \
            "Expected path `input` to point to a file that exists."

        puzzle = []
        with open(input_data, 'r', encoding='utf-8') as puzzle_file:
            for line in puzzle_file.readlines():
                puzzle += re.findall(r'\d+', line)

        return puzzle

    def __getitem__(self, index: int) -> int:
        return self.data[index]

    def __setitem__(self, index: int, element: int):
        assert 0 <= element <= self.size, \
            f"Only allowed to set values between 0 and {self.size}."
        self.data[index] = element

    def __eq__(self, puzzle: Puzzle) -> bool:
        return all(i == j for i, j in zip(self.data, puzzle.data))

    def __len__(self) -> int:
        return self.size

    def __str__(self) -> str:
        puzzle_string = ""
        for row_index in range(len(self)):
            row_string = self._get_row_str(row_index)
            puzzle_string += row_string + '\n'

        return puzzle_string

    def _get_row_str(self, row_index) -> str:
        row_string = ""
        row = [self[row_index * len(self) + i] for i in range(len(self))]
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

    def save(self, output_path: Union[str, Path]):
        """Save current puzzle state to file."""
        if isinstance(output_path, str):
            output_path = Path(output_path)

        output = str(self)
        with open(output_path, 'r', encoding='utf-8') as puzzle_file:
            puzzle_file.write(output)

    def copy(self) -> Puzzle:
        """Return a duplicate."""
        return Puzzle(input_data=self.data)

    def is_solved(self) -> bool:
        """Check if the puzzle has any empty cells."""
        return all(i == 0 for i in self.data)

    def get_empty_indices(self) -> List[int]:
        """Get indices that correspond to empty cells."""
        return [i for i in range(len(self) ** 2) if self[i] == 0]

    def _get_row_indices(self, index: int) -> List[int]:
        row_start = index // len(self)
        return [row_start * len(self) + i for i in range(len(self))]

    def _get_col_indices(self, index: int) -> List[int]:
        col_start = index % len(self)
        return [col_start + len(self) * i for i in range(self)]

    def _get_block_indices(self, index: int) -> List[int]:
        block_index = (self.order ** 3) * (index // self.order ** 3) \
            + self.order * ((index % len(self)) // self.order)
        return [
            block_index + (i % self.order) + (i // self.order) * len(self)
            for i in range(len(self))
        ]

    def get_row_col_block_indices(self, index: int) -> List[int]:
        """Get indices of the elements in the same row, column, and block as
        the input index."""
        row_indices = self._get_row_indices(index)
        col_indices = self._get_col_indices(index)
        block_indices = self._get_block_indices(index)
        return list(set(sum([row_indices, col_indices, block_indices])))

    def get_options(self, index: int) -> List[int]:
        """Get options for puzzle cell index."""
        if self[index] != 0:
            return []

        indices = self.get_row_col_block_indices(index)
        elements = set(self[i] for i in indices if self[i] != 0)
        return [i + 1 for i in range(len(self)) if i + 1 not in elements]

    def is_valid(self) -> bool:
        """Check if the puzzle is valid."""
        valid = True
        for index in self:
            indices = self.get_row_col_block_indices(index)
            values = [self[i] for i in indices if self[i] != 0]
            if len(values) != len(set(values)):
                valid = False
                break

        return valid
