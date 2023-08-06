import numpy as np

"""
Funções miscelâneas, de conveniência.
"""


def get_wrapped(matrix, i, j):
    # {{{
    """
    Pega um elemento na matriz, com a propriedade adicional de
    dar a volta pela linha ou coluna quando o índice é maior que
    o tamanho da matriz.
    """

    m, n = matrix.shape
    return matrix[i % m, j % n]


# }}}


def random_matrix(size, values=2):
    # {{{
    """
    Gera uma matriz aleatória. Como vai gerar essa matriz depende
    do tipo do argumento 'values', então verifique as funções
    para saber mais.
    """

    # Se o size for um inteiro, assume-se que o usuário quer uma
    # matriz quadrada.
    if isinstance(size, (int, np.integer)):
        size = (size, size)

    if isinstance(values, (int, np.integer)):
        return random_int_matrix(size, values)
    elif isinstance(values, (tuple, list, np.ndarray)):
        return random_choice_matrix(size, values)
    elif isinstance(values, (float, np.float64)):
        return random_float_matrix(size, values)
    elif isinstance(values, (str)):
        if values in ("standard normal", "normal"):
            return normal_matrix(size)


# }}}


def random_int_matrix(size, to_int, from_int=0, seed=None):
    # {{{
    """
    Gera uma matriz de inteiros aleatórios entre from_int e
    to_int, de dimensões size.
    """

    rng = np.random.default_rng(seed=seed)
    return rng.integers(
        low=from_int,
        high=to_int,
        size=size,
    )


# }}}


def random_choice_matrix(size, values, seed=None):
    # {{{
    """
    Gera uma matriz com valores aleatoriamente escolhidos dentre
    o iterável values. Detalhe que se o values conter valores de
    tipos diferentes, tudo vai virar strings do numpy (tipo <U21)
    na matriz gerada.
    """

    rng = np.random.default_rng(seed=seed)
    return rng.choice(values, size)


# }}}


def random_float_matrix(
    size,
    to_float,
    from_float=0,
    seed=None,
):
    # {{{
    """
    Gera uma matriz de valores aleatórios entre from_float e
    to_float seguindo uma distribuição uniforme.
    """

    rng = np.random.default_rng(seed=seed)
    return rng.uniform(
        low=from_float,
        high=to_float,
        size=size,
    )


# }}}


def normal_matrix(size, mean=0.0, std_dev=1.0, seed=None):
    # {{{
    """
    Retorna uma matriz de floats aleatórios conforme uma
    distribuição normal (gaussiana) com média e desvio padrão
    especificados.
    """

    rng = np.random.default_rng(seed=seed)
    return rng.normal(loc=mean, scale=std_dev, size=size)


# }}}


def cross_matrix(size, value):
    # {{{
    """
    Cria uma matriz com uma cruz no meio, com o valor
    especificado.
    """
    try:
        # size é iteráevel
        m, n = size
    except TypeError:
        # size é intenro (eu espero)
        m, n = size, size

    state_matrix = np.zeros((m, n))
    state_matrix[m // 2, n // 2] = value
    state_matrix[m // 2 + 1, n // 2] = value
    state_matrix[m // 2 - 1, n // 2] = value
    state_matrix[m // 2, n // 2 - 1] = value
    state_matrix[m // 2, n // 2 + 1] = value

    return state_matrix


# }}}


def vertical_padding(num_lines, first_line):

    """
    Cria uma matriz de num_lines linhas na qual first_line é a primeira linha
    e o resto é 0. Útil para autômatos 1D.
    """

    matrix = np.zeros(((num_lines - 1), len(first_line)))
    matrix[0,:] = first_line
    return matrix
