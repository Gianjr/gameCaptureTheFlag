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
from Code.enemy import Enemy


class Level:

    def __init__(self, window, name, game_mode):
        self.window = window
        self.name = name
        self.game_mode = game_mode

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 32)
        self.big_font = pygame.font.SysFont("Arial", 72)

        self.entity_list: list[Entity] = []
        self.platforms: list[Platform] = []
        self.flags: list[Flag] = []
        self.chests: list[Chest] = []
        self.enemies: list[Enemy] = []
        self.bullets = []

        self.score = 0
        self.max_score = 5

        self.lives = 3
        self.max_lives = 3

        self.current_level = 1
        self.max_level = 3

        self.game_over = False
        self.level_completed = False

        self.player_start_position = (100, 100)

        self.heart_size = (40, 40)

        self.heart_full = pygame.image.load(
            "./assets/heart/full.png"
        ).convert_alpha()

        self.heart_empty = pygame.image.load(
            "./assets/heart/empty.png"
        ).convert_alpha()

        self.heart_full = pygame.transform.scale(
            self.heart_full,
            self.heart_size
        )

        self.heart_empty = pygame.transform.scale(
            self.heart_empty,
            self.heart_size
        )

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

            elif isinstance(obj, Enemy):
                self.enemies.append(obj)

            else:
                self.entity_list.append(obj)

        self.load_platforms()
        self.apply_level_difficulty()

    def apply_level_difficulty(self):
        if self.current_level == 1:
            shoot_delay = 1700
            bullet_speed = 3
            bullet_color = (255, 220, 0)

        elif self.current_level == 2:
            shoot_delay = 1200
            bullet_speed = 5
            bullet_color = (255, 120, 0)

        else:
            shoot_delay = 800
            bullet_speed = 7
            bullet_color = (255, 0, 0)

        for enemy in self.enemies:
            enemy.set_difficulty(
                shoot_delay,
                bullet_speed,
                bullet_color
            )

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

    def reset_player(self):
        player = self.get_player()

        if player:
            player.rect.topleft = self.player_start_position
            player.velocity_y = 0
            player.on_ground = False

        self.bullets.clear()

        for flag in self.flags:
            flag.reset()

    def restart_game(self):
        self.score = 0
        self.lives = self.max_lives
        self.current_level = 1
        self.game_over = False
        self.level_completed = False
        self.apply_level_difficulty()
        self.reset_player()

    def player_take_damage(self):
        if self.game_over:
            return

        self.lives -= 1
        print(f"Player levou dano! Vidas: {self.lives}")

        if self.lives <= 0:
            self.lives = 0
            self.game_over = True
            self.bullets.clear()
            print("GAME OVER")

        else:
            self.reset_player()

    def next_level(self):
        self.current_level += 1

        if self.current_level > self.max_level:
            self.current_level = self.max_level
            self.level_completed = True
            print("Todos os níveis completos!")
            return

        self.score = 0
        self.bullets.clear()
        self.apply_level_difficulty()
        self.reset_player()

        print(f"Indo para o nível {self.current_level}")

    def check_level_complete(self):
        if self.score >= self.max_score:
            self.next_level()

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
                        self.check_level_complete()

    def update_bullets(self, player):
        screen_width = self.window.get_width()
        screen_height = self.window.get_height()

        for bullet in self.bullets[:]:
            bullet.update()

            if bullet.rect.colliderect(player.rect):
                self.bullets.remove(bullet)
                self.player_take_damage()
                continue

            if bullet.is_off_screen(screen_width, screen_height):
                self.bullets.remove(bullet)

    def draw_hud(self):
        score_text = self.font.render(
            f"Bandeiras: {self.score}/{self.max_score}",
            True,
            (255, 255, 255)
        )

        level_text = self.font.render(
            f"Nível: {self.current_level}",
            True,
            (255, 255, 255)
        )

        self.window.blit(score_text, (30, 30))
        self.window.blit(level_text, (30, 70))

        for i in range(self.max_lives):

            if i < self.lives:
                self.window.blit(
                    self.heart_full,
                    (30 + i * 45, 110)
                )
            else:
                self.window.blit(
                    self.heart_empty,
                    (30 + i * 45, 110)
                )

        if self.game_over:
            game_over_text = self.big_font.render(
                "GAME OVER",
                True,
                (255, 0, 0)
            )

            restart_text = self.font.render(
                "Aperte ENTER para reiniciar",
                True,
                (255, 255, 255)
            )

            self.window.blit(
                game_over_text,
                (
                    self.window.get_width() // 2 - game_over_text.get_width() // 2,
                    self.window.get_height() // 2 - 80
                )
            )

            self.window.blit(
                restart_text,
                (
                    self.window.get_width() // 2 - restart_text.get_width() // 2,
                    self.window.get_height() // 2
                )
            )

        if self.level_completed:
            complete_text = self.big_font.render(
                "VOCÊ VENCEU!",
                True,
                (255, 255, 0)
            )

            self.window.blit(
                complete_text,
                (
                    self.window.get_width() // 2 - complete_text.get_width() // 2,
                    self.window.get_height() // 2 - 80
                )
            )

    def run(self):

        while True:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_RETURN and self.game_over:
                        self.restart_game()

                    if event.key == pygame.K_F1:
                        self.editor_mode = not self.editor_mode

                    if event.key == pygame.K_s:
                        keys = pygame.key.get_pressed()

                        if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                            self.save_platforms()

                if self.editor_mode:
                    self.handle_editor_events(event)

            player = self.get_player()

            if not self.game_over and not self.level_completed:

                for ent in self.entity_list:

                    if isinstance(ent, Player):
                        ent.update(self.platforms)
                    else:
                        ent.move()

                if player:
                    for enemy in self.enemies:
                        enemy.update(player, self.bullets)

                for chest in self.chests:
                    chest.update()

                self.check_flag_system()

                if player:
                    self.update_bullets(player)

            for ent in self.entity_list:
                self.window.blit(ent.surf, ent.rect)

            for chest in self.chests:
                self.window.blit(chest.surf, chest.rect)

            for flag in self.flags:
                flag.move()
                self.window.blit(flag.surf, flag.rect)

            for enemy in self.enemies:
                self.window.blit(enemy.surf, enemy.rect)

            for bullet in self.bullets:
                self.window.blit(bullet.surf, bullet.rect)

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

            self.draw_hud()

            pygame.display.flip()
            self.clock.tick(60)