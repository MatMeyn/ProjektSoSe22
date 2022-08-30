""" Author: Matthias Meyn
    Project for Skriptsprachen SS2022 """

import collections
import copy
from subgrid import subgrids


class SudokuSolver:
    def __init__(self, unfinished_sudoku):
        self.stack = []
        self.subgrid = subgrids
        self.all_possibilities = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.rows = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.columns = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.sudoku = self.create_2d_from_string(unfinished_sudoku)
        self.sudoku_before_guess = None
        self.previous_sudoku = None
        self.highlight_index = ()
        self.possible_guess = []
        self.shortest_list_generator = None
        self.initiate_stack()

    def solve_next(self):
        """ This is the main solving function used by the GUI.
        Every GUI update calls this function once.
        If the stack is not empty it collapses(reduces) clues for each solved tile,
        else it uses the other solving functions to advance the sudoku grid.
        If the Sudoku Solver is stuck it makes use of the guessing function"""
        self.previous_sudoku = copy.deepcopy(self.sudoku)
        if len(self.stack) > 0:
            self.set_digit()
        else:
            self.pointing()
            self.box_line()
            self.naked_pairs()
            self.set_single_clue()
            self.set_last_possible()
        if self.is_stuck():
            self.make_a_guess()

    def initiate_stack(self):
        """ Initiates the stack with every already pre-solved tile. """
        for i in range(9):
            for j in range(9):
                if isinstance(self.sudoku[i][j], int):
                    self.stack_append(row=i, column=j, number=self.sudoku[i][j])

    def stack_append(self, row, column, number):
        """ Appends a solved tile to the stack if not already present.
            Used by the functions that solve a tile """
        if not any((d["row"] == row and d["column"] == column and d["number"] == number) for d in self.stack):
            self.stack.append({
                "row": row,
                "column": column,
                "number": number
            })

    def set_digit(self):
        """ Takes a solved tile from the stack to collapse every clue its number influences,
        and set it in the sudoku grid if not already present. """
        top = self.stack.pop()
        row = top["row"]
        column = top["column"]
        number = top["number"]
        self.highlight_index = (row, column)
        self.collapse(row, column, number)
        if isinstance(self.sudoku[row][column], list):
            self.sudoku[row][column] = number

    # reduction of clues
    def remove_clue(self, row, column, number):
        """ Helper function to remove a single clue from a single tile """
        if isinstance(self.sudoku[row][column], list):
            if number in self.sudoku[row][column]:
                self.sudoku[row][column].remove(number)

    def collapse(self, row, column, number):
        """ Collapses(reduces) the clues of a given number in the row, column and box of the given solved tile """
        for x in range(9):
            self.remove_clue(row=x, column=column, number=number)
            self.remove_clue(row=row, column=x, number=number)

        # collapsing box
        for box in self.subgrid:
            if (row, column) in self.subgrid[box]:
                for index in self.subgrid[box]:
                    x = index[0]
                    y = index[1]
                    self.remove_clue(row=x, column=y, number=number)

    ############################# Solving functions #############################
    def set_single_clue(self):
        """ Solves a tile if there is only a single clue left """
        for i in range(9):
            for j in range(9):
                if isinstance(self.sudoku[i][j], list):
                    if len(self.sudoku[i][j]) == 1:
                        temp = self.sudoku[i][j].copy()
                        num = temp.pop()
                        self.stack_append(row=i, column=j, number=num)

    def set_last_possible(self):
        """ Solves a tile if it contains the last possible number in a row, column or box """
        # row
        for i in range(9):
            counter_row = self.count_clues_in_row(row=i)
            single_clue_row = [k for k, v in counter_row.items() if v == 1]
            counter_row.clear()
            for num in single_clue_row:
                for j in range(9):
                    if isinstance(self.sudoku[i][j], list) and num in self.sudoku[i][j]:
                        self.stack_append(row=i, column=j, number=num)

        # column
        for j in range(9):
            counter_column = self.count_clues_in_column(column=j)
            single_clue_column = [k for k, v in counter_column.items() if v == 1]
            counter_column.clear()
            for num in single_clue_column:
                for i in range(9):
                    if isinstance(self.sudoku[i][j], list) and num in self.sudoku[i][j]:
                        self.stack_append(row=i, column=j, number=num)

        # box
        for box in self.subgrid:
            counter_box = self.count_clues_in_box(box)
            single_clue_box = [k for k, v in counter_box.items() if v == 1]
            counter_box.clear()
            for num in single_clue_box:
                for index in self.subgrid[box]:
                    x = index[0]
                    y = index[1]
                    if isinstance(self.sudoku[x][y], list) and num in self.sudoku[x][y]:
                        self.stack_append(row=x, column=y, number=num)

    def pointing(self):
        """ Solving strategy pointing pairs and pointing triples
            If in a box all clues of a number are in the same row or column those numbers can't be
            in other tiles of this row or column """
        for box in self.subgrid:
            box_rows = set([row for row, column in self.subgrid[box]])  # all poss. r/c indices in curr. box
            box_columns = set([column for row, column in self.subgrid[box]])
            other_rows = [row for row in self.rows if row not in box_rows]  # all other r/c indices outside box
            other_columns = [col for col in self.columns if col not in box_columns]
            counter = self.count_clues_in_box(box)
            digits = [(k, v) for k, v in counter.items() if (v == 2 or v == 3)]  # clue 2 or 3 times in box
            # rows
            for row in box_rows:
                counter = self.count_clues_in_box_row(box=box, row=row)
                for k in digits:
                    if k in counter.items():
                        for i in other_columns:
                            self.remove_clue(row=row, column=i, number=k[0])
                counter.clear()
            # columns
            for column in box_columns:
                counter = self.count_clues_in_box_column(box=box, column=column)
                for k in digits:
                    if k in counter.items():
                        for i in other_rows:
                            self.remove_clue(row=i, column=column, number=k[0])
                counter.clear()
            counter.clear()

    def box_line(self):
        """ Box/Line reduction.
            If a number can only be in 2 or 3 tiles and those tiles are in the same box, you can remove
            all other clues of that number from that box """
        # row
        for row in self.rows:
            row_count = self.count_clues_in_row(row=row)
            row_num = [(k, v) for k, v in row_count.items() if (v == 2 or v == 3)]
            for box in self.subgrid.keys():
                box_row_count = self.count_clues_in_box_row(box=box, row=row)
                box_twos_or_threes = [(k, v) for k, v in box_row_count.items() if (v == 2 or v == 3)]
                for kv in row_num:
                    if kv in box_twos_or_threes:
                        indices_to_remove = [x for x in self.subgrid[box] if x[0] != row]
                        for i in indices_to_remove:
                            self.remove_clue(row=i[0], column=i[1], number=kv[0])
        # column
        for column in self.columns:
            column_count = self.count_clues_in_column(column=column)
            col_num = [(k, v) for k, v in column_count.items() if (v == 2 or v == 3)]
            for box in self.subgrid.keys():
                box_col_count = self.count_clues_in_box_column(box=box, column=column)
                box_twos_or_threes = [(k, v) for k, v in box_col_count.items() if (v == 2 or v == 3)]
                for kv in col_num:
                    if kv in box_twos_or_threes:
                        indices_to_remove = [x for x in self.subgrid[box] if x[1] != column]
                        for i in indices_to_remove:
                            self.remove_clue(row=i[0], column=i[1], number=kv[0])

    def naked_pairs(self):
        """Naked Pairs
        If in a row, column or box two clues of the same number are in exactly the same two tiles,
        all the other clues of those numbers can be removed"""
        # get every tile that contains a pair
        pairs = []
        for i in range(9):
            for j in range(9):
                if isinstance(self.sudoku[i][j], list) and len(self.sudoku[i][j]) == 2:
                    pairs.append({
                        "row": i,
                        "column": j,
                        "pair": self.sudoku[i][j]
                    })

        # look for pairs that match in every column, row, box
        for i in range(9):
            col_pairs = list(filter(lambda pair: pair["column"] == i, pairs))
            row_pairs = list(filter(lambda pair: pair["row"] == i, pairs))

            # col
            for p in col_pairs:
                naked_pair = list(filter(lambda same: same["pair"] == p["pair"], col_pairs))
                if len(naked_pair) == 2:
                    nums_to_delete = naked_pair[0]["pair"]
                    rows_to_ignore = [d["row"] for d in naked_pair]
                    for num in nums_to_delete:
                        for row in self.rows:
                            if row not in rows_to_ignore:
                                self.remove_clue(row=row, column=i, number=num)
            # row
            for p in row_pairs:
                naked_pair = list(filter(lambda same: same["pair"] == p["pair"], row_pairs))
                if len(naked_pair) == 2:
                    nums_to_delete = naked_pair[0]["pair"]
                    cols_to_ignore = [d["column"] for d in naked_pair]
                    for num in nums_to_delete:
                        for col in self.columns:
                            if col not in cols_to_ignore:
                                self.remove_clue(row=i, column=col, number=num)
        # box
        for box in self.subgrid:
            box_indices = self.subgrid[box]
            box_pairs = []
            for i in box_indices:
                for pair in pairs:
                    if pair["row"] == i[0] and pair["column"] == i[1]:
                        box_pairs.append(pair)
            for p in box_pairs:
                naked_pair = list(filter(lambda same: same["pair"] == p["pair"], box_pairs))
                if len(naked_pair) == 2:
                    nums_to_delete = naked_pair[0]["pair"]
                    tiles_to_ignore = [(naked_pair[i]["row"], naked_pair[i]["column"]) for i in range(2)]
                    for num in nums_to_delete:
                        for (row, col) in box_indices:
                            if (row, col) not in tiles_to_ignore:
                                self.remove_clue(row=row, column=col, number=num)

    ######################### Guessing function ##########################
    def make_a_guess(self):
        """ This function is used if the Sudoku Solver is stuck
            It guesses a number of a tile where the list of clues is the shortest,
            then the normal solving functions continue.
            If it guessed wrong and the puzzle breaks the sudoku grid is reverted to its original
            state before the first guess.
            Then it guesses the other candidates"""
        if self.sudoku_before_guess is None:
            self.init_guess()
        if not self.is_valid():
            self.restore_sudoku()
        self.guess_digit()

    def init_guess(self):
        """Saves the state of the sudoku grid before a guess.
            Creates a generator for every guessable tile by number of clues ascending to maximize the chance
            of the guess being right"""
        self.sudoku_before_guess = copy.deepcopy(self.sudoku)
        self.shortest_list_generator = self.create_shortest_list_generator()
        self.possible_guess.append(self.shortest_list_generator.__next__())

    def guess_digit(self):
        """Guesses a number
            If the sudoku solver is still stuck it loads the candidates of the next tile for guessing"""
        if len(self.possible_guess[0]["guess"]) == 0:
            self.possible_guess.clear()
            try:
                self.possible_guess.append(self.shortest_list_generator.__next__())
            except StopIteration:
                print("Couldn't solve this Sudoku")
        num_to_guess = self.possible_guess[0]["guess"].pop()
        row = self.possible_guess[0]["row"]
        column = self.possible_guess[0]["column"]
        self.stack_append(row=row, column=column, number=num_to_guess)

    def create_shortest_list_generator(self):
        """Creates a Generator-object which yields every unsolved tile and its candidates sorted by length"""
        for i in range(2, 9):
            for row in self.rows:
                for col in self.columns:
                    if isinstance(self.sudoku[row][col], list):
                        if len(self.sudoku[row][col]) == i:
                            yield {"row": row,
                                   "column": col,
                                   "guess": [x for x in self.sudoku[row][col]]}

    ################ Helper functions ############
    def is_stuck(self) -> bool:
        """ Check if the sudoku solver is stuck (No number to set and no progress between iterations)"""
        return len(self.stack) == 0 and self.sudoku == self.previous_sudoku

    def is_complete(self) -> bool:
        """ Check if every tile is solved """
        complete = 0
        for i in range(9):
            for j in range(9):
                if isinstance(self.sudoku[i][j], int):
                    complete += 1
        return complete == 81

    def is_solved(self) -> bool:
        """ Check if every row and every column adds to 45.
        Since 45 is the sum of 1 to 9, if that is true for every row and every column the sudoku is solved
        Only works if the sudoku grid is fully filled in"""
        row_sums = [sum(row) for row in self.sudoku]
        col_sums = [sum(col) for col in zip(*self.sudoku)]
        if any((d != 45) for d in row_sums) or any((d != 45) for d in col_sums):
            return False
        else:
            return True

    def is_valid(self) -> bool:
        """ Check if the sudoku grid is still valid.
        Fails if:
        Any list of candidates in the grid is emtpy,
        or if any row, column or box contains more than 1 of the same number"""
        for row in self.rows:
            for col in self.columns:
                if isinstance(self.sudoku[row][col], list):
                    if not len(self.sudoku[row][col]) == 0:
                        return False

        for row in self.rows:
            counter_row = collections.Counter([x for x in self.sudoku[row] if isinstance(self.sudoku[row], int)])
            for count in counter_row.values():
                if count > 1:
                    return False

        for col in self.columns:
            counter_col = collections.Counter()
            for row in self.rows:
                if isinstance(self.sudoku[row][col], int):
                    counter_col.update({self.sudoku[row][col]: 1})
            for count in counter_col.values():
                if count > 1:
                    return False

        for box in self.subgrid:
            counter_box = collections.Counter()
            for index in self.subgrid[box]:
                x = index[0]
                y = index[1]
                if isinstance(self.sudoku[x][y], int):
                    counter_box.update({self.sudoku[x][y]: 1})
            for count in counter_box.values():
                if count > 1:
                    return False
        return True

    def restore_sudoku(self):
        """ Restores the sudoku grid to its pre-guess state"""
        self.sudoku = copy.deepcopy(self.sudoku_before_guess)

    def create_2d_from_string(self, unfinished_sudoku) -> list:
        """Converts String to 2d Array and puts a list of all possibilities where a tile is unsolved (0 in string)"""
        unf = []
        for i in range(len(unfinished_sudoku)):
            if i % 9 == 0:
                row = unfinished_sudoku[i:i + 9]
                lst = [int(x) if int(x) > 0 else self.all_possibilities.copy() for x in row]
                unf.append(lst)
        return unf

    # counting functions
    def count_clues_in_box(self, box) -> collections.Counter:
        """ Helper function for every function that needs to know the count of clues in a box.
        :param box: Index of Sudoku box between 1-9
        :return: Counter-Object containing counts of every clue """
        counter_box = collections.Counter()
        for index in self.subgrid[box]:
            x = index[0]
            y = index[1]
            if isinstance(self.sudoku[x][y], list):
                counter_box.update(collections.Counter(self.sudoku[x][y]))
        return counter_box

    def count_clues_in_box_row(self, box, row) -> collections.Counter:
        """ Helper function for the count of clues in a specific row of a box"""
        counter_box_row = collections.Counter()
        for index in self.subgrid[box]:
            if index[0] == row:
                y = index[1]
                if isinstance(self.sudoku[row][y], list):
                    counter_box_row.update(collections.Counter(self.sudoku[row][y]))
        return counter_box_row

    def count_clues_in_box_column(self, box, column) -> collections.Counter:
        """ Helper function for the count of clues in a specific column of a box"""
        counter_box_col = collections.Counter()
        for index in self.subgrid[box]:
            if index[1] == column:
                x = index[0]
                if isinstance(self.sudoku[x][column], list):
                    counter_box_col.update(collections.Counter(self.sudoku[x][column]))
        return counter_box_col

    def count_clues_in_row(self, row) -> collections.Counter:
        """ Helper function for every function that needs to know the count of clues in a row. """
        counter_row = collections.Counter()
        for j in range(9):
            if isinstance(self.sudoku[row][j], list):
                counter_temp = collections.Counter(self.sudoku[row][j])
                counter_row += counter_temp
        return counter_row

    def count_clues_in_column(self, column) -> collections.Counter:
        """ Helper function for every function that needs to know the count of clues in a column. """
        counter_column = collections.Counter()
        for i in range(9):
            if isinstance(self.sudoku[i][column], list):
                counter_temp = collections.Counter(self.sudoku[i][column])
                counter_column += counter_temp
        return counter_column

    def get_main_sudoku(self) -> list:
        """ Returns the current sudoku grid"""
        return self.sudoku

    def get_stack(self) -> list:
        """ Returns the current stack"""
        return self.stack

    def get_highlight(self) -> tuple:
        """ Returns the Index of the last Number that was set"""
        return self.highlight_index
