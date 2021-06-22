#!/usr/bin/env python3
import random
import time

from blessed import Terminal
from Figure import Figure

PIECE_TYPES = []

line_piece = [[1, 1, 1, 1]]
PIECE_TYPES.append(line_piece)

square_piece = [[2, 2], [2, 2]]
PIECE_TYPES.append(square_piece)

j_piece = [[3, 0, 0], [3, 3, 3]]
PIECE_TYPES.append(j_piece)

l_piece = [[0, 0, 4], [4, 4, 4]]
PIECE_TYPES.append(l_piece)

t_piece = [[0, 5, 0], [5, 5, 5]]
PIECE_TYPES.append(t_piece)

s_piece = [[0, 6, 6], [6, 6, 0]]
PIECE_TYPES.append(s_piece)

z_piece = [[7, 7, 0], [0, 7, 7]]
PIECE_TYPES.append(z_piece)

COLOR_DICT = {
    0: "  ",
    1: "🟥",
    2: "🟫",
    3: "🟦",
    4: "🟪",
    5: "🟨",
    6: "🟩",
    7: "🟧",
    8: "⬜"
}

LEVEL_TIMES = {0: .5, 1: .35, 2: .25, 3: .2, 4: .175, 5: .15}

LINE_SCORES = {0: 0, 1: 40, 2: 100, 3: 300, 4: 1200}


class TetrisGame:
    def __init__(self, width, height):
        """
        Stores a TetrisGame object with a board width x height

        Contains most needed functions for playing the tetris game,
        with the exception of the logic for determing when to do certain
        events
        """

        self.WIDTH = width
        self.HEIGHT = height

        self.active_piece = None

        # 0,0 is defined as the top left
        self.board = [[0 for x in range(self.WIDTH)]
                      for y in range(self.HEIGHT)]

        self.cleared_lines = 0
        self.score = 0

    def print_board(self):
        """
        For debugging purposes; prints the raw board in a basic manner
        """
        for row in self.board:
            for col in row:
                print(col, end="")
            print()

    def spawn_new_piece(self):
        """
        Deletes the current piece, and creates a new one in it's place.
        Note- Does not do the saving of the current block
        """

        del self.active_piece

        self.active_piece = Figure(random.choice(PIECE_TYPES),
                                   (self.WIDTH // 2 - 1, 0))

    def get_block_positions(self, fig):
        """
        Converts to cooridinates from a figure layout, as can be given by
        the figure class
        """

        block_positions = []

        for y, row in enumerate(fig):
            for x, col in enumerate(row):
                if col != 0:
                    block_positions.append((x + self.active_piece.position[0],
                                            y + self.active_piece.position[1]))

        return block_positions

    def verify_legal_move(self, direction):
        """
        Refrences the state of the current board and the current falling block
        to determine if the falling block can move left, right, or down
        without colliding with a wall or other block
        """
        for block in self.get_block_positions(self.active_piece.FIGURE):

            position = block

            if direction == "LEFT":
                position = (position[0] - 1, position[1])
            elif direction == "RIGHT":
                position = (position[0] + 1, position[1])
            elif direction == "DOWN":
                position = (position[0], position[1] + 1)
            # else:
            #     raise ValueError

            if position[0] < 0 or position[0] >= self.WIDTH:
                return False

            if position[1] < 0 or position[1] >= self.HEIGHT:
                return False

            if self.board[position[1]][position[0]] != 0:
                return False
        return True

    def verify_legal_rotation(self, direction):
        """
        Refrences the state of the current board and the current falling block
        to determine if the falling block can rotate clockwise or
        counterclockwise (specified by direction = CW or CCW)without colliding
        with a wall or other block
        """
        test_figure = None
        if direction == "CW":
            test_figure = self.get_block_positions(
                self.active_piece.get_cw_rotation())
        elif direction == "CCW":
            test_figure = self.get_block_positions(
                self.active_piece.get_ccw_rotation())

        for block in test_figure:
            if block[0] < 0 or block[0] >= self.WIDTH:
                return False

            if block[1] < 0 or block[1] >= self.HEIGHT:
                return False

            if self.board[block[1]][block[0]] != 0:
                return False
        return True

    def check_game_end(self):
        """
        Returns if the game should be over, defined as a block being present
        in the topmost row of the board
        """

        return any([i != 0 for i in self.board[0]])

    def check_clear_lines(self):
        """
        Looks for full lines. If it finds one, it counts it,
        clears it, and makes all of the lines above 'fall' down.
        This repeats for any number of full lines

        This function also increments the score according to the scoring rules
        """
        num_lines = 0

        i = self.HEIGHT - 1

        level = ((self.cleared_lines // 10) + 1)

        while i >= 0:
            if 0 not in self.board[i]:
                self.board[i] = [0 for i in range(self.WIDTH)]
                num_lines += 1

                for j in range(i - 1, -1, -1):
                    self.board[j + 1] = self.board[j]
                self.board[0] = [0 for i in range(self.WIDTH)]
            else:
                i -= 1

        self.cleared_lines += num_lines

        self.score += LINE_SCORES[num_lines] * level

    def move_block_down(self):
        """
        Moves the currently falling block down- Handles the logic for
        detecting if the falling block can move down without impedance, or if
        it should be placed onto the static board, and a new block spawned
        """
        if not self.verify_legal_move("DOWN"):
            # If it can't move down, place the block on the grid
            for block in self.get_block_positions(self.active_piece.FIGURE):
                self.board[block[1]][block[0]] = self.active_piece.COLOR

            self.check_clear_lines()

            self.spawn_new_piece()
            return

        self.active_piece.move_down()


def render_scene(game, term):
    """
    Uses the game object and terminal object to render the scene using the
    Blessings library

    It first prints the board, then prints the scores and other useful words
    such as the help section
    """
    converted_board = [[COLOR_DICT[color] for color in row]
                       for row in game.board]

    col = COLOR_DICT[game.active_piece.COLOR]

    for block in game.get_block_positions(game.active_piece.FIGURE):
        converted_board[block[1]][block[0]] = col

    converted_board = ["".join(row) for row in converted_board]

    print(term.home + term.clear + term.move_yx(0, 0), end="")
    print("⬜️" * (game.WIDTH + 2), end="")

    for y in range(game.HEIGHT):
        print(term.move_yx(1 + y, 0) + "⬜️" + converted_board[y] + "⬜️",
              end="")

    print(term.move_yx(game.HEIGHT + 1, 0) + "⬜️" * (game.WIDTH + 2), end="")

    # Print the game name and scores
    print(term.move_yx(3, (2 * game.WIDTH) + 10) +
          term.underline_bold("Terminal Tetris") +
          term.move_yx(4, (2 * game.WIDTH) + 10) +
          f"By {term.link('https://github.com/readjfb', 'J. Bremen')}" +
          term.move_yx(5, (2 * game.WIDTH) + 10) +
          f"Lines Cleared: {game.cleared_lines}" +
          term.move_yx(6, (2 * game.WIDTH) + 10) + f"Score: {game.score}",
          end="")

    # Print the controls section
    print(term.move_yx(10, (2 * game.WIDTH) + 10) + "Left:   ←" +
          term.move_yx(11, (2 * game.WIDTH) + 10) + "Right:  →" +
          term.move_yx(12, (2 * game.WIDTH) + 10) + "Down:   ↓" +
          term.move_yx(13, (2 * game.WIDTH) + 10) + "Rotate: ↑" +
          term.move_yx(14, (2 * game.WIDTH) + 10) + "Drop:   space/ return" +
          term.move_yx(15, (2 * game.WIDTH) + 10) + "Pause:  p",
          term.move_yx(16, (2 * game.WIDTH) + 10) + "Quit:   q",
          end="")

    print(end="", flush=True)


def pause_handler(term):
    """
    This function is used as a pause; it waits for the user to input either p
    or q, while displaying the relevant dialog on screen
    """
    print(term.home + term.clear + term.move_y(term.height // 2))
    print(term.black_on_white(term.center('press P to continue.')))

    inp = None
    while inp not in (u'p', u'P'):
        inp = term.inkey()

        if inp in (u'q', u'Q'):
            return


def main():
    """program entry point"""
    term = Terminal()

    main_game = TetrisGame(11, 25)

    main_game.spawn_new_piece()

    prev_time = time.time()

    time_delta = .5

    inp = None

    update_flag = True

    end_flag = False

    with term.hidden_cursor(), term.cbreak(), term.fullscreen():
        while inp not in (u'q', u'Q'):
            if inp in (u'p', u'P'):
                pause_handler(term)
                inp = None
                prev_time = time.time()
                update_flag = True
                continue

            level = main_game.cleared_lines // 10

            if main_game.check_game_end():
                end_flag = True
                break

            # Rendering first makes it smoother for some reason
            if update_flag:
                # Update the time before piece is moved down
                if level in LEVEL_TIMES.keys():
                    time_delta = LEVEL_TIMES[level]

                render_scene(main_game, term)
                update_flag = False

            inp = term.inkey(timeout=0)

            inp_name = inp.name

            if inp_name == "KEY_UP":
                if main_game.verify_legal_rotation("CW"):
                    main_game.active_piece.rotate_cw()
                    prev_time += 0.07
                    update_flag = True

            elif inp_name == "KEY_LEFT":
                if main_game.verify_legal_move("LEFT"):
                    main_game.active_piece.move_left()
                    prev_time += 0.07
                    update_flag = True

            elif inp_name == "KEY_RIGHT":
                if main_game.verify_legal_move("RIGHT"):
                    main_game.active_piece.move_right()
                    prev_time += 0.07
                    update_flag = True

            elif inp_name == "KEY_DOWN":
                main_game.move_block_down()
                prev_time = time.time()
                update_flag = True

            elif inp_name in ("KEY_ENTER", ) or inp in (" ", ):
                current_block = main_game.active_piece

                while current_block == main_game.active_piece:
                    main_game.move_block_down()

                prev_time = time.time()
                update_flag = True

            if time.time() >= prev_time + time_delta:
                main_game.move_block_down()
                prev_time = time.time()
                update_flag = True

    if end_flag:
        print("Game over")

    print(f"Score: {term.bold(str(main_game.score))}")
    print(f"Lines Cleared: {term.bold(str(main_game.cleared_lines))}")


if __name__ == '__main__':
    main()
