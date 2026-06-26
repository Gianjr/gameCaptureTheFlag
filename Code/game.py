#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame

from Code.Menu import Menu
from Code.const import WIN_HEIGHT, WIN_WIDTH, MENU_OPTIONS
from Code.level import Level


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.window = pygame.display.set_mode(
            (WIN_WIDTH, WIN_HEIGHT)
        )

        pygame.display.set_caption("Capture The Flag")

    def play_music(self, music_path, volume=0.35):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1)

    def run(self):

        while True:

            # Música do menu
            self.play_music("./assets/music/musica_menu.wav", 0.35)

            menu = Menu(self.window)
            menu_return = menu.run()

            if menu_return in [
                MENU_OPTIONS[0],
                MENU_OPTIONS[1],
                MENU_OPTIONS[2]
            ]:

                # Música da fase
                self.play_music("./assets/music/MC Hammer - U Can't Touch This (HQ).mp3", 0.35)

                level = Level(
                    self.window,
                    "Level1",
                    menu_return
                )

                level_return = level.run()

            elif menu_return == MENU_OPTIONS[4]:
                pygame.quit()
                quit()

            else:
                pass