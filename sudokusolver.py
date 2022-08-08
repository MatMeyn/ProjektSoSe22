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

hardest_sudoku = [[1, 0, 0, 0, 0, 7, 0, 9, 0],
               [0, 3, 0, 0, 2, 0, 0, 0, 8],
               [0, 0, 9, 6, 0, 0, 5, 0, 0],
               [0, 0, 5, 3, 0, 0, 9, 0, 0],
               [0, 1, 0, 0, 8, 0, 0, 0, 2],
               [6, 0, 0, 0, 0, 4, 0, 0, 0],
               [3, 0, 0, 0, 0, 0, 0, 1, 0],
               [0, 4, 0, 0, 0, 0, 0, 0, 7],
               [0, 0, 7, 0, 0, 0, 3, 0, 0]]

subgrids = {1: {(0, 0), (0, 1), (0, 2),
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
                (8, 6), (8, 7), (8, 8)}}


class SudokuSolver:
    def __init__(self, unfinished_sudoku):
        self.stack = []
        self.subgrid = subgrids
        self.all_possibilities = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.rows = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.columns = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.sudoku = self.create_2d(unfinished_sudoku)
        self.initiate_stack()

    # helper functions
    def create_2d(self, unfinished_sudoku) -> list:
        empty_sudoku = [[self.all_possibilities.copy() for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                if unfinished_sudoku[i][j] > 0:
                    empty_sudoku[i][j] = unfinished_sudoku[i][j]
        return empty_sudoku

    def is_solved(self) -> bool:
        solved = 0
        for i in range(9):
            for j in range(9):
                if isinstance(self.sudoku[i][j], int):
                    solved += 1
        return solved == 81

    def count_clues_in_box(self, quadrant) -> collections.Counter:
        counter_local = collections.Counter()
        for index in subgrids[quadrant]:
            x = index[0]
            y = index[1]
            if isinstance(self.sudoku[x][y], list):
                counter_local.update(collections.Counter(self.sudoku[x][y]))
        return counter_local

    # lamda?
    def initiate_stack(self):
        for i in range(9):
            for j in range(9):
                if isinstance(self.sudoku[i][j], list):
                    pass
                else:
                    self.stack_append(row=i, column=j, number=self.sudoku[i][j])

    def stack_append(self, row, column, number):
        if not any((d["row"] == row and d["column"] == column and d["number"] == number) for d in self.stack):
            self.stack.append({
                "row": row,
                "column": column,
                "number": number
            })

    def set_digit(self):
        top = self.stack.pop()
        row = top["row"]
        column = top["column"]
        number = top["number"]
        print(f"pulled {top} from stack")
        self.collapse(row, column, number)

        if isinstance(self.sudoku[row][column], list):
            self.sudoku[row][column] = number

    def solve_next(self) -> list:
        if len(self.stack) > 0:
            self.set_digit()
            return self.sudoku
        else:
            self.pointing()
            # self.box_line()
            self.set_single_clue()
            self.set_last_possible()

    def set_single_clue(self):
        for i in range(9):
            for j in range(9):
                if isinstance(self.sudoku[i][j], list):
                    if len(self.sudoku[i][j]) == 1:
                        # umwandlung von list zu int einfacher möglich?
                        temp = self.sudoku[i][j].copy()
                        num = temp.pop()
                        print(f"giving single clue {num} row {i} column {j} to stack")
                        self.stack_append(row=i, column=j, number=num)

    # Solving-functions
    def set_last_possible(self):
        # horizontal
        counter_hor = collections.Counter()
        for i in range(9):
            for j in range(9):
                if isinstance(self.sudoku[i][j], list):
                    counter_temp = collections.Counter(self.sudoku[i][j])
                    counter_hor += counter_temp
            digits = [k for k, v in counter_hor.items() if v == 1]
            print(f"digits {digits}")
            print(f"counter_horizontal {counter_hor}")
            counter_hor.clear()
            for digit in digits:
                for j in range(9):
                    if isinstance(self.sudoku[i][j], list) and digit in self.sudoku[i][j]:
                        print(f"last_possible_horizontal giving {digit} row {i} colum {j} to set_digit")
                        self.stack_append(row=i, column=j, number=digit)

        # vertical
        counter_ver = collections.Counter()
        for i in range(9):
            for j in range(9):
                if isinstance(self.sudoku[j][i], list):
                    counter_ver.update(collections.Counter(self.sudoku[j][i]))
            digits = [k for k, v in counter_ver.items() if v == 1]
            print(f"digits {digits}")
            print(f"counter_vertical {counter_ver}")
            counter_ver.clear()
            for digit in digits:
                for j in range(9):
                    if isinstance(self.sudoku[j][i], list) and digit in self.sudoku[j][i]:
                        print(f"last_possible_vertical giving {digit} row {j} colum {i} to set_digit")
                        self.stack_append(row=j, column=i, number=digit)

        for quadrant in self.subgrid:
            counter_local = self.count_clues_in_box(quadrant)
            digits = [k for k, v in counter_local.items() if v == 1]
            print(f"digits {digits}")
            print(f"counter_local {counter_local}")
            counter_local.clear()
            for digit in digits:
                for index in subgrids[quadrant]:
                    x = index[0]
                    y = index[1]
                    if isinstance(self.sudoku[x][y], list) and digit in self.sudoku[x][y]:
                        print(f"last_possible_local giving {digit} row {x} column {y} to set_digit")
                        self.stack_append(row=x, column=y, number=digit)

    # Reductive functions
    def remove_clue(self, row, column, number):
        if isinstance(self.sudoku[row][column], list):
            if number in self.sudoku[row][column]:
                self.sudoku[row][column].remove(number)

    # collapsing clues after setting of new number ??maybe put into setfunction??
    def collapse(self, row, column, number):
        print(f"collapsing {number} in row {row} column {column}")
        # collapsing horizontal and vertical
        for x in range(9):
            self.remove_clue(row=x, column=column, number=number)
            self.remove_clue(row=row, column=x, number=number)

        # collapsing local
        for quadrants in self.subgrid:
            if (row, column) in self.subgrid[quadrants]:
                for index in self.subgrid[quadrants]:
                    x = index[0]
                    y = index[1]
                    self.remove_clue(row=x, column=y, number=number)

    # pointing pairs and triples
    def pointing(self):
        for box in self.subgrid:
            box_rows = set([row for row, column in self.subgrid[box]])  # all poss. r/c in curr. box
            box_columns = set([column for row, column in self.subgrid[box]])
            other_rows = [item for item in self.rows if item not in box_rows]  # all other r/c outside box
            other_columns = [item for item in self.columns if item not in box_columns]
            counter = self.count_clues_in_box(box)
            digits = [(k, v) for k, v in counter.items() if (v == 2 or v == 3)]  # clue 2 oder 3 mal vorhanden
            # rows
            for row in box_rows:
                counter = collections.Counter()
                for column in box_columns:
                    if isinstance(self.sudoku[row][column], list):
                        counter.update(collections.Counter(self.sudoku[row][column]))
                for k in digits:
                    if k in counter.items():
                        for i in other_columns:
                            self.remove_clue(row=row, column=i, number=k[0])
                counter.clear()
            # columns
            for column in box_columns:
                counter = collections.Counter()
                for row in box_rows:
                    if isinstance(self.sudoku[row][column], list):
                        counter.update(collections.Counter(self.sudoku[row][column]))
                for k in digits:
                    if k in counter.items():
                        for i in other_rows:
                            self.remove_clue(row=i, column=column, number=k[0])
                counter.clear()
            print(f"subgrid {box} counts {counter}")
            print(f"digits only there 2 or 3 times: {digits}")
            print(f"in this quadrant are rows -> {box_rows} columns -> {box_columns}")
            counter.clear()
        pass

    # box-line reduction
    def box_line(self):
        pass

    # test-functions
    def get_main_sudoku(self):
        return self.sudoku

    def get_stack(self):
        return self.stack

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


start = time.perf_counter()
abc = SudokuSolver(test_sudoku)
for count in range(300):
    abc.solve_next()
    abc.print_sudoku()
    abc.get_stack()
    abc.get_main_sudoku()
    # if count == 1:
        # abc.remove_clue(4, 6, 1)
        # abc.remove_clue(4, 7, 1)
        # abc.remove_clue(4, 8, 1)
        # abc.remove_clue(4, 6, 7)
        # abc.remove_clue(4, 7, 7)
        # abc.remove_clue(4, 8, 7)
    print(f'Iterations: {count}')
    if abc.is_solved():
        break
end = time.perf_counter()
print(f"Total Time used is {end - start:0.2f}s")
