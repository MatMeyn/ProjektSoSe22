import tkinter as tk
from tkinter import ttk
from sudoku import solve


class Sudoku():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('SudokuSolver')
        self.root.geometry('800x500')
        self.root.attributes('-toolwindow', True)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        #Sudoku
        self.entries = []
        for a in range(9):
            for b in range(9):
                temp = ttk.Entry(self.root, width=5, justify='center')
                temp.place(x=50*a, y=50*b, height=50, width=50)
                self.entries.append(temp.get())

        #Buttons
        ttk.Button(self.root, text='Solve').grid(column=1, row=1)
        ttk.Button(self.root, text='Stop').grid(column=1, row=1)
        ttk.Button(self.root, text='Reset').grid(column=1, row=2)
        ttk.Label(self.root, text='Speed').grid(column=1, row=3)
        ttk.Scale(self.root).grid(column=1, row=4)

        self.root.mainloop()


def main():
    Sudoku()
    #solve()


if __name__ == '__main__':
    main()
