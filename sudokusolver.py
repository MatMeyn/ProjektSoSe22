import time
import collections

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


class SudokuSolver:
    def __init__(self, unfinished_sudoku):
        self.stack = []
        self.subgrid = subgrids
        self.all_possibilities = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.sudoku = self.create_2d(unfinished_sudoku)
        self.initiate_stack()

    def create_2d(self, unfinished_sudoku):
        empty_sudoku = [[self.all_possibilities.copy() for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                if unfinished_sudoku[i][j] > 0:
                    empty_sudoku[i][j] = unfinished_sudoku[i][j]
        return empty_sudoku

    # lamda?
    def initiate_stack(self):
        for i in range(9):
            for j in range(9):
                if isinstance(self.sudoku[i][j], list):
                    pass
                else:
                    self.stack_append(row=i, column=j, number=self.sudoku[i][j])

    def stack_append(self, row, column, number):
        self.stack.append({
            "row": row,
            "column": column,
            "number": number
        })
        print(f"appended {number} in row {row} column {column} to stack")

    def set_digit(self):
        top = self.stack.pop()
        row = top["row"]
        column = top["column"]
        number = top["number"]
        print(f"pulled {top} from stack")
        self.collapse(row, column, number)

        if isinstance(self.sudoku[row][column], list):
            self.sudoku[row][column] = number

    def solve_next(self):
        if len(self.stack) > 0:
            self.set_digit()
            return self.sudoku
        else:
            self.set_single_clue()
            #self.set_last_possible()


    def is_solved(self):
        solved = 0
        for i in range(9):
            for j in range(9):
                if isinstance(self.sudoku[i][j], int):
                    solved += 1
        return solved == 81

    def collapse(self, row, column, number):
        print(f"collapsing {number} in row {row} column {column}")
        print(f"collapsing horizontal {number} in row {row}")
        for x in self.sudoku[row]:
            if isinstance(x, list):
                if number in x:
                    print(f"set an dieser stelle{x}")
                    x.remove(number)

        print(f"collapsing vertical {number} in column {column}")
        for x in range(9):
            if isinstance(self.sudoku[x][column], list):
                if number in self.sudoku[x][column]:
                    print(f"set an dieser stelle{self.sudoku[x][column]}")
                    self.sudoku[x][column].remove(number)

        print(f"collapsing local {number} in row {row} column {column}")
        for quadrants in self.subgrid:
            if (row, column) in self.subgrid[quadrants]:
                for index in self.subgrid[quadrants]:
                    x = index[0]
                    y = index[1]
                    if isinstance(self.sudoku[x][y], list):
                        if number in self.sudoku[x][y]:
                            print(f"set an dieser stelle{self.sudoku[x][y]}")
                            self.sudoku[x][y].remove(number)

    def set_single_clue(self):
        for i in range(9):
            for j in range(9):
                if isinstance(self.sudoku[i][j], list):
                    if len(self.sudoku[i][j]) == 1:
                        #umwandlung von list zu int einfacher möglich?
                        temp = self.sudoku[i][j].copy()
                        num = temp.pop()
                        print(f"giving single clue {num} row {i} column {j} to stack")
                        self.stack_append(row=i, column=j, number=num)

    #testfunctions
    def get_main_sudoku(self):
        print(self.sudoku)

    def get_stack(self):
        print(self.stack)

    def print_sudoku(self):
        row_count = 0
        column_count = 0

        class Color:
            RED = '\033[91m'
            BOLD = '\033[1m'
            END = '\033[0m'

        for elem in self.sudoku:
            top = "|"
            middle = "|"
            bottom = "|"
            if row_count % 3 == 0:
                print(Color.BOLD + "_" * 73 + Color.END)
            else:
                print("_" * 73)
            row_count += 1
            for type in elem:
                column_count += 3
                if isinstance(type, list):
                    possibles = type.copy()
                    for num in self.all_possibilities:
                        if num not in possibles:
                            possibles.insert(num - 1, " ")
                    top += Color.RED + f" {possibles[0]} {possibles[1]} {possibles[2]} " + Color.END + "|"
                    middle += Color.RED + f" {possibles[3]} {possibles[4]} {possibles[5]} " + Color.END + "|"
                    bottom += Color.RED + f" {possibles[6]} {possibles[7]} {possibles[8]} " + Color.END + "|"

                else:
                    top += "       |"
                    middle += Color.BOLD + f"   {type}   " + Color.END + "|"
                    bottom += "       |"

            print(top)
            print(middle)
            print(bottom)


abc = SudokuSolver(test_sudoku)
for _ in range(500):
    abc.solve_next()
    abc.print_sudoku()
    abc.get_stack()
    abc.get_main_sudoku()
    if abc.is_solved():
        break
