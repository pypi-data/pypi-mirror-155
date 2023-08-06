from tomato.classes import cell

"""
Author: Eduardo Lopes Dias (codeberg.org/eduardotogpi)

An implementation of Conways' classic Game of Life. Besides being cool to
look at, it serves as a simple example as to how new rulesets can be
implemented.
"""


class Cell(cell.CellTemplate):
    # {{{
    def update(self, state_matrix):
        self.state_matrix = state_matrix

        # Dead cell:
        if self.value == 0:
            if self.live_neighbors == 3:
                self.value = 1
            else:
                self.value = 0
        # Live cell:
        else:
            if self.live_neighbors in (2, 3):
                self.value = 1
            else:
                self.value = 0

    @property
    def neighbors(self):
        return self.moore_neighborhood

    @property
    def live_neighbors(self):
        return sum(self.neighbors)


# }}}
