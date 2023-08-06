import numpy as np
from multiprocessing import Pool
from functools import partial

"""
Estrutura de dados para a matriz que contém todos os autômatos.
"""


class CellMatrix:
    # {{{
    def __init__(self, state_matrix, rule, cell_args=None):
        # {{{
        """
        Cria a matriz de autômatos a partir de uma regra e a
        matriz de estado inicial.
        """

        Cell = rule.Cell
        self.state_matrix = state_matrix

        if cell_args is not None:
            self.cell_matrix = np.array(
                [
                    Cell(value, (lin_num, col_num), cell_args)
                    for lin_num, lin in enumerate(self.state_matrix)
                    for col_num, value in enumerate(lin)
                ]
            )
        else:
            self.cell_matrix = np.array(
                [
                    Cell(value, (lin_num, col_num))
                    for lin_num, lin in enumerate(self.state_matrix)
                    for col_num, value in enumerate(lin)
                ]
            )

        self.display_func = np.vectorize(rule.Cell.display)

    # }}}

    @classmethod
    def from_display(cls, display_matrix, rule, cell_args=None):
        # {{{
        """
        Inicializa a partir da matriz de valores RGB ou valor de
        escala monocromática extraídos de uma imagem. Essa
        provavelmente é a maneira mais lenta possível de se fazer
        isso.
        """

        cell_from_display = rule.Cell.from_display
        pixels_gen = (cell_from_display(col) for lin in display_matrix for col in lin)

        state_matrix = np.array(list(pixels_gen))
        state_matrix = state_matrix.reshape(display_matrix.shape[:2])

        return cls(state_matrix, rule, cell_args)

    # }}}

    def display(self):
        # {{{
        """
        Retorna a matriz para representação visual do conjunto de
        células. É feio desse jeito para suportar o células
        retornando tanto inteiros (caso grayscale) quanto tuplas.
        """

        rgb_tuple = self.display_func(self.state_matrix)

        if not isinstance(rgb_tuple, tuple):
            # Isso cheira a um anti-padrão...
            rgb_tuple = (rgb_tuple, rgb_tuple, rgb_tuple)

        rgb_matrix = np.dstack(rgb_tuple).astype(np.uint8)
        return rgb_matrix

    # }}}

    @property
    def shape(self):
        return self.state_matrix.shape


# }}}


class CellMatrixThreaded(CellMatrix):
    # {{{
    def update(self, *args, **kwargs):
        # {{{

        old_state_matrix = self.state_matrix

        update_cell = partial(
            self.update_cell,
            old_state_matrix=old_state_matrix,
            *args, **kwargs
        )

        with Pool() as p:
            new_state_matrix = p.map(update_cell, self.cell_matrix)

        for cell, new_value in zip(self.cell_matrix, new_state_matrix):
            cell.value = new_value

        self.state_matrix = np.array(new_state_matrix).reshape(
            old_state_matrix.shape
        )

        return self.state_matrix

    # }}}

    @staticmethod
    def update_cell(cell, old_state_matrix, *args, **kwargs):
        cell.update(old_state_matrix, *args, **kwargs)
        return cell.value


# }}}


class CellMatrixUnthreaded(CellMatrix):
    # {{{
    def update(self, *args, **kwargs):
        # {{{
        """
        Atualiza o estado de todas as células. Detalhe que é
        necessário copiar a matriz de estados porque matrizes do
        numpy são passadas por referência. A state_matrix é
        modificada in-place.
        """

        old_state_matrix = self.state_matrix.copy()

        for cell in self.cell_matrix:
            cell.update(old_state_matrix, *args, **kwargs)
            self.state_matrix[cell.pos] = cell.value

        return self.state_matrix

    # }}}


# }}}
