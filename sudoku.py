class Sudoku(object):
    def __init__(self, file_path):
        self.file_path = file_path
        self.puzzle, self.dim = self.load_puzzle(file_path)
        self.hist_index = 0
        self.puzzle_hist = list()
        self.puzzle_hist.append(self.puzzle)
        self.poss_hist = list()
        self.poss_hist.append(['']*len(self.puzzle))
        self.total_sweeps = 1000

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

    def restore(self):
        # check if input is inconsistent
        if self.hist_index == 0:
            print("Puzzle is not solvable?")
            raise ValueError("hist_index == 0")
        # revert puzzle to current checkpoint and remove from hist
        self.puzzle = self.puzzle_hist.pop().copy()
        possibility_sweep = self.poss_hist.pop().copy()
        # decrease checkpoint index
        self.hist_index -= 1
        return possibility_sweep

    def save_state(self, possibility_sweep):
        # increase checkpoint index
        self.hist_index += 1
        # save puzzle to history before making guess
        self.puzzle_hist.append(self.puzzle.copy())
        self.poss_hist.append(possibility_sweep.copy())
        pass

    def guess(self, possibility_sweep):
        # find puzzle index with smallest number of possibilities
        possibility_counts = list(map(len,possibility_sweep))
        non_zero_counts = [i for i in possibility_counts if i != 0]
        selected_puzzle_index = possibility_counts.index(min(non_zero_counts))
        # get guess and remove from possibilities
        guess = possibility_sweep[selected_puzzle_index][-1]
        possibility_sweep[selected_puzzle_index].pop()
        # save state
        self.save_state(possibility_sweep)
        # insert guess
        self.puzzle[selected_puzzle_index] = guess
        pass


    def solve(self):
        print("Solving puzzle")
        self.display()
        sweep, sweep_num = True, 0
        while sweep:
            # start sweep
            change_made = False
            sweep_num += 1
            if sweep_num > self.total_sweeps:
                print("exceeded total_sweeps")
                break

            possibility_sweep = ['']*len(self.puzzle)
            for puzzle_index in range(len(possibility_sweep)):
                if self.puzzle[puzzle_index] == 0:

                    possibilities = self.get_possibilities(puzzle_index)

                    if len(possibilities) > 1:
                        possibility_sweep[puzzle_index] = possibilities

                    elif len(possibilities) == 1:
                        self.puzzle[puzzle_index] = possibilities[0]
                        change_made = True

                    elif len(possibilities) == 0:
                        print("INDETERMENENT, restore previous guess")
                        possibility_sweep = self.restore()
                        # if one possibility in checkpoint, make change
                        possibility_counts = list(map(len,possibility_sweep))
                        single_counts = [i for i in possibility_counts if i == 1]
                        if len(single_counts) > 0:
                            # import pdb; pdb.set_trace()
                            selected_index = possibility_counts.index(1)
                            possibilities = possibility_sweep[selected_index]
                            self.puzzle[selected_index] = possibilities[0]
                            change_made = True

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
                    self.guess(possibility_sweep)
        pass
