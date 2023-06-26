import tkinter
from settings import *


class Board(tkinter.Canvas):

    def __init__(self, window, width=BOARD_WIDTH, height=BOARD_HEIGHT, **kwargs):
        super().__init__(master=window, width=width, height=height, **kwargs)

        self.width = width
        self.height = height

        self.ranks = [6, 5, 4, 3, 2, 1]
        self.files = ['a', 'b', 'c', 'd', 'e', 'f', 'g']

        self.circles = {}

    def grid(self, row, column, **kwargs):
        super().grid(row=row, column=column, **kwargs)
        self.draw_board()

    def draw_board(self):
        """
        Draws the Connect 4 board.
        The board is 6 x 7.
        """
        for y, rank in enumerate(self.ranks):
            y0 = y * 80
            y1 = y0 + 80

            for x, file in enumerate(self.files):
                x0 = x * 80
                x1 = x0 + 80
                self.create_rectangle(x0, y0, x1, y1, fill='dark blue', outline="")
                circle_id = self.create_oval(x0+10, y0+10, x1-10, y1-10, fill='cornflower blue')

                self.circles[circle_id] = f"{file}{rank}"


if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("Connect 4 GUI")
    root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')

    board = Board(root, relief='sunken')
    board.grid(row=0, column=0, padx=20, pady=20)

    root.mainloop()
