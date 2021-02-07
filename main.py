"""Sudoku-py

Main file
"""






def get_col(rows, col_index):
    col = list()
    for row in rows:
        col.append(row[col_index])
    return col


def get_block(rows, row_index, col_index):
    block = list()
    # ...
    return block

# Read sudoku puzzle from data
with open('input.txt','r') as f:
    lines = f.readlines()
    rows = list()

    for line in lines:
        if line[0] != "-":
            row = line.strip().replace("|", ",").split(",")
            row = list(map(int,row))
            rows.append(row)

    length = len(row)
    if length == 4:
        dim = 2
    elif length == 9:
        dim = 3

print(rows)
print(dim)


# Preallocate possibility array
possibilities = [['']*(dim^2)]*len(rows)
print(possibilities)

# Loop over each row
for row_index, row in enumerate(rows):
    for col_index in range(len(row)):
        col = get_col(rows, col_index)
        block = get_block(rows, row_index, col_index)






# Construct lists for selected row, col, block
# Eliminate possibilities at cell
# If one possibility, fill value
# Mark
