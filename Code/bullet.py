#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import math


class Bullet:

    def __init__(self, x, y, target_x, target_y, speed=4, color=(255, 220, 0)):
        self.name = "bullet"

        self.surf = pygame.Surface((12, 12), pygame.SRCALPHA)
        pygame.draw.circle(self.surf, color, (6, 6), 6)

        self.rect = self.surf.get_rect(center=(x, y))

        self.speed = speed

        dx = target_x - x
        dy = target_y - y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance == 0:
            distance = 1

        self.velocity_x = (dx / distance) * self.speed
        self.velocity_y = (dy / distance) * self.speed

    def update(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

    def is_off_screen(self, width, height):
        return (
            self.rect.right < -200
            or self.rect.left > width + 200
            or self.rect.bottom < -200
            or self.rect.top > height + 200
        )