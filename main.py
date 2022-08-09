import random
import time
from sudokusolver import SudokuSolver
import template_sudokus as ts


def main():
    start = time.perf_counter()
    abc = SudokuSolver(ts.hard_sudoku)
    for count in range(300):
        abc.solve_next()
        abc.print_sudoku()
        abc.get_stack()
        abc.get_main_sudoku()
        print(f'Iterations: {count}')
        if abc.is_solved():
            break
    end = time.perf_counter()
    print(f"Total Time used is {end - start:0.2f}s")
    #input_from_tkinter = []
    #sudoku = sudokusolver.SudokuSolver(input_from_tkinter)


if __name__ == '__main__':
    main()



