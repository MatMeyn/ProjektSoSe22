import PySimpleGUI as sg
import random
import time
import sudokusolver


def main():
    window = sg.Window('SudokuSolver',
                       [[sg.Frame('',
                                  [[sg.I(random.randint(1, 9),
                                    justification='r',
                                    size=(3, 1),
                                    enable_events=True,
                                    key=(fr * 3 + r, fc * 3 + c)) for c in range(3)] for r in range(3)]) for fc in range(3)] for fr in range(3)] +
                       [[sg.B('Solve'),
                         sg.B('Check'),
                         sg.B('Hint'),
                         sg.B('New Game'),
                         sg.T('Mask rate (0-1)'),
                         sg.In(str(0.7),
                               size=(3, 1),
                               key='-RATE-')], ],
                       finalize=True)
    while True:  # The Event Loop
        event, values = window.read()
        if event == 'Check':
            sg.Window('test',list(),None,)
        if event == sg.WIN_CLOSED:
            break
    #input_from_tkinter = []
    #sudoku = sudokusolver.SudokuSolver(input_from_tkinter)


if __name__ == '__main__':
    main()



