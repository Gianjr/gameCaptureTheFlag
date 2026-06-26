#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame


class Chest:

    def __init__(self, position):
        self.name = "chest"

        self.closed = pygame.image.load(
            "./assets/chest2/sprite_0.png"
        ).convert_alpha()

        self.open = pygame.image.load(
            "./assets/chest2/sprite_1.png"
        ).convert_alpha()

        self.closed = pygame.transform.scale(self.closed, (34, 34))
        self.open = pygame.transform.scale(self.open, (34, 34))

        self.surf = self.closed
        self.rect = self.surf.get_rect(topleft=position)

        self.opened = False
        self.open_time = 0

    def open_chest(self):
        self.opened = True
        self.surf = self.open
        self.open_time = pygame.time.get_ticks()

    def update(self):
        if self.opened:
            if pygame.time.get_ticks() - self.open_time > 1000:
                self.opened = False
                self.surf = self.closed

    def move(self):
        self.update()