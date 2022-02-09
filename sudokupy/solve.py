from sudokupy.sudoku import Sudoku
from sudokupy.checkpoint import Checkpoint


def get_possibilities(sudoku, puzzle_index):
    possibilities = set(range(1, sudoku.dim**2+1))
    row = set(sudoku.get_row(puzzle_index))
    col = set(sudoku.get_col(puzzle_index))
    block = set(sudoku.get_block(puzzle_index))

    present = block.union(row).union(col)
    possibilities = list(possibilities.difference(present))
    return possibilities

def solve(sudoku: Sudoku):
    pass
