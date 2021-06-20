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

# LEFT = (-1, 0)
# RIGHT = (1, 0)
# UP = (0, -1)
# DOWN = (0, 1)

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

LEVEL_TIMES = {0: .5, 1: .3, 2: .25, 3: .2, 4: .15, 5: .1}

LINE_SCORES = {0: 0, 1: 40, 2: 100, 3: 300, 4: 1200}


class TetrisGame:
    def __init__(self, width, height):
        self.WIDTH = width
        self.HEIGHT = height

        self.empty = 0

        self.active_piece = None

        # 0,0 is defined as the top left
        self.board = [[self.empty for x in range(self.WIDTH)]
                      for y in range(self.HEIGHT)]

        self.cleared_lines = 0
        self.score = 0

    def print_board(self):
        # For debugging purposes; prints the board simply
        for row in self.board:
            for col in row:
                print(col, end="")
            print()

    def spawn_new_piece(self):
        del self.active_piece

        self.active_piece = Figure(random.choice(PIECE_TYPES),
                                   (self.WIDTH // 2 - 1, 0))

    def get_block_positions(self, fig):
        # converts to cooridinates from a figure layout
        block_positions = []

        for y, row in enumerate(fig):
            for x, col in enumerate(row):
                if col != 0:
                    block_positions.append((x + self.active_piece.position[0],
                                            y + self.active_piece.position[1]))

        return block_positions

    def verify_legal_move(self, direction):
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
        return any([i != 0 for i in self.board[0]])

    def check_clear_lines(self):
        num_lines = 0

        i = self.HEIGHT - 1

        while i >= 0:
            if not (0 in self.board[i]):
                self.board[i] = [0 for i in range(self.WIDTH)]
                num_lines += 1

                for j in range(i - 1, -1, -1):
                    self.board[j + 1] = self.board[j]
                self.board[0] = [0 for i in range(self.WIDTH)]
            else:
                i -= 1
        self.cleared_lines += num_lines

        self.score += LINE_SCORES[num_lines] * ((self.cleared_lines // 10) + 1)

    def move_block_down(self):
        if not self.verify_legal_move("DOWN"):
            # place the block on the grid
            for block in self.get_block_positions(self.active_piece.FIGURE):
                self.board[block[1]][block[0]] = self.active_piece.COLOR

            self.check_clear_lines()

            self.spawn_new_piece()
            return

        self.active_piece.move_down()


def render_scene(game, term):
    converted_board = [[COLOR_DICT[color] for color in row]
                       for row in game.board]

    col = COLOR_DICT[game.active_piece.COLOR]

    for block in game.get_block_positions(game.active_piece.FIGURE):
        converted_board[block[1]][block[0]] = col

    converted_board = ["".join(row) for row in converted_board]

    print(term.home + term.clear + term.move_yx(0, 0), end="")
    print("⬜️" * (game.WIDTH + 2), end="", flush=False)

    for y in range(game.HEIGHT):
        print(term.move_yx(1 + y, 0), end="")
        print("⬜️" + converted_board[y] + "⬜️", end="")

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
    print(term.move_yx(10, (2 * game.WIDTH) + 10) + "L/ R arrow keys strafe" +
          term.move_yx(11, (2 * game.WIDTH) + 10) + "Up arrow rotates" +
          term.move_yx(12, (2 * game.WIDTH) + 10) + "Q quits" +
          term.move_yx(13, (2 * game.WIDTH) + 10) + "P pauses",
          term.move_yx(14, (2 * game.WIDTH) + 10) + "Return drops block",
          end="")

    print(end="", flush=True)


def pause_handler(term):
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

            if level in LEVEL_TIMES.keys():
                time_delta = LEVEL_TIMES[level]

            if update_flag:
                render_scene(main_game, term)

                update_flag = False

            if main_game.check_game_end():
                end_flag = True
                break

            inp = term.inkey(timeout=0)

            if inp.is_sequence:
                inp = inp.name

                if inp == "KEY_UP":
                    if main_game.verify_legal_rotation("CW"):
                        main_game.active_piece.rotate_cw()
                        update_flag = True

                elif inp == "KEY_LEFT":
                    if main_game.verify_legal_move("LEFT"):
                        main_game.active_piece.move_left()
                        update_flag = True

                elif inp == "KEY_RIGHT":
                    if main_game.verify_legal_move("RIGHT"):
                        main_game.active_piece.move_right()
                        update_flag = True

                elif inp == "KEY_DOWN":
                    main_game.move_block_down()
                    prev_time = time.time()
                    update_flag = True

                elif inp == "KEY_ENTER":
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
        # main_game.print_board()
    print(f"Score: {term.bold(str(main_game.score))}")
    print(f"Lines Cleared: {term.bold(str(main_game.cleared_lines))}")


if __name__ == '__main__':
    main()
