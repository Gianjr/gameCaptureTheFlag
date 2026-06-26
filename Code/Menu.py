#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame.image

from Code.const import WIN_WIDTH, COLOR_ORANGE, MENU_OPTIONS, COLOR_GREY, COLOR_YELLOW


class Menu:
    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load("./assets/menu1.png")
        self.rect = self.surf.get_rect(left=0, top=0)

    def run(self):
        # 1. Configurações iniciais FORA do loop
        global menu_option
        menu_option = 0
        pygame.mixer_music.load("./assets/music/musica_menu.wav")
        pygame.mixer_music.play(-1)

        while True:
            self.window.blit(self.surf, self.rect)
            self.menu_text(50, "Capture", COLOR_ORANGE, (WIN_WIDTH / 2, 70))
            self.menu_text(50, "The", COLOR_ORANGE, (WIN_WIDTH / 2, 120))
            self.menu_text(50, "Flag", COLOR_ORANGE, (WIN_WIDTH / 2, 170))

            # 2. Lógica de desenho corrigida
            for i in range(len(MENU_OPTIONS)):
                if i == menu_option:  # Comparando com o índice selecionado
                    self.menu_text(20, MENU_OPTIONS[i], COLOR_YELLOW, (WIN_WIDTH / 2, 300 + 30 * i))
                else:
                    self.menu_text(20, MENU_OPTIONS[i], COLOR_GREY, (WIN_WIDTH / 2, 300 + 30 * i))

            pygame.display.flip()

            # 3. Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                #   KEYDOWN DOWN
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        if menu_option < len(MENU_OPTIONS) - 1:
                            menu_option += 1
                        else:
                            menu_option = 0
                # KEYDOWN UP
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if menu_option > 0:
                            menu_option -= 1
                        else:
                            menu_option = len(MENU_OPTIONS) - 1
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  #ENTER
                        return MENU_OPTIONS[menu_option]


    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple) -> None:
        text_font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf = text_font.render(text, True, text_color).convert_alpha()
        text_rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(text_surf, text_rect)