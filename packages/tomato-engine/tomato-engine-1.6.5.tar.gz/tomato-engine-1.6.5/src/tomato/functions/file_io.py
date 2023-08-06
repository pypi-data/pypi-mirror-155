import glob
import os

import numpy as np
from PIL import Image

"""
Funções relacionadas a ler e escrever arquivos.
"""


def img(display_matrix, size=1):
    # {{{
    """
    Define uma imagem Image do PIL, da biblioteca pillow
    """

    y, x = (size * display_matrix.shape[0], size * display_matrix.shape[1])

    # Somente nesta função o PIL entende que a imagem está em lin, col, e não x, y
    img_pil = Image.fromarray(display_matrix)

    img_pil = img_pil.resize(
        (x, y),
        resample=Image.NEAREST,
    )
    return img_pil


# }}}


def load_png(path, size=1):
    # {{{
    """
    O 'size' se refere ao tamanho da célula na imagem. Se for 1,
    a imagem inteira será usada, se for 2, cada segundo pixel
    será excluído, e assim por diante.
    """

    img = Image.open(path).convert()
    # img = img.transpose(Image.TRANSPOSE)
    # O :: é o que faz considerar somente os elementos de índice
    # divisível por size
    img_matrix = np.array(img)[0::size, 0::size]

    return img_matrix


# }}}


def save_png(path, display_matrix, size=1, print_output=True):
    # {{{
    img_pil = img(display_matrix, size)

    if print_output:
        print(f"Imagem salva em {path}.")

    img_pil.save(path, "PNG")


# }}}


def save_gif(path, fps):
    # {{{
    fp_in = f"{path}*.png"
    fp_out = f"{path}out.gif"

    imgs = (
        Image.open(f)
        for f in sorted(
            glob.glob(fp_in),
            key=lambda x: int(os.path.splitext(os.path.basename(x))[0]),
        )
    )
    imga = next(imgs)
    duration = 1 / fps
    imga.save(
        fp=fp_out,
        format="GIF",
        append_images=imgs,
        save_all=True,
        fps=fps,
        duration=duration,
        loop=1,
    )


# }}}


def record_values(file_obj, values, separator="\t"):
    # {{{
    """
    Uma função de conveniência para salvar os elementos do iterável values em
    um arquivo de texto, uma operação bastante comum.
    """

    line = separator.join(str(x) for x in values) + "\n"
    file_obj.write(line)


# }}}


def read_from_record(file_path, value_types=None, num_values=None, separator="\t"):
    # {{{
    """
    Lê os valores de cada linha de file_obj.

    file_types é uma tupla de tipos (como int, float, np.uint8, etc.), e tem
    que ter o mesmo comprimento do número de valores em cada linha a ser lida
    do arquivo. Essa função vai converter os valores que lê do arquivo aos
    respectivos tipos. Se file_types for None, não converte nada.
    """

    if num_values is None and value_types is None:
        num_values = number_of_values_line(file_path, separator=separator)
    elif value_types is not None:
        num_values = len(value_types)

    # Tupla com uma lista para cada coluna no arquivo
    cols = tuple([] for x in range(num_values))

    with open(file_path, "r") as record:

        # Poderia colocar esses elifs dentro do for line in record, mas aí
        # seria mais lento, apesar de mais sucinto
        if value_types is None:
            for line in record:
                separated_line = line.split(separator)

                for index, col in enumerate(cols):
                    col.append(separated_line[index])

        # value_types é iterável. se não for, fudeu
        elif isinstance(value_types, (tuple, list, np.ndarray)):
            for line in record:
                separated_line = line.split(separator)

                for index, col in enumerate(cols):
                    col.append(value_types[index](separated_line[index]))

        else:
            raise ValueError("value_types is not iterable")

    return cols


# }}}


def number_of_values_line(file_path, separator="\t"):
    # {{{
    """
    Descobre o número de valores por linha no arquivo. É chamada pela
    read_from_record se o número de valores não for especificado.
    """

    with open(file_path, "r") as record:
        for line in record:
            separated_line = line.split(separator)

            if separated_line[0] == "#":
                # ignorar comentários
                continue
            else:
                return len(separated_line)


# }}}
