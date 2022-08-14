import tkinter as tk
from tkinter import *
from sudokusolver import SudokuSolver
import template_sudokus as ts

class Gui:
    def __init__(self, root):
        self.sudoku = SudokuSolver(ts.test_sudoku)
        self.root = root
        self.root.title("SudokuSolver")
        self.root.geometry("1200x900")

        self.labels = self.initial()

        self.button = tk.Button(self.root, text="next", command=self.update_labels)
        self.button.grid(column=200, row=1, sticky='ne')
        self.root.bind('<Button-1>', self.update_labels())


    def initial(self):
        labels = []
        for i, block_row in enumerate(self.sudoku.get_main_sudoku()):
            row = []
            for j, block in enumerate(block_row):
                temp = block
                if isinstance(temp, list):
                    temp = self.clues_to_str(temp)
                block = tk.Label(self.root,
                                 text=f'{temp}',
                                 height=4,
                                 width=8,
                                 relief='solid')
                block.grid(row=i, column=j)
                row.append(block)
            labels.append(row)
        return labels

    def update_labels(self):
        self.sudoku.solve_next()
        for row_matrix, row_labels in zip(self.sudoku.get_main_sudoku(), self.labels):
            for cell_content, label in zip(row_matrix, row_labels):
                if isinstance(cell_content, int):
                    label.config(font='Arial 12 bold',
                                 fg='black')
                if isinstance(cell_content, list):
                    label.config(font='Arial 10',
                                 fg='red')
                    cell_content = self.clues_to_str(cell_content)
                label["text"] = cell_content

    def clues_to_str(self, clues_list):
        """ returns a string in form of '1 2 3\n4 5 6\n7 8 9', but replacing missing clues with space"""
        string = ''
        for i in range(9):
            if i in clues_list:
                string += ''.join(str(i))
            else:
                string += ' '
            if i % 3 == 0:
                string += '\n'
            else:
                string += ' '
        return string + '\n'
