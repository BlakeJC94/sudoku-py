from sudoku import Sudoku

file_path = './puzzles/3_dim/hard/input_1.txt'
sudoku = Sudoku(file_path)
# sudoku.total_sweeps = 10000
sudoku.solve()
