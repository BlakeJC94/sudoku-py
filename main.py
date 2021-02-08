
class Sudoku(object):
    def __init__(self, file_path):
        self.file_path = file_path
        self.puzzle, self.dim = self.load_puzzle(file_path)
        self.display()

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
        row_number = (index // self.dim**2)
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
        # find topleft corner index
        row_number = index // self.dim**3
        col_number = index % self.dim**2
        block_index = self.dim**3 * row_number + self.dim * (col_number // self.dim)

        block = list()
        for i in range(self.dim**2):
            selected_index = block_index + (i % self.dim) + i % (self.dim ** 2)
            row_add = i % self.dim
            col_add = i // self.dim
            selected_index = block_index + row_add + col_add * self.dim**2
            block.append(self.puzzle[selected_index])

        return block

    def solve(self):
        total_sweeps = 10
        for sweep in range(total_sweeps):

            change_made = False
            for puzzle_index in range(len(self.puzzle)):
                possibilities = set(range(1,self.dim**2+1))
                row = set(self.get_row(puzzle_index))
                col = set(self.get_col(puzzle_index))
                block = set(self.get_block(puzzle_index))

                present = block.union(row).union(col)
                possibilities = list(possibilities.difference(present))

                if len(possibilities) == 1:
                    self.puzzle[puzzle_index] = possibilities[0]
                    change_made = True

            print(f"\nCompleted sweep {sweep+1}")
            self.display()

            if not change_made and min(self.puzzle) > 0:
                print("Puzzle solved!")
                break

            if not change_made:
                print("Multiple possibilities")

        pass


file_path = './input.txt'
sudoku = Sudoku(file_path)
sudoku.solve()
