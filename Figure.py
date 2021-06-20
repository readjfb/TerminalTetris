#!/usr/bin/env python3

class Figure:
    def __init__(self, shape, position=(0, 0)):
        self.FIGURE = shape

        self.COLOR = None

        for i in shape[0]:
            if i != 0:
                self.COLOR = i
                break

        self.position = position

    def print_self(self):
        for row in self.FIGURE:
            for col in row:
                print(col, end="")
            print()

    def get_cw_rotation(self):
        new_figure = [[None for j in range(len(self.FIGURE))]
                      for k in range(len(self.FIGURE[0]))]

        for column in range(len(self.FIGURE[0])):
            for row in range(len(self.FIGURE)):
                new_figure[column][row] = self.FIGURE[row][column]

        return [i[::-1] for i in new_figure]

    def get_ccw_rotation(self):
        new_figure = [[None for j in range(len(self.FIGURE))]
                      for k in range(len(self.FIGURE[0]))]

        for column in range(len(self.FIGURE[0])):
            for row in range(len(self.FIGURE)):
                new_figure[column][row] = self.FIGURE[row][column]

        return new_figure[::-1]

    def rotate_cw(self):
        self.FIGURE = self.get_cw_rotation()

    def rotate_ccw(self):
        self.FIGURE = self.get_ccw_rotation()

    def move_left(self):
        self.position = (self.position[0] - 1, self.position[1])

    def move_right(self):
        self.position = (self.position[0] + 1, self.position[1])

    def move_down(self):
        self.position = (self.position[0], self.position[1] + 1)


if __name__ == "__main__":
    a_shape = [[1, 1, 1, 1], [0, 1, 1, 0]]
    a = Figure(a_shape)
    a.print_self()

    a.rotate_cw()
    a.print_self()
