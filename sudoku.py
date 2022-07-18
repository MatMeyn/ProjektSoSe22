import numpy as np
import time
import os
import collections

#TEST1

test_sudoku = [[4, 0, 6, 7, 5, 1, 0, 8, 0],
         [2, 0, 8, 0, 0, 0, 4, 7, 0],
         [0, 0, 0, 0, 0, 0, 9, 0, 6],
         [5, 3, 0, 2, 0, 0, 0, 0, 0],
         [6, 4, 9, 1, 3, 0, 0, 0, 0],
         [0, 0, 7, 9, 0, 5, 1, 0, 0],
         [0, 7, 0, 8, 2, 9, 0, 5, 0],
         [0, 6, 2, 0, 1, 0, 0, 3, 8],
         [1, 8, 0, 0, 0, 7, 0, 0, 9]]

hard_sudoku = [[0, 0, 9, 3, 0, 0, 0, 0, 5],
         [0, 0, 0, 0, 0, 0, 9, 8, 0],
         [7, 5, 0, 0, 0, 8, 0, 0, 2],
         [5, 3, 4, 0, 6, 0, 2, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 2, 0, 4, 0, 8, 6, 9],
         [8, 0, 0, 1, 0, 0, 0, 9, 4],
         [0, 4, 7, 0, 0, 0, 0, 0, 0],
         [6, 0, 0, 0, 0, 5, 3, 0, 0]]


def print_sudoku(sudoku):
    row_count = 0
    column_count = 0

    class color:
        RED = '\033[91m'
        BOLD = '\033[1m'
        END = '\033[0m'

    all_possibilities = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    for elem in sudoku:
        top = "|"
        middle = "|"
        bottom = "|"
        if row_count % 3 == 0:
            print(color.BOLD + "_" * 73 + color.END)
        else:
            print("_" * 73)
        row_count += 1
        for type in elem:
            column_count += 3
            if isinstance(type, list):
                possibles = type.copy()
                for num in all_possibilities:
                    if num not in possibles:
                        possibles.insert(num - 1, " ")
                top += color.RED + f" {possibles[0]} {possibles[1]} {possibles[2]} " + color.END + "|"
                middle += color.RED + f" {possibles[3]} {possibles[4]} {possibles[5]} " + color.END + "|"
                bottom += color.RED + f" {possibles[6]} {possibles[7]} {possibles[8]} "+ color.END + "|"

            else:
                top += "       |"
                middle += color.BOLD + f"   {type}   " + color.END + "|"
                bottom += "       |"

        print(top)
        print(middle)
        print(bottom)


def create_2d_sudoku_array(unfinished_sudoku):
    row, column = 9, 9
    all_possibilities = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    empty_sudoku = [[all_possibilities.copy() for i in range(column)] for j in range(row)]

    for i in range(9):
        for j in range(9):
            if unfinished_sudoku[i][j] > 0:
                empty_sudoku[i][j] = unfinished_sudoku[i][j]

    return empty_sudoku


def create_subgrids():
    subgrids = {
        1: {(0, 0), (0, 1), (0, 2),
            (1, 0), (1, 1), (1, 2),
            (2, 0), (2, 1), (2, 2)},
        2: {(0, 3), (0, 4), (0, 5),
            (1, 3), (1, 4), (1, 5),
            (2, 3), (2, 4), (2, 5)},
        3: {(0, 6), (0, 7), (0, 8),
            (1, 6), (1, 7), (1, 8),
            (2, 6), (2, 7), (2, 8)},
        4: {(3, 0), (3, 1), (3, 2),
            (4, 0), (4, 1), (4, 2),
            (5, 0), (5, 1), (5, 2)},
        5: {(3, 3), (3, 4), (3, 5),
            (4, 3), (4, 4), (4, 5),
            (5, 3), (5, 4), (5, 5)},
        6: {(3, 6), (3, 7), (3, 8),
            (4, 6), (4, 7), (4, 8),
            (5, 6), (5, 7), (5, 8)},
        7: {(6, 0), (6, 1), (6, 2),
            (7, 0), (7, 1), (7, 2),
            (8, 0), (8, 1), (8, 2)},
        8: {(6, 3), (6, 4), (6, 5),
            (7, 3), (7, 4), (7, 5),
            (8, 3), (8, 4), (8, 5)},
        9: {(6, 6), (6, 7), (6, 8),
            (7, 6), (7, 7), (7, 8),
            (8, 6), (8, 7), (8, 8)}
    }
    return subgrids


def solving_loop(sudoku):
    stack = initiate_stack(sudoku)
    subgrids = create_subgrids()
    #while len(stack) > 0:
    while True:
        if len(stack) > 0:
            top = stack.pop()
            print(f"pulled {top} from stack")
            collapse(sudoku, subgrids, row=top["row"], column=top["column"], number=top["number"])
            set_single_clue(stack, sudoku)
        else:
            set_last_possible(stack, sudoku, subgrids)

        #PROBLEME
        print_sudoku(sudoku)
        time.sleep(0.5)
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        if len(stack) == 0:
            if sudoku_solved(sudoku):
                print("fertig")
                break


#TODO higher order functions
def collapse(sudoku, subgrids, row, column, number):
    print(f"collapsing {number} in row {row} column {column}")
    collapse_horizontal(sudoku, row, number)
    collapse_vertical(sudoku, column, number)
    collapse_local(sudoku, subgrids, row, column, number)


def collapse_horizontal(sudoku, row, number):
    print(f"collapsing horizontal {number} in row {row}")
    for x in sudoku[row]:
        if isinstance(x, list):
            if number in x:
                print(f"set an dieser stelle{x}")
                x.remove(number)


def collapse_vertical(sudoku, column, number):
    print(f"collapsing vertical {number} in column {column}")
    for x in range(9):
        if isinstance(sudoku[x][column], list):
            if number in sudoku[x][column]:
                print(f"set an dieser stelle{sudoku[x][column]}")
                sudoku[x][column].remove(number)


def collapse_local(sudoku, subgrids, row, column, number):
    print(f"collapsing local {number} in row {row} column {column}")
    for quadrants in subgrids:
        if (row, column) in subgrids[quadrants]:
            for index in subgrids[quadrants]:
                x = index[0]
                y = index[1]
                if isinstance(sudoku[x][y], list):
                    if number in sudoku[x][y]:
                        print(f"set an dieser stelle{sudoku[x][y]}")
                        sudoku[x][y].remove(number)


def set_digit(stack, sudoku, row, column, number):
    #time.sleep(0.5)
    sudoku[row][column] = number
    stack_append(stack, row, column, number)
    print(f"set {number} in row {row} column {column}")

#TODO higher order functions
def set_last_possible(stack, sudoku, subgrids):
    if set_last_possible_horizontal(stack, sudoku):
        return True
    elif set_last_possible_vertical(stack, sudoku):
        return True
    elif set_last_possible_local(stack, sudoku, subgrids):
        return True
    else:
        return False


def set_last_possible_horizontal(stack, sudoku):
    #horizontal
    counter_hor = collections.Counter()
    for i in range(9):
        for j in range(9):
            if isinstance(sudoku[i][j], list):
                counter_temp = collections.Counter(sudoku[i][j])
                counter_hor += counter_temp
        digits = [k for k, v in counter_hor.items() if v == 1]
        print(f"digits {digits}")
        print(f"counter_horizontal {counter_hor}")
        counter_hor.clear()
        for digit in digits:
            for j in range(9):
                if isinstance(sudoku[i][j], list) and digit in sudoku[i][j]:
                    print(f"last_possible_horizontal giving {digit} row {i} colum {j} to set_digit")
                    set_digit(stack, sudoku, row=i, column=j, number=digit)
                    return True


def set_last_possible_vertical(stack, sudoku):
    #vertical
    counter_ver = collections.Counter()
    for i in range(9):
        for j in range(9):
            if isinstance(sudoku[j][i], list):
                counter_ver.update(collections.Counter(sudoku[j][i]))
        digits = [k for k, v in counter_ver.items() if v == 1]
        print(f"digits {digits}")
        print(f"counter_vertical {counter_ver}")
        counter_ver.clear()
        for digit in digits:
            for j in range(9):
                if isinstance(sudoku[j][i], list) and digit in sudoku[j][i]:
                    print(f"last_possible_vertical giving {digit} row {j} colum {i} to set_digit")
                    set_digit(stack, sudoku, row=j, column=i, number=digit)
                    return True


def set_last_possible_local(stack, sudoku, subgrids):
    counter_local = collections.Counter()
    for quadrants in subgrids:
        for index in subgrids[quadrants]:
            x = index[0]
            y = index[1]
            if isinstance(sudoku[x][y], list):
                counter_local.update(collections.Counter(sudoku[x][y]))
        digits = [k for k, v in counter_local.items() if v == 1]
        print(f"digits {digits}")
        print(f"counter_local {counter_local}")
        counter_local.clear()
        for digit in digits:
            for index in subgrids[quadrants]:
                x = index[0]
                y = index[1]
                if isinstance(sudoku[x][y], list) and digit in sudoku[x][y]:
                    print(f"last_possible_local giving {digit} row {x} column {y} to set_digit")
                    set_digit(stack, sudoku, row=x, column=y, number=digit)
                    return True


def set_single_clue(stack, sudoku):
    for i in range(9):
        for j in range(9):
            if isinstance(sudoku[i][j], list):
                if len(sudoku[i][j]) == 1:
                    num = sudoku[i][j].pop()
                    print(f"giving single clue {num} row {i} column {j} to set_digit")
                    set_digit(stack, sudoku, row=i, column=j, number=num)
                    return True

#lamda?
def initiate_stack(sudoku):
    stack = []
    for i in range(9):
        for j in range(9):
            if isinstance(sudoku[i][j], list):
                pass
            else:
                stack_append(stack, row=i, column=j, number=sudoku[i][j])
    return stack


def stack_append(stack, row, column, number):
    stack.append({
                    "row": row,
                    "column": column,
                    "number": number
                    })
    print(f"appended {number} in row {row} column {column} to stack")


def sudoku_solved(sudoku):
    print("check?")
    #Listcomprehension 2d array
   # [[all_possibilities.copy() for i in range(column)] for j in range(row)]
    #print([[for i in range(9)] isinstance(item, int) for item in sudoku[i]])
    return all([isinstance(item, int) for item in sudoku])


def solve():
    solvable = create_2d_sudoku_array(hard_sudoku)
    #solvable = create_2d_sudoku_array(test_sudoku)
    solving_loop(solvable)