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
            True: ['yellow', 'player1'],
            False: ['red', 'player2'],
        }
        self.game_over = False

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
        # check first to see if the game is over
        if self.game_over:
            return  # if the game is over do nothing

        # the game is not over yet
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
            player_color = self.players[self.player1_turn][0]
            self.place_checker(player_color, circle_name)

            # check whether the player has checkers in connect 4
            connect4 = self.check_game_state(circle_name)
            if connect4:
                print(f"{self.players[self.player1_turn][1]} has won!")
                self.game_over = True

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

    def generate_circle_names(self, circle_name: str) -> dict:
        """
        Generates horizontal, vertical and diagonal circle names from the `circle_name`.
        There are 8 possible directions from the circle_name.

        Horizontally: East and West
        Vertically: North and South
        Diagonally:
            Main: North East and South West
            Other: North West and South East

        return: `dict` containing all the spaces in the 8 direction.
        """
        file, rank = circle_name[0], int(circle_name[1])

        n = [f"{file}{r}" for r in range(rank+1, max(self.ranks) + 1)]
        ne = [f"{chr(f)}{r}" for f, r in zip(range(ord(file)+1, ord(self.files[-1])+1), range(rank+1, self.ranks[0]+1))]
        e = [f"{chr(f)}{rank}" for f in range(ord(file)+1, ord(self.files[-1])+1)]
        se = [f"{chr(f)}{r}" for f, r in zip(range(ord(file)+1, ord(self.files[-1]) + 1), range(rank-1, 0, -1))]
        s = [f"{file}{r}" for r in range(rank-1, 0, -1)]
        sw = [f"{chr(f)}{r}" for f, r in zip(range(ord(file)-1, ord(self.files[0])-1, -1), range(rank-1, 0, -1))]
        w = [f"{chr(f)}{rank}" for f in range(ord(file)-1, ord(self.files[0])-1, -1)]
        nw = [f"{chr(f)}{r}" for f, r in zip(range(ord(file)-1, ord(self.files[0])-1, -1),
                                             range(rank+1, self.ranks[0]+1))]

        return {
            "n": n,
            "ne": ne,
            "e": e,
            "se": se,
            "s": s,
            "sw": sw,
            "w": w,
            "nw": nw,
        }

    def get_checker(self, circle_name: str) -> tuple:
        """
        Returns tuple(checker_id, checker_color) in the circle_name.

        If there exists no checker in that circle, -> ()
        """
        checker_id = self.find_withtag(f"checker_in_{circle_name}")[0]
        if checker_id:
            checker_color = self.itemconfig(checker_id)['fill']
            return checker_id, checker_color

        return ()   # if there isn't a checker, return an empty tuple

    def check_connect_4(self, circle_name: str, dir1: list, dir2: list) -> list:
        """
        Given 2 lists of direction, this function checks if there exists any checkers that are in connect 4.
        If there aren't any -> [](return an empty list)
        """
        connect_4 = [circle_name]   # currently there is one item
        count = 1

        checker_id, checker_color = self.get_checker(circle_name)

        for circle in dir1:
            # check if there is a checker
            if self.find_withtag(f"checker_in_{circle}"):
                # check the color
                _, color = self.get_checker(circle)
                if color == checker_color:
                    count += 1
                    connect_4.append(circle)
                else:
                    break
            else:
                break   # circle is empty

            if len(connect_4) == 4:
                return connect_4

        for circle in dir2:
            if self.find_withtag(f"checker_in_{circle}"):
                # check the color
                _, color = self.get_checker(circle)

                if color == checker_color:
                    count += 1
                    connect_4.append(circle)
                else:
                    break
            else:
                break   # the circle is empty

            if len(connect_4) == 4:
                return connect_4

        return []   # no checkers were found to be in connect 4

    def check_game_state(self, circle_name: str):
        """
        Checks whether a player has 4 checkers in a row either horizontally, vertically or diagonally.

        When a player places a checker on a circle(circle_name) this function checks if the player's checkers are
        in connect 4.

        return: `list` containing the connect 4 circle names if any (if not -> [])
        """
        circle_names = self.generate_circle_names(circle_name)

        vertical_directions = [circle_names['n'], circle_names['s']]
        horizontal_directions = [circle_names['e'], circle_names['w']]
        main_diagonal = [circle_names['ne'], circle_names['sw']]
        other_diagonal = [circle_names['nw'], circle_names['se']]

        directions = [vertical_directions, horizontal_directions, main_diagonal, other_diagonal]

        for direction in directions:
            dir1, dir2 = direction
            connect4 = self.check_connect_4(circle_name, dir1, dir2)

            if connect4:
                return connect4

        return []   # no checkers are in connect 4


if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("Connect 4 GUI")
    root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')

    board = Board(root, relief='sunken')
    board.grid(row=0, column=0, padx=20, pady=20)

    root.mainloop()