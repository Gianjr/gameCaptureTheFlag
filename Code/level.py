#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import json
import os

from Code.entity import Entity
from Code.EntityFactory import EntityFactory
from Code.platform import Platform
from Code.player import Player
from Code.flag import Flag
from Code.chest import Chest


class Level:

    def __init__(self, window, name, game_mode):
        self.window = window
        self.name = name
        self.game_mode = game_mode

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 32)

        self.entity_list: list[Entity] = []
        self.platforms: list[Platform] = []
        self.flags: list[Flag] = []
        self.chests: list[Chest] = []

        self.score = 0

        self.editor_mode = False
        self.drawing = False
        self.start_pos = None
        self.temp_rect = None

        for obj in EntityFactory.get_entity("level1"):

            if isinstance(obj, Platform):
                self.platforms.append(obj)

            elif isinstance(obj, Flag):
                self.flags.append(obj)

            elif isinstance(obj, Chest):
                self.chests.append(obj)

            else:
                self.entity_list.append(obj)

        self.load_platforms()

    def save_platforms(self):
        data = []

        for plat in self.platforms:
            data.append({
                "x": plat.rect.x,
                "y": plat.rect.y,
                "width": plat.rect.width,
                "height": plat.rect.height
            })

        with open("level1_platforms.json", "w") as file:
            json.dump(data, file, indent=4)

        print("Plataformas salvas!")

    def load_platforms(self):
        if not os.path.exists("level1_platforms.json"):
            return

        with open("level1_platforms.json", "r") as file:
            data = json.load(file)

        self.platforms = []

        for item in data:
            self.platforms.append(
                Platform(
                    item["x"],
                    item["y"],
                    item["width"],
                    item["height"]
                )
            )

        print("Plataformas carregadas!")

    def handle_editor_events(self, event):
        mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:
                self.drawing = True
                self.start_pos = mouse_pos

            if event.button == 3:
                for plat in self.platforms[:]:
                    if plat.rect.collidepoint(mouse_pos):
                        self.platforms.remove(plat)

        if event.type == pygame.MOUSEBUTTONUP:

            if event.button == 1 and self.drawing:
                self.drawing = False

                end_pos = mouse_pos

                x = min(self.start_pos[0], end_pos[0])
                y = min(self.start_pos[1], end_pos[1])
                width = abs(self.start_pos[0] - end_pos[0])
                height = abs(self.start_pos[1] - end_pos[1])

                if width > 5 and height > 5:
                    self.platforms.append(
                        Platform(x, y, width, height)
                    )

                self.temp_rect = None

        if event.type == pygame.MOUSEMOTION and self.drawing:
            end_pos = mouse_pos

            x = min(self.start_pos[0], end_pos[0])
            y = min(self.start_pos[1], end_pos[1])
            width = abs(self.start_pos[0] - end_pos[0])
            height = abs(self.start_pos[1] - end_pos[1])

            self.temp_rect = pygame.Rect(x, y, width, height)

    def get_player(self):
        for ent in self.entity_list:
            if isinstance(ent, Player):
                return ent

        return None

    def check_flag_system(self):
        player = self.get_player()

        if player is None:
            return

        for flag in self.flags:

            if not flag.carried and player.rect.colliderect(flag.rect):
                flag.carried = True

            if flag.carried:
                flag.rect.midbottom = player.rect.midtop

                for chest in self.chests:
                    if player.rect.colliderect(chest.rect):
                        self.score += 1
                        chest.open_chest()
                        flag.reset()

    def draw_score(self):
        score_text = self.font.render(
            f"Pontos: {self.score}",
            True,
            (255, 255, 255)
        )

        self.window.blit(score_text, (30, 30))

    def run(self):

        while True:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_F1:
                        self.editor_mode = not self.editor_mode

                    if event.key == pygame.K_s:
                        keys = pygame.key.get_pressed()

                        if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                            self.save_platforms()

                if self.editor_mode:
                    self.handle_editor_events(event)

            for ent in self.entity_list:

                if isinstance(ent, Player):
                    ent.update(self.platforms)
                else:
                    ent.move()

            for chest in self.chests:
                chest.update()

            self.check_flag_system()

            for ent in self.entity_list:
                self.window.blit(ent.surf, ent.rect)

            for chest in self.chests:
                self.window.blit(chest.surf, chest.rect)

            for flag in self.flags:
                flag.move()
                self.window.blit(flag.surf, flag.rect)

            if self.editor_mode:

                for plat in self.platforms:
                    pygame.draw.rect(
                        self.window,
                        (255, 0, 0),
                        plat.rect,
                        2
                    )

                for chest in self.chests:
                    pygame.draw.rect(
                        self.window,
                        (0, 0, 255),
                        chest.rect,
                        2
                    )

                if self.temp_rect:
                    pygame.draw.rect(
                        self.window,
                        (0, 255, 0),
                        self.temp_rect,
                        2
                    )

            self.draw_score()

            pygame.display.flip()
            self.clock.tick(60)