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
        self.button.grid(sticky='sw')
        self.root.bind('<Button-1>', self.update_labels())

    def initial(self):
        labels = []
        for i, block_row in enumerate(self.sudoku.get_main_sudoku()):
            row = []
            for j, block in enumerate(block_row):
                temp = block
                if isinstance(temp, list):
                    temp = ','.join([str(elem) for elem in temp])
                block = tk.Label(self.root, text=f'{temp}', height=5, width=5, borderwidth=1, relief='solid')
                block.grid(row=i, column=j)
                row.append(block)
            labels.append(row)
        return labels

    def update_labels(self):
        self.sudoku.solve_next()
        for row_matrix, row_labels in zip(self.sudoku.get_main_sudoku(), self.labels):
            for cell_content, label in zip(row_matrix, row_labels):
                if isinstance(cell_content, int):
                    label.config(font=15, fg='black')
                if isinstance(cell_content, list):
                    label.config(fg='red')
                    cell_content = '-'.join([str(elem) for elem in cell_content])
                    print(cell_content)
                label["text"] = cell_content
