from tomato.classes import cell

"""
Author: Eduardo Lopes Dias (codeberg.org/eduardotogpi)

This rule was originally made to test tomato's display capabilities, but it
turned out too pretty to throw out once the test was completed.
"""


class Cell(cell.CellTemplate):
    # {{{
    def __init__(self, val, pos):
        self.lin, self.col = pos
        self.value = val

    def update(self, state_matrix):
        self.value += (self.col // (self.value + 1) + 1) % 255
        self.value % -255

    @property
    def neighbors(self):
        return self.moore_neighborhood

    @staticmethod
    def display(value):
        return (value % 90, value % 125, value % 255)

    @staticmethod
    def from_display(value):
        return value[2]


# }}}
