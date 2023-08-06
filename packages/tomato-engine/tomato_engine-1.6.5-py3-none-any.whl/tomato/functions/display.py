import numpy as np
import pygame

"""
Funções relacionadas a mostrar e atualizar a janelinha de
observação dos autômatos.
"""


def create_screen(cells, cell_size, title):
    # {{{
    cells_y, cells_x = cells

    screen = pygame.display.set_mode((cells_x * cell_size, cells_y * cell_size))
    pygame.display.set_caption(title)

    return screen


# }}}


def draw_screen(screen, display_matrix, size):
    # {{{

    # pygame usa x,y para indexar pixels. resto do tomate usa lin, col
    display_matrix = np.swapaxes(display_matrix, 0, 1)

    x, y = (size * display_matrix.shape[0], size * display_matrix.shape[1])

    surface = pygame.surfarray.make_surface(display_matrix)
    surface = pygame.transform.scale(surface, (x, y))
    screen.blit(surface, (0, 0))
    array_from_display = pygame.surfarray.pixels3d(surface)


# }}}
