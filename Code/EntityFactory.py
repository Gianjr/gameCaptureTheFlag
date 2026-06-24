#!/usr/bin/python
# -*- coding: utf-8 -*-
from Code.background import Background


class EntityFactory:

    @staticmethod
    def get_entity(entity_name: str, position=(0, 0)):

        if entity_name == "level1":
            return [
                Background("level1", (0, 0))
            ]

        return []
