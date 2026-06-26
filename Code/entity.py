#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame


class Entity:

    def __init__(self, name: str, position: tuple):

        self.name = name

        self.surf = pygame.image.load(
            "./assets/" + name + ".png"
        ).convert_alpha()

        self.rect = self.surf.get_rect(
            topleft=position
        )

        self.speed = 0

    def move(self):
        pass