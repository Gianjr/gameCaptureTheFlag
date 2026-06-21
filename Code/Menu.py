#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame.image

from Code.const import WIN_WIDTH, COLOR_ORANGE, MENU_OPTIONS, COLOR_WHITE


class Menu:
    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load("./assets/1.png")
        self.rect = self.surf.get_rect(left=0, top=0)


    def run(self):



        pygame.mixer_music.load("./assets/musica_menu.wav")
        pygame.mixer_music.play(-1)

        while True:
            self.window.blit(self.surf, self.rect)
            self.menu_text(50,"Capture",(COLOR_ORANGE),((WIN_WIDTH/2),70))
            self.menu_text(50, "The", (COLOR_ORANGE), ((WIN_WIDTH / 2), 120))
            self.menu_text(50, "Flag", (COLOR_ORANGE), ((WIN_WIDTH / 2), 170))

            for i in range(len(MENU_OPTIONS)):
                self.menu_text(20, MENU_OPTIONS[i], (COLOR_WHITE), ((WIN_WIDTH / 2), 500 + 30 * i))
            pygame.display.flip()


            # running = True
            # while running:
            #     Verifica todos os eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()


    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf = text_font.render(text, True, text_color).convert_alpha()
        text_rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(text_surf, text_rect)