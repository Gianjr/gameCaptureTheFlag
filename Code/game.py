#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame

from Code.Menu import Menu


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((800, 600))

    def run(self):
        global menu
        while True:
            menu = Menu(self.window)
            menu.run()
            pass
        # # running = True
        # # while running:
        #     Verifica todos os eventos
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             running = False
        #
        # pygame.quit()
