
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
        dim = (length == 4)*2 + (length == 9)*3

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
                    row_output = row_output + '\n' + '-'*(2*(self.dim**2) - 1)

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

    def get_possibilities(self, puzzle_index):
        possibilities = set(range(1,self.dim**2+1))
        row = set(self.get_row(puzzle_index))
        col = set(self.get_col(puzzle_index))
        block = set(self.get_block(puzzle_index))

        present = block.union(row).union(col)
        possibilities = list(possibilities.difference(present))
        return possibilities

    def solve(self):
        total_sweeps = 1000
        sweep = True
        sweep_num = 0

        checkpoint_index = 0
        checkpoints_puzzle = list()
        checkpoints_puzzle.append(self.puzzle)
        checkpoints_possibilities = list()
        checkpoints_possibilities.append([''])

        while sweep:
            # start sweep
            change_made = False
            sweep_num += 1
            possibility_sweep = ['']*len(self.puzzle)
            if sweep_num > total_sweeps:
                print("exceeded total_sweeps")
                break

            for puzzle_index in range(len(self.puzzle)):
                if self.puzzle[puzzle_index] == 0:

                    possibilities = self.get_possibilities(puzzle_index)

                    if len(possibilities) > 1:
                        possibility_sweep[puzzle_index] = possibilities

                    elif len(possibilities) == 1:
                        self.puzzle[puzzle_index] = possibilities[0]
                        change_made = True

                    elif len(possibilities) == 0:
                        print("INDETERMINENT, restore previous guess")
                        print(len(checkpoints_puzzle))
                        self.puzzle = checkpoints_puzzle[checkpoint_index]
                        checkpoints_puzzle.pop()
                        possibility_sweep = checkpoints_possibilities[checkpoint_index]
                        checkpoints_possibilities.pop()
                        checkpoint_index -= 1
                        if checkpoint_index < 0:
                            print("ERROR")
                            sweep = False
                            raise ValueError("checkpoint_index must be positive")
                        break

            print(f"\nCompleted sweep {sweep_num}")

            if not change_made:

                if min(self.puzzle) > 0:
                    print("Puzzle solved!")
                    self.display()
                    sweep = False
                else:
                    print("Multiple possibilities")
                    self.display()
                    # save puzzle state
                    print("INCREASE CHKIND")
                    checkpoint_index += 1
                    checkpoints_puzzle.append(self.puzzle)
                    print(len(checkpoints_puzzle))
                    print(checkpoint_index)

                    # find index with lowest number of possibilities
                    selected_index = 0
                    for i, possibility in enumerate(possibility_sweep):
                        # import pdb; pdb.set_trace()
                        if len(possibility_sweep[selected_index]) < 1:
                            selected_index = i
                        if len(possibility) < len(possibility_sweep[selected_index]):
                            if len(possibility) > 0:
                                selected_index = i

                    # guess and remove from possibility list
                    self.puzzle[selected_index] = possibility_sweep[selected_index][-1]
                    possibility_sweep[selected_index].pop()
                    checkpoints_possibilities.append(possibility_sweep)

        pass


file_path = './3_dim_hard.txt'
sudoku = Sudoku(file_path)
# import pdb; pdb.set_trace()
sudoku.display()
sudoku.solve()
