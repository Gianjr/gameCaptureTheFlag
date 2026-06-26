#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame


class Flag:

    def __init__(self, position):
        self.name = "flag"
        self.start_position = position
        self.carried = False

        # Tamanho desejado da bandeira
        self.width = 46
        self.height = 46

        self.frames = []

        for i in range(4):

            image = pygame.image.load(
                f"./assets/flags/sprite_{i}.png"
            ).convert_alpha()

            image = pygame.transform.scale(
                image,
                (self.width, self.height)
            )

            self.frames.append(image)

        self.frame = 0
        self.animation_speed = 0.12

        self.surf = self.frames[0]
        self.rect = self.surf.get_rect(topleft=position)

    def animate(self):

        self.frame += self.animation_speed

        if self.frame >= len(self.frames):
            self.frame = 0

        self.surf = self.frames[int(self.frame)]

    def reset(self):
        self.carried = False
        self.rect.topleft = self.start_position

    def move(self):
        self.animate()