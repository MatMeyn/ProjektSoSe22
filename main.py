import time
import tkinter as tk
from tkk_sudoku import Gui

# TODO: Cleanup, Functiondeskriptors


def main():
    # test_without_GUI(sudoku)
    root = tk.Tk()
    root.configure(background='grey')
    gui = Gui(root)
    root.mainloop()


if __name__ == '__main__':
    main()

