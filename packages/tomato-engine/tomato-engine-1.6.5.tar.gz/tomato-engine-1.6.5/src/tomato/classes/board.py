from ..functions import file_io
from .cellmatrix import CellMatrixUnthreaded, CellMatrixThreaded
from .window import Window
import numpy as np
from time import time
import os
from IPython import display


class Board:

    """
    O nome dessa classe é vago, mas ela é importante. Esta é a
    interface do usuário, e também coordena a CellMatrix e a
    Window.
    """

    def __init__(self, rule, **kwargs):
        # {{{
        """
        Recebe a regra a ser adotada, assim como algumas
        configurações. A simulação em si começa com a função
        start.

        A rule é o módulo importado contendo a regra, no
        formato especificado pelo exemplo game_of_life.py.
        """

        self.rule = rule

        # Configurações opcionais são passadas por kwargs.
        self.debug = kwargs.get("debug", False)
        self.title = kwargs.get("title", "Simulação")
        self.max_fps = kwargs.get("max_fps", 60)
        self.cell_size = kwargs.get("cell_size", 4)

        self.generation = 0

        if self.debug:
            # Lista com o tempo transcorrido para cada geração
            self.gen_time = []

    # }}}

    def start(self, state_matrix, **kwargs):
        # {{{
        """
        Inicia a simulação, o estado inicial sendo dado pela
        state_matrix. state_matrix pode ser o caminho para uma
        imagem ou uma matriz de numpy com os valores desejados.
        """

        cell_args = kwargs.get("cell_args", None)
        show_window = kwargs.get("show_window", True)
        multithreaded = kwargs.get("multithreaded", False)
        self.paused = kwargs.get("paused", False)
        self.generations = kwargs.get("generations", None)
        self.inline = kwargs.get("inline", False)
        self.generate_figures = kwargs.get("generate_figures", False)
        self.generate_figures_dir = kwargs.get(
            "generate_figures_dir", f"{self.title}{os.path.sep}"
        )
        self.generate_gif = kwargs.get("generate_gif", False)
        self.step = kwargs.get("step", None)

        if self.inline is True:
            show_window = False

        if self.generate_gif:
            self.generate_figures = True
            if self.generations is None:
                raise TypeError(
                    f"You must specify the number of generations for the gif to be created."
                )

        if self.generate_figures:
            self.check_dir(self.generate_figures_dir)

        self.load_state(state_matrix, cell_args, multithreaded)

        if show_window:
            self.show_window()
        else:
            self.mainloop()

    # }}}

    def update(self, *args, **kwargs):
        # {{{
        """
        Atualiza o estado da simulação, ou seja, realiza uma nova
        iteração.
        """
        try:
            if self.generate_figures:
                if self.step is None:
                    self.save_png()
                else:
                    if self.generation % self.step == 0:
                        self.save_png()
            if self.inline:
                display.clear_output(wait=True)
                display.display(
                    file_io.img(self.display_matrix, self.cell_size)
                )
        except AttributeError:
            pass
        if not self.debug:
            self.cellMatrix.update(*args, **kwargs)
        else:
            initial_time = time()
            self.cellMatrix.update()
            self.gen_time.append(1000.0 * (time() - initial_time))

        self.generation += 1

    # }}}

    def show_window(self, paused=None):
        # {{{
        """
        Começa a simulação, mostrando a janelinha.
        """

        if paused is None:
            try:
                paused = self.paused
            except AttributeError:
                paused = False

        window = Window(
            self.cellMatrix.display(),
            debug=self.debug,
            title=self.title,
            paused=paused,
            max_fps=self.max_fps,
            cell_size=self.cell_size,
        )

        while window.running:
            window.query_inputs()

            if window.paused is False:
                self.update()
                window.update(self.cellMatrix.display())

                if self.debug:
                    self.print_debug()

                try:
                    if self.generations is not None:
                        if self.generation >= self.generations:
                            window.running = False
                        if self.generation == self.generations:
                            if self.generate_gif:
                                self.save_gif()
                except AttributeError:
                    pass

        if self.debug:
            self.print_avg_update_time()

        # Para lembrar como o usuário deixou a janela
        self.paused = window.paused
        self.max_fps = window.max_fps

        window.quit()

    # }}}

    def mainloop(self):
        # {{{
        """
        Começa a simulação, sem mostrar a janelinha.
        """

        running = True
        while running:
            try:
                self.update()
            except KeyboardInterrupt:
                break

            if self.debug:
                self.print_debug()

            if self.generations is not None:
                if self.generation >= self.generations:
                    running = False
                if self.generation == self.generations:
                    if self.generate_gif:
                        self.save_gif()

        if self.debug:
            self.print_avg_update_time()

    # }}}

    def load_state(self, state_matrix, cell_args=None, multithreaded=False):
        # {{{
        """
        Carrega uma matriz de estados a partir de uma imagem, uma
        matriz numpy ou uma lista de listas.
        """

        if multithreaded:
            CellMatrix = CellMatrixThreaded
        else:
            CellMatrix = CellMatrixUnthreaded

        if isinstance(state_matrix, str):
            png_matrix = file_io.load_png(state_matrix, size=self.cell_size)
            self.cellMatrix = CellMatrix.from_display(
                png_matrix, self.rule, cell_args
            )
        elif isinstance(state_matrix, np.ndarray):
            self.cellMatrix = CellMatrix(state_matrix, self.rule, cell_args)
        elif isinstance(state_matrix, list):
            state_matrix = np.array(state_matrix)
            self.cellMatrix = CellMatrix(state_matrix, self.rule, cell_args)
        else:
            raise TypeError(
                f"{type(state_matrix)} is not a valid type for a state matrix."
            )

    # }}}

    def print_debug(self):
        # {{{
        """
        Auto-explicativo. Printa as informações de depuração.
        """

        print(
            "| {:<16} {:<8} | {:<16} {:<8.4f} ms |".format(
                "Generation:",
                self.generation,
                "Generation time:",
                self.gen_time[-1],
            )
        )

    # }}}

    def print_avg_update_time(self):
        # {{{
        """
        Método bem específico. Printa o tempo médio das gerações
        e o desvio padrão.
        """

        print(
            "| Average generation time: {} +- {} ms |".format(
                np.mean(self.gen_time),
                np.std(self.gen_time),
            )
        )

    # }}}

    def save_png(self, path=None):
        # {{{
        """
        Salva o estado da cellMatrix em uma png, para
        visualização e para retomar a simulação depois.
        """
        if path[-4:] != ".png":      # gamb
            if path is None:
                path = f"{self.generate_figures_dir}"
            elif not path.endswith(f"{os.path.sep}"):
                path = f"{path}{os.path.sep}"

            path = f"{path}{self.generation}.png"

        file_io.save_png(
            path, self.display_matrix, self.cell_size, print_output=False
        )

    # }}}

    def save_gif(self, path=None, max_fps=60):
        # {{{
        """
        Salva o estado da cellMatrix em uma png, para
        visualização e para retomar a simulação depois.
        """
        if path is None:
            path = f"{self.generate_figures_dir}"

        file_io.save_gif(path, fps=self.max_fps)

    # }}}

    def check_dir(self, add=0):
# {{{
        """
        Função para checar se o diretório existe e renomear
        com números inteiros em sequência para a criação de outro diretório.
        """
        i = 1
        dir = self.generate_figures_dir
        if dir is None:
            dir = f"{self.title}{os.path.sep}"
        if not dir.endswith(f"{os.path.sep}"):
            dir = f"{dir}{os.path.sep}"
        while os.path.isdir(dir):
            num = "%03d" % i
            dir = (
                dir.split(f"{os.path.sep}")[0].split("_")[0]
                + "_"
                + f"{num}"
                + f"{os.path.sep}"
            )
            i += 1
        os.mkdir(dir)
        self.generate_figures_dir = dir
# }}}

    def current_time_millis(self):
# {{{
        """
        Função auxiliar para retornar o tempo UNIX em milissegundos
        arredondado.
        """
        return round(time() * 1000)
# }}}

    @property
    def state_matrix(self):
        # {{{
        """
        Propriedade de conveniência para acessar a matriz de estados.
        """

        return self.cellMatrix.state_matrix

    # }}}

    @property
    def display_matrix(self):
        # {{{
        """
        Propriedade de conveniência para acessar a matriz display.
        """

        return self.cellMatrix.display()


# }}}
