""" Author: Matthias Meyn
    Project for Skriptsprachen SS2022 """

import tkinter as tk
from sudoku_gui import Gui


def main():
    root = tk.Tk()
    root.configure(background='grey')
    gui = Gui(root)
    root.mainloop()


if __name__ == '__main__':
    main()

