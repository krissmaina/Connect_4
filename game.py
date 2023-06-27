import tkinter
from settings import *


class Board(tkinter.Canvas):

    def __init__(self, window, width=BOARD_WIDTH, height=BOARD_HEIGHT, **kwargs):
        super().__init__(master=window, width=width, height=height, **kwargs)

        self.width = width
        self.height = height

        self.ranks = [6, 5, 4, 3, 2, 1]
        self.files = ['a', 'b', 'c', 'd', 'e', 'f', 'g']

        self.squares = {}
        self.circles = {}

        self.player1_turn = True
        self.player1_checker = "yellow"
        self.player2_checker = "red"
        self.players = {
            True: 'yellow',
            False: 'red',
        }

        self.player1_checkers = []
        self.player2_checkers = []

        self.bind("<Button-1>", self.on_click)

    def grid(self, row, column, **kwargs):
        super().grid(row=row, column=column, **kwargs)
        self.draw_board()

    def draw_board(self):
        """
        Draws the Connect 4 board.
        The board is 6 x 7.
        """
        for y, rank in enumerate(self.ranks):
            y0 = y * SQUARE_LENGTH
            y1 = y0 + SQUARE_LENGTH

            for x, file in enumerate(self.files):
                x0 = x * SQUARE_LENGTH
                x1 = x0 + SQUARE_LENGTH
                square_id = self.create_rectangle(x0, y0, x1, y1, fill='dark blue', outline="",
                                                  tags=f'square_in_{file}{rank}')
                circle_id = self.create_oval(x0+5, y0+5, x1-5, y1-5, fill='cornflower blue',
                                             tags=f'circle_in_{file}{rank}')

                self.squares[square_id] = f"{file}{rank}"
                self.circles[circle_id] = f"{file}{rank}"

    def on_click(self, event):
        """
        In the event that the cursor is clicked, a checker will be placed in the last available row if any.
        """
        items_id = self.find_overlapping(event.x, event.y, event.x, event.y)
        square_id = None

        # get the correct id (rectangle id/ square_id)
        for item_id in items_id:
            item_type = self.type(item_id)

            if item_type == 'rectangle':
                square_id = item_id
                break

        file = self.squares[square_id][0]
        circle_name = self.check_checker_on_file(file)

        if circle_name:     # an empty circle was found
            player_color = self.players[self.player1_turn]
            self.place_checker(player_color, circle_name)

            # give the turn to the other player
            self.player1_turn = not self.player1_turn

    def check_checker_on_file(self, file: str):
        """
        Given a file (a, b, c .., g), this function checks to see if there are any checkers in that particular column.
        If there is an empty circle, the function will return the circle name of that empty circle.
        """
        column = [f"{file}{rank}" for rank in range(1, 7)]
        for circle in column:
            checker = self.find_withtag(f"checker_in_{circle}")
            if checker:
                continue
            else:
                return circle

        return None     # will be executed if the column is full

    def place_checker(self, player_color: str, circle_name: str):
        """
        Puts a player's checker in the circle_name.
        """
        # find the coordinates of the circle_name
        circle_id = self.find_withtag(f"circle_in_{circle_name}")[0]
        x0, y0, x1, y1 = self.coords(circle_id)

        # place the checker in that circle
        checker_id = self.create_oval(x0, y0, x1, y1, fill=player_color, tags=f"checker_in_{circle_name}")

        # add the checker_id to its respective player list
        if player_color == 'yellow':
            self.player1_checkers.append(checker_id)
        elif player_color == 'red':
            self.player2_checkers.append(checker_id)


if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("Connect 4 GUI")
    root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')

    board = Board(root, relief='sunken')
    board.grid(row=0, column=0, padx=20, pady=20)

    root.mainloop()
