from sudoku_py import Puzzle, Solver


INPUT = 'puzzles/3_dim/hard/input_0.txt'

if __name__ == '__main__':
    bar = Solver()
    foo = Puzzle(INPUT)

    print("Given puzzle:")
    print(foo)

    print("Solving...")
    baz = bar(foo)

    print("Solution:")
    print(baz)

    print("PASS! :)")
