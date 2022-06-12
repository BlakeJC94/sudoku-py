class Sudoku(object):
    def __init__(self, file_path):
        self.file_path = file_path
        self.output_path = './output.txt'
        self.puzzle, self.dim = self.load_puzzle(file_path)
        self.hist_index = 0
        self.puzzle_hist = list()
        self.puzzle_hist.append(self.puzzle)
        self.poss_hist = list()
        self.poss_hist.append(['']*len(self.puzzle))
        self.total_sweeps = 10000

    def load_puzzle(self, file_path):
        with open(file_path, 'r') as f:
            lines = f.readlines()

        rows = list()
        puzzle = list()
        for line in lines:
            if line[0] != "-":
                row = line.strip().replace("|", ",").split(",")
                row = list(map(int, row))
                rows.append(row)
                puzzle = puzzle + row

        length = len(row)
        dim = (length == 4)*2 + (length == 9)*3

        return puzzle, dim

    def get_row(self, index):
        dim = self.dim
        row_number = (index // dim**2)
        start = row_number*(dim**2)
        end = start + (dim**2)
        row = self.puzzle[start:end]
        return row

    def get_col(self, index):
        col = list()
        start = index % self.dim**2
        col = self.puzzle[start::self.dim**2]
        return col

    def get_block(self, index):
        dim = self.dim
        # find topleft corner index
        row_number = index // dim**3
        col_number = index % dim**2
        block_index = dim**3 * row_number + dim * (col_number // dim)

        block = list()
        for i in range(dim**2):
            selected_index = block_index + (i % dim) + i % (dim ** 2)
            row_add = i % dim
            col_add = i // dim
            selected_index = block_index + row_add + col_add * dim**2
            block.append(self.puzzle[selected_index])

        return block

    def get_possibilities(self, puzzle_index):
        possibilities = set(range(1, self.dim**2+1))
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
        possibility_counts = list(map(len, possibility_sweep))
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

    def get_row_str(self, row_index, row):
        dim = self.dim
        row_str = str()
        for index, element in enumerate(row):
            row_str += str(element)
            if (index+1) % dim == 0:
                if index+1 == dim**2:
                    row_str += '\n'
                else:
                    row_str += '|'
            else:
                row_str += ','

        line = ('-'*(2*dim-1)+'+')*(dim-1)+'-'*(2*dim - 1)+'\n'
        if ((row_index+1) % dim == 0) and (row_index < dim**2-1):
            row_str += line

        return row_str

    def print_solution(self, *output_path):
        if output_path:
            target = open(output_path[0], 'w')

        dim = self.dim
        rows = [self.get_row(i) for i in range(0, dim**4, dim**2)]
        for row_index, row in enumerate(rows):
            row_str = self.get_row_str(row_index, row)

            if output_path:
                target.write(row_str)
            else:
                print(row_str[:-1])

        if output_path:
            target.close()

        pass

    def solve(self):
        print("Solving puzzle")
        self.print_solution()
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
                        possibility_counts = list(map(len, possibility_sweep))
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
                    self.print_solution()
                    self.print_solution(self.output_path)
                    sweep = False
                else:
                    print("Multiple possibilities")
                    self.print_solution()
                    self.guess(possibility_sweep)
        pass
