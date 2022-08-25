""" Author: Matthias Meyn
    Project for Skriptsprachen SS2022 """

import tkinter as tk
from tkinter import ttk
from sudokusolver import SudokuSolver
from template_sudokus import template_names_list, templates_dict


class Gui:
    def __init__(self, root):
        self.root = root
        self.root.title('SudokuSolver')
        self.root.geometry('1000x800')

        self.sudoku = None
        self.stop = True
        self.time_delay = 1
        self.labels = self.initial()

        self.combo_var = tk.StringVar()
        self.combo_box = ttk.Combobox(self.root, values=template_names_list, textvariable=self.combo_var)
        self.combo_box.grid(column=10, row=0)

        self.import_button = tk.Button(self.root, text='Import', command=self.import_sudoku,
                                       height=1, width=10)
        self.import_button.grid(column=10, row=0, sticky='s')

        self.start_button = tk.Button(self.root, text='Start', command=self.start_method, state='disabled',
                                      height=1, width=10)
        self.start_button.grid(column=10, row=1)

        self.stop_button = tk.Button(self.root, text='Stop', command=self.stop_method, state='disabled',
                                     height=1, width=10)
        self.stop_button.grid(column=10, row=1, sticky='s')

        self.slider = tk.Scale(self.root,
                               from_=1,
                               to=1000,
                               label='Solve/ms',
                               orient='horizontal',
                               command=self.slider_change)
        self.slider.grid(column=10, row=2)

        self.solved_label = tk.Label(self.root, text='Solved',
                                     font='Arial 16 bold', fg='green', bg='grey')

    def initial(self) -> list:
        """ Creates the initial grid by constructing a label for every tile of the puzzle"""
        labels = []
        for i in range(9):
            row = []
            for j in range(9):
                pady = 5 if ((i + 1) % 3 == 0) else 1  # Thicker pad between boxes
                padx = 5 if ((j + 1) % 3 == 0) else 1
                block = tk.Label(self.root,
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
        """ This function updates the grid to its current content.
            Changes text color of a tile based on its solving status
            and changes the background of failed tiles to red.
            Stops the solver if the stop button is used or the puzzle is solved"""
        for row_matrix, row_labels in zip(self.sudoku.get_main_sudoku(), self.labels):
            for tile_content, label in zip(row_matrix, row_labels):
                if isinstance(tile_content, list):       # unsolved tile
                    label.config(fg='red', bg='white')
                    if len(tile_content) == 0:           # failed tile
                        label.config(bg='red')
                    tile_content = self.clues_to_str(tile_content)
                if isinstance(tile_content, int):        # solved tile
                    label.config(fg='black', bg='white')
                label["text"] = tile_content
        if self.sudoku.is_complete():                   # stop and display 'solved'
            if self.sudoku.is_solved():
                self.stop_method()
                self.solved_label.grid(column=10, row=3)
        if not self.stop:                               # loop until solved or otherwise stopped
            self.sudoku.solve_next()
            self.root.after(self.time_delay, self.update_labels)

    def import_sudoku(self):
        """Function used by the import button. Loads the puzzle into the sudoku solver and activates the start button"""
        self.sudoku = SudokuSolver(templates_dict[self.combo_var.get()])
        self.update_labels()
        self.start_button['state'] = 'active'
        self.solved_label.grid_remove()

    def stop_method(self):
        """Function used by the stop button. Stops the solving process."""
        self.stop = True
        self.start_button['state'] = 'active'
        self.stop_button['state'] = 'disabled'

    def start_method(self):
        """Function used by the start button. Starts the solving process."""
        self.stop = False
        self.stop_button['state'] = 'active'
        self.start_button['state'] = 'disabled'
        self.root.after(self.time_delay, self.update_labels)

    def slider_change(self, var):
        """Function used by the slider. Updates the time delay between solving steps"""
        self.time_delay = self.slider.get()

    def clues_to_str(self, clues_list) -> str:
        """Returns a string in form of '1 2 3\n4 5 6\n7 8 9', but replacing missing numbers with space"""
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
