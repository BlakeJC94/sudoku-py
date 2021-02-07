
class Sudoku(object):
    def __init__(self, file_path):
        self.file_path = file_path
        self.puzzle, self.dim = self.load_puzzle(file_path)

    def load_puzzle(self, file_path):
        with open(file_path,'r') as f:
            lines = f.readlines()

        rows = list()
        puzzle = list()
        for line in lines:
            if line[0] != "-":
                row = line.strip().replace("|", ",").split(",")
                row = list(map(int,row))
                rows.append(row)
                puzzle = puzzle + row

        length = len(row)
        dim = (length == 4)*2 + (length == 3)*3

        return puzzle, dim

    def display(self):
        for row_number in range(self.dim**2):
            row = self.get_row(row_number*self.dim**2)
            row_output = str()
            for row_index, row_element in enumerate(row):
                row_output = row_output + str(row_element)
                if not ((row_index+1) % self.dim):
                    if row_index < self.dim**2 - 1:
                        row_output = row_output + '|'
                else:
                    row_output = row_output + ','

            if not ((row_number+1) % self.dim):
                if row_number < self.dim**2 - 1:
                    row_output = row_output + '\n' + '-'*(self.dim**3 - 1)

            print(row_output)

    def get_row(self, index):
        row_number = ((index + 1) // self.dim**2)
        start = row_number*(self.dim**2)
        end = start + (self.dim**2)
        row = self.puzzle[start:end]
        return row

    def get_col(self, index):
        col = list()
        start = index % self.dim**2
        col = self.puzzle[start::self.dim**2]
        return col

    def get_block(self, index):
        block = list()
        return block

    def solve(self):
        # for puzzle_index in range(len(self.puzzle)):
            # row = get_row(puzzle_index)
            # col = get_col(puzzle_index)
            # block = get_block(puzzle_inex)

        pass


file_path = './input.txt'
sudoku = Sudoku(file_path)
sudoku.display()
