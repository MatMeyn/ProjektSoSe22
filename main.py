import time
from sudokusolver import SudokuSolver
import template_sudokus as ts
import tkinter as tk
from tkk_sudoku import Gui


def main():
    pass

def update_labels():
    sudoku.solve_next()
    for row_matrix, row_labels in zip(sudoku.get_main_sudoku(), labels):
        for item, label in zip(row_matrix, row_labels):
            label["text"] = item


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
    sudoku = SudokuSolver(ts.test_sudoku)

    #test_without_GUI(sudoku)
    root = tk.Tk()
    root.title("SudokuSolver")
    root.geometry("1500x300")

    labels = []
    for i, block_row in enumerate(sudoku.get_main_sudoku()):
        row = []
        for j, block in enumerate(block_row):
            block = tk.Label(root, text=f'{block}')
            block.grid(row=i, column=j)
            row.append(block)
        labels.append(row)

    button = tk.Button(root, text="next", command=update_labels)
    button.grid(sticky='sw')
    #gui = Gui(root)
    root.bind('<Button-1>', update_labels())
    root.mainloop()

    #main()



