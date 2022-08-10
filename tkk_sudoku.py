import tkinter as tk
from tkinter import *
from sudokusolver import SudokuSolver
import template_sudokus as ts

class Gui:
    def __init__(self, root):
        self.root = root

        #self.canvas = tk.Canvas(self.root, width=900, height=900, background='grey')
        #self.canvas.grid(row=0, column=0)

        #self.buttons = tk.Frame(self.root, width=100, height=900, background='green')
        #self.buttons.grid(row=0, column=1)

        # Buttons
        #Button(self.buttons, command=self.test, text="Solve", height=2, width=10).grid(row=0, column=0, sticky=N)
        #Button(self.buttons, command=self.test, text="Stop", height=2, width=10).grid(row=1, column=0, sticky=N)


    def test(self):
        print("Pressed a Button")

