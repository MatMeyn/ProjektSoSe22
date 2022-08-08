import tkinter as tk
from tkinter import ttk
import time
import sudokusolver


class MainApplication(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.parent.title('SudokuSolver')
        self.parent.geometry('550x470')
        self.parent.attributes('-toolwindow', True)
        self.testtext = 'test'
        ttk.Label(parent, text=self.testtext).pack(anchor='e', padx=10, ipady=25)
        self.after(20, self.task)

    def task(self):
        for i in range(1000):
            self.testtext = 'a' + str(i)
        self.after(20, self.task)

def main():
    input_from_tkinter = []
    sudoku = sudokusolver.SudokuSolver(input_from_tkinter)
    root = tk.Tk()
    MainApplication(root)
    root.mainloop()


if __name__ == '__main__':
    main()


def leftovers():
    class Entrygrid:
        def __init__(self, parent):
            # Sudoku

            self.entries = []
            for a in range(9):
                for b in range(9):
                    self.temp = ttk.Entry(parent, width=5, justify='center')
                    self.temp.place(x=50 * a, y=50 * b, height=50, width=50)
                    self.entries.append(self.temp.get())

        def get_entries(self):
            return self.entries

    class Buttons(tk.Frame):
        def __init__(self, parent):
            # Buttons
            ttk.Button(parent, text='Solve').pack(anchor='e', padx=10, ipady=25)
            ttk.Button(parent, text='Stop').pack(anchor='e', padx=10, ipady=25)
            ttk.Button(parent, text='Reset', command=self.get_entrylist).pack(anchor='e', padx=10, ipady=25)
            ttk.Label(parent, text='Speed').pack(anchor='e', padx=28, ipady=25)
            ttk.Scale(parent).pack(anchor='e')

        def get_entrylist(self):
            pass

    class MainApplication(tk.Frame):
        def __init__(self, parent):
            tk.Frame.__init__(self, parent)
            self.parent = parent
            self.parent.title('SudokuSolver')
            self.parent.geometry('550x470')
            self.parent.attributes('-toolwindow', True)

            self.entrygrid = Entrygrid(parent)
            self.buttons = Buttons(parent)
            print(self.entrygrid.get_entries())


