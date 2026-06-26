#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame


class Platform:

    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def move(self):
        pass