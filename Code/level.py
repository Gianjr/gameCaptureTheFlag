#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame

from Code.entity import Entity
from Code.EntityFactory import EntityFactory


class Level:
    def __init__(self, whindow, name, game_mode):
        self.window = whindow
        self.name = name
        self.game_mode = game_mode
        self.entity_list: list[Entity] = []
        self.entity_list.extend(EntityFactory.get_entity('level1'))

    def run(self):
        while True:
            for ent in self.entity_list:
                self.window.blit(source=ent.surf, dest=ent.rect)
                pygame.display.flip()
        pass