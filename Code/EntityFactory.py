#!/usr/bin/python
# -*- coding: utf-8 -*-

from Code.background import Background
from Code.player import Player
from Code.platform import Platform
from Code.flag import Flag
from Code.chest import Chest


class EntityFactory:

    @staticmethod
    def get_entity(entity_name: str):

        if entity_name == "level1":
            return [
                Background("level1", (0, 0)),

                Player((100, 100)),

                Flag((1350, 320)),

                # Baú / ponto de entrega da bandeira
                Chest((142, 350)),

                Platform(0, 650, 1280, 70),
                Platform(250, 520, 250, 30),
                Platform(650, 430, 250, 30),
                Platform(980, 320, 180, 30),
            ]

        return []