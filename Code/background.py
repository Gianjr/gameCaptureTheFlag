#!/usr/bin/python
# -*- coding: utf-8 -*-

from Code.entity import Entity

class Background(Entity):

    def __init__(self, name:str, position:tuple):
        super().__init__(name, position)

    def move(self):
        self.rect.centerx
