#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame

from Code.const import (
    WIN_WIDTH,
    WIN_HEIGHT,
    COLOR_ORANGE,
    COLOR_GREY,
    COLOR_YELLOW,
    MENU_OPTIONS
)


class Menu:

    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load("./assets/menu1.png")
        self.rect = self.surf.get_rect(left=0, top=0)

    def run(self):
        menu_option = 0

        while True:
            self.window.blit(self.surf, self.rect)

            self.menu_text(52, "Capture", COLOR_ORANGE, (WIN_WIDTH / 2, 70))
            self.menu_text(52, "The", COLOR_ORANGE, (WIN_WIDTH / 2, 120))
            self.menu_text(52, "Flag", COLOR_ORANGE, (WIN_WIDTH / 2, 170))

            for i in range(len(MENU_OPTIONS)):
                color = COLOR_YELLOW if i == menu_option else COLOR_GREY
                self.menu_text(24, MENU_OPTIONS[i], color, (WIN_WIDTH / 2, 300 + 35 * i))

            painel = pygame.Surface((390, 170), pygame.SRCALPHA)
            painel.fill((0, 0, 0, 120))
            self.window.blit(painel, (20, WIN_HEIGHT - 190))

            self.menu_text(
                18,
                "SETA CIMA       Pular",
                (255, 255, 255),
                (215, WIN_HEIGHT - 110)
            )

            self.menu_text(
                18,
                    "SETA ESQUERDA/DIREITA      Movimento",
                (255, 255, 255),
                (215, WIN_HEIGHT - 80)
            )

            self.menu_text(
                18,
                "ESPACO          Ataque em breve",
                (255, 255, 255),
                (215, WIN_HEIGHT - 50)
            )

            self.menu_text(
                18,
                "ENTER           Selecionar",
                (255, 255, 255),
                (215, WIN_HEIGHT - 20)
            )
            pygame.display.flip()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_DOWN:
                        menu_option += 1
                        if menu_option >= len(MENU_OPTIONS):
                            menu_option = 0

                    elif event.key == pygame.K_UP:
                        menu_option -= 1
                        if menu_option < 0:
                            menu_option = len(MENU_OPTIONS) - 1

                    elif event.key == pygame.K_RETURN:
                        return MENU_OPTIONS[menu_option]

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font = pygame.font.SysFont("Lucida Sans Typewriter", text_size, bold=True)
        text_surf = text_font.render(text, True, text_color).convert_alpha()
        text_rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(text_surf, text_rect)