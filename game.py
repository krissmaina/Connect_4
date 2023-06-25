import tkinter
from settings import *


class Board(tkinter.Canvas):

    def __init__(self, window, width=BOARD_WIDTH, height=BOARD_HEIGHT, **kwargs):
        super().__init__(master=window, width=width, height=height, **kwargs)

        self.width = width
        self.height = height

    def grid(self, row, column, **kwargs):
        super().grid(row=row, column=column, **kwargs)

    def draw_board(self):
        """Draws the Connect 4 board"""
        pass
