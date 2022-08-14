import time
import tkinter as tk
from tkk_sudoku import Gui


def main():
    # test_without_GUI(sudoku)
    root = tk.Tk()
    gui = Gui(root)
    root.mainloop()


def test_without_GUI(sudoku):
    start = time.perf_counter()
    count = 0
    while True:
        count += 1
        sudoku.solve_next()
        sudoku.print_sudoku()
        print(f'Iterations: {count}')
        if sudoku.is_solved():
            break
    end = time.perf_counter()
    print(f"Total Time used is {end - start:0.2f}s")


if __name__ == '__main__':
    main()

