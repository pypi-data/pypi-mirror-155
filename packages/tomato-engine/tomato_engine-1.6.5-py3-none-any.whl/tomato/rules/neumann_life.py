from tomato.classes import cell

"""
Author: Eduardo Lopes Dias (codeberg.org/eduardotogpi)

This is an approximation of Conway's Game of Life using von Neumann
neighborhoods. It's here just to remind everyone that this kind of
neighborhood is available, and also because it forms some pretty
cool and unpredictable "boxy" patterns.
"""


class Cell(cell.CellTemplate):
    # {{{
    # É o high life só que com vizinhança de Neumann.

    def update(self, state_matrix):
        self.state_matrix = state_matrix

        # Dead cell
        if self.value == 0:
            if self.live_neighbors == 2:
                self.value = 1
            else:
                self.value = 0
        # Live cell
        else:
            if self.live_neighbors in (2, 3):
                self.value = 1
            else:
                self.value = 0

    @property
    def neighbors(self):
        return self.neumann_neighborhood

    @property
    def live_neighbors(self):
        return sum(self.neighbors)


# }}}
