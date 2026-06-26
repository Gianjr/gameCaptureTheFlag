#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import sys

from Code.Menu import Menu
from Code.const import WIN_HEIGHT, WIN_WIDTH, MENU_OPTIONS
from Code.level import Level


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.window = pygame.display.set_mode(
            (WIN_WIDTH, WIN_HEIGHT),
            pygame.FULLSCREEN | pygame.SCALED
        )

        pygame.display.set_caption("Capture The Flag")

    def play_music(self, music_path, volume=0.35):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1)

    def run(self):

        while True:

            self.play_music("./assets/music/menu_music.wav", 0.35)

            menu = Menu(self.window)
            menu_return = menu.run()

            if menu_return in [
                MENU_OPTIONS[0],
                MENU_OPTIONS[1],
                MENU_OPTIONS[2]
            ]:

                self.play_music("./assets/music/The Last Encounter (90s RPG Version).mp3", 0.35)

                level = Level(
                    self.window,
                    "Level1",
                    menu_return
                )

                level_return = level.run()

                if level_return == "menu":
                    continue

            elif menu_return == MENU_OPTIONS[4]:
                pygame.quit()
                sys.exit()