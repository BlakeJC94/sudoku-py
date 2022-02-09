from pathlib import Path
from re import findall
from typing import Union

def load_from_file(file_path: Union[Path, str]):
    """TODO."""
    with open(file_path, 'r') as f:
        lines = f.readlines()

    puzzle = []
    for line in lines:
        puzzle.extend(findall(r'\d', line))

    if len(puzzle) not in [2**4, 3**4]:
        raise ValueError("Only 2D and 3D puzzles supported for now")

    return puzzle

