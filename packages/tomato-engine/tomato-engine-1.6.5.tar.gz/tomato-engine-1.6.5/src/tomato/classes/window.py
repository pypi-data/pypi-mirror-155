from ..functions import display
import pygame
from time import time
from numpy import mean, std


class Window:

    """
    Uma classe para ser a representação da janelinha da simulação
    no projeto. Sim, porque não temos overhead suficiente.

    Nota-se que a Window não tem acesso direto à CellMatrix. Tudo
    que envolve a CellMatrix passa pela Board, e de lá para a
    Window. Decidi fazer assim porque me pareceu um design mais
    sensato (apesar de mais complicado) e isso deixa a Window
    mais geral.
    """

    def __init__(self, display_matrix, **kwargs):
        # {{{
        """
        Este método faz os preparativos para mostrar a janelinha
        da simulação.
        """

        self.cell_size = kwargs.get("cell_size", 4)
        self.title = kwargs.get("title", "Simulação")
        self.debug = kwargs.get("debug", False)
        self.paused = kwargs.get("paused", False)
        self.max_fps = kwargs.get("max_fps", 60)

        self.clock = pygame.time.Clock()

        if self.debug:
            self.draw_time = []

        self.running = True

        self.screen = display.create_screen(
            display_matrix.shape[:2], self.cell_size, self.title
        )
        pygame.init()
        self.update(display_matrix)

    # }}}

    def update(self, display_matrix):
        # {{{
        """
        Atualiza o conteúdo da tela e seu título.
        """

        initial_time = time()

        self.clock.tick(self.max_fps)
        display.draw_screen(self.screen, display_matrix, self.cell_size)
        pygame.display.flip()

        display_caption = f"{self.title} | FPS: {self.clock.get_fps():.0f}"
        pygame.display.set_caption(display_caption)

        if self.debug:
            self.draw_time.append(1000.0 * (time() - initial_time))

            # Medida de segurança para não entupir a memória com
            # uma lista
            if len(self.draw_time) > 900:
                self.draw_time.pop(0)

            self.print_debug()

    # }}}

    def toggle_pause(self):
        # {{{
        """
        Pausa ou despausa a simulação
        """

        self.paused = True if not self.paused else False

    # }}}

    def query_inputs(self):
        # {{{
        """
        Responde aos inputs do usuário.
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.toggle_pause()

    # }}}

    def quit(self):
        # {{{
        """
        Fecha a janelinha.
        """

        pygame.quit()

        if self.debug:
            self.print_avg_update_time()

    # }}}

    def print_avg_update_time(self):
        # {{{
        print(
            "| Average screen draw time: {} +- {} ms |".format(
                mean(self.draw_time),
                std(self.draw_time),
            )
        )

    # }}}

    def print_debug(self):
        # {{{
        """
        Auto-explicativo. Printa as informações de depuração.
        """

        print(
            "| {:<16} {:<8.4f} | {:<16} {:<8.4f} ms |".format(
                "FPS:",
                self.clock.get_fps(),
                "Draw time:",
                self.draw_time[-1],
            )
        )

    # }}}

    @property
    def inputs(self):
        # {{{
        """
        Retorna a lista com os inputs do usuário na janela.
        """
        return pygame.event.get()

    # }}}
