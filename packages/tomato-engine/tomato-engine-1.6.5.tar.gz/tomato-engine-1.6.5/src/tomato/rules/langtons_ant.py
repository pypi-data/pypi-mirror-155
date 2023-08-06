from tomato.classes import cell

"""
Author: Murilo Melhem (codeberg.org/Muril-o)
Improved by Eduardo Lopes Dias (codeberg.org/eduardotogpi)

An implementation of another classic automaton, Langton's Ant.
This implementation is not as clean as the others, because tomato-engine
wasn't really designed around single automata that move along vast,
empty boards. But this rule shows that even such automata are possible.
"""


class Cell(cell.CellTemplate):
    # {{{
    def __init__(self, val, pos, cell_args):

        global ant_pos
        global ant_dir

        self.value = val
        self.lin, self.col = pos

        ant_pos = cell_args["pos"]
        ant_dir = cell_args["dir"]

    def update(self, state_matrix):

        global ant_pos
        global ant_dir

        if ant_pos == self.pos:
            if self.value == 0:
                self.value = 1
                ant_dir = (
                    -ant_dir[1],
                    ant_dir[0],
                )
            elif self.value == 1:
                self.value = 0
                ant_dir = (
                    ant_dir[1],
                    -ant_dir[0],
                )

            # Wrap around the board when close to its edge
            m, n = state_matrix.shape
            ant_pos = (
                (ant_dir[0] + ant_pos[0]) % m,
                (ant_dir[1] + ant_pos[1]) % n,
            )


# }}}
