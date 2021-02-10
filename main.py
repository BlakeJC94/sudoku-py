from sudoku import Sudoku

file_path = './input.txt'
sudoku = Sudoku(file_path)

# Change total number of sweeps here if needed
# sudoku.total_sweeps = 10000
sudoku.solve()
