import tkinter as tk
from tkinter import ttk
from tkinter import *
from sudokusolver import SudokuSolver
import template_sudokus as ts


# TODO: highlight top of stack?
# TODO: Buttons: Solve, Speed, Stop, Import, Import from String
# TODO: Adjust Window Size
# TODO: Adjust Fontsize
# TODO: Backtracking solve
class Gui:
    def __init__(self, root):
        self.sudoku = SudokuSolver(ts.hard_sudoku)
        self.root = root
        self.root.title("SudokuSolver")
        self.root.geometry("1200x900")

        self.stop = False
        self.time_delay = 1
        self.labels = self.initial()

        self.initialize_buttons()

        self.slider = tk.Scale(self.root,
                               from_=1,
                               to=2000,
                               label='Solve/ms',
                               orient='horizontal',
                               command=self.slider_change)
        self.slider.grid(column=200, row=4, sticky='ne')

    def initial(self):
        labels = []
        for i, block_row in enumerate(self.sudoku.get_main_sudoku()):
            row = []
            for j, block in enumerate(block_row):
                temp = block
                if isinstance(temp, list):
                    temp = self.clues_to_str(temp)
                pady = 5 if ((i + 1) % 3 == 0) else 1
                padx = 5 if ((j + 1) % 3 == 0) else 1
                block = tk.Label(self.root,
                                 text=temp,
                                 height=4,
                                 width=8,
                                 relief='solid',
                                 font='Arial 12 bold'
                                 )
                block.grid(row=i, column=j, pady=(0, pady), padx=(0, padx))
                row.append(block)
            labels.append(row)
        return labels

    def update_labels(self):
        self.sudoku.solve_next()
        for row_matrix, row_labels in zip(self.sudoku.get_main_sudoku(), self.labels):
            for cell_content, label in zip(row_matrix, row_labels):
                if isinstance(cell_content, list):
                    label.config(fg='red')
                    cell_content = self.clues_to_str(cell_content)
                if isinstance(cell_content, int):
                    label.config(fg='black')
                label["text"] = cell_content
        if self.sudoku.is_solved():
            print('solved')
        if not self.stop:
            self.root.after(self.time_delay, self.update_labels)

    def clues_to_str(self, clues_list):
        """ returns a string in form of '1 2 3\n4 5 6\n7 8 9', but replacing missing clues with space"""
        string = '\n'
        for i in range(1, 10):
            if i in clues_list:
                string += ''.join(str(i))
            else:
                string += '  '
            if i % 3 == 0:
                string += '\n'
            else:
                string += '   '
        return string

    def stop_function(self):
        self.stop = True

    def start_function(self):
        self.stop = False
        self.root.after(self.time_delay, self.update_labels)

    def slider_change(self, var):
        self.time_delay = self.slider.get()

    def initialize_buttons(self):
        solve_button = tk.Button(self.root, text="next", command=self.update_labels)
        solve_button.grid(column=200, row=1, sticky='ne')

        stop_button = tk.Button(self.root, text="Stop", command=self.stop_function)
        stop_button.grid(column=200, row=2, sticky='ne')

        start_button = tk.Button(self.root, text="Start", command=self.start_function)
        start_button.grid(column=200, row=3, sticky='ne')
