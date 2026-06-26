#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import math


class Bullet:

    def __init__(self, x, y, target_x, target_y, speed=4, color=(255, 220, 0)):
        self.name = "bullet"

        self.surf = pygame.Surface((18, 18), pygame.SRCALPHA)

        pygame.draw.circle(self.surf, (*color, 80), (9, 9), 9)
        pygame.draw.circle(self.surf, color, (9, 9), 5)
        pygame.draw.circle(self.surf, (255, 255, 255), (7, 7), 2)

        self.x = float(x)
        self.y = float(y)

        self.rect = self.surf.get_rect(center=(self.x, self.y))

        dx = target_x - x
        dy = target_y - y

        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance == 0:
            distance = 1

        self.velocity_x = (dx / distance) * speed
        self.velocity_y = (dy / distance) * speed

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        self.rect.center = (
            int(self.x),
            int(self.y)
        )

    def is_off_screen(self, width, height):
        return (
            self.rect.right < -50
            or self.rect.left > width + 50
            or self.rect.bottom < -50
            or self.rect.top > height + 50
        )