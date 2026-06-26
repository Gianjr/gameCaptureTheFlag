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
        self.font = pygame.font.SysFont("Arial", 32, bold=True)
        self.big_font = pygame.font.SysFont("Arial", 76, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 24, bold=True)

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
        self.paused = False

        #screen effects
        self.show_level_intro = True
        self.level_intro_start = pygame.time.get_ticks()
        self.level_intro_duration = 1800

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

        self.continue_button = pygame.Rect(
            self.window.get_width() // 2 - 150,
            self.window.get_height() // 2 - 40,
            300,
            50
        )

        self.exit_button = pygame.Rect(
            self.window.get_width() // 2 - 150,
            self.window.get_height() // 2 + 30,
            300,
            50
        )

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

    def draw_text_shadow(self, text, font, color, center_pos, shadow_color=(0, 0, 0), shadow_offset=4):
        shadow = font.render(text, True, shadow_color)
        shadow_rect = shadow.get_rect(
            center=(center_pos[0] + shadow_offset, center_pos[1] + shadow_offset)
        )
        self.window.blit(shadow, shadow_rect)

        surf = font.render(text, True, color)
        rect = surf.get_rect(center=center_pos)
        self.window.blit(surf, rect)

    def draw_dark_overlay(self, alpha=170):
        overlay = pygame.Surface(
            (self.window.get_width(), self.window.get_height()),
            pygame.SRCALPHA
        )
        overlay.fill((0, 0, 0, alpha))
        self.window.blit(overlay, (0, 0))

    def apply_level_difficulty(self):
        if self.current_level == 1:
            self.max_score = 3
            shoot_delay = 1700
            bullet_speed = 3
            bullet_color = (255, 220, 0)

        elif self.current_level == 2:
            self.max_score = 5
            shoot_delay = 1200
            bullet_speed = 5
            bullet_color = (255, 120, 0)

        else:
            self.max_score = 10
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
        self.paused = False
        self.show_level_intro = True
        self.level_intro_start = pygame.time.get_ticks()
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
            self.paused = False
            self.bullets.clear()
            print("GAME OVER")

        else:
            self.reset_player()

    def next_level(self):
        self.current_level += 1

        if self.current_level > self.max_level:
            self.current_level = self.max_level
            self.level_completed = True
            self.bullets.clear()
            print("Todos os níveis completos!")
            return

        self.score = 0
        self.bullets.clear()

        self.apply_level_difficulty()
        self.reset_player()

        self.show_level_intro = True
        self.level_intro_start = pygame.time.get_ticks()

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

        hud_panel = pygame.Surface((430, 85), pygame.SRCALPHA)
        hud_panel.fill((0, 0, 0, 95))

        pygame.draw.rect(
            hud_panel,
            (255, 180, 0, 180),
            hud_panel.get_rect(),
            2,
            border_radius=14
        )

        self.window.blit(hud_panel, (20, 20))

        # Flags
        flag_text = self.font.render(
            f"Bandeiras: {self.score}/{self.max_score}",
            True,
            (255, 255, 255)
        )

        self.window.blit(flag_text, (40, 43))

        # Hearts
        heart_start_x = 280
        heart_y = 40

        for i in range(self.max_lives):

            if i < self.lives:
                self.window.blit(
                    self.heart_full,
                    (heart_start_x + i * 45, heart_y)
                )
            else:
                self.window.blit(
                    self.heart_empty,
                    (heart_start_x + i * 45, heart_y)
                )

        # Level

        level_panel = pygame.Surface((180, 55), pygame.SRCALPHA)
        level_panel.fill((0, 0, 0, 95))

        pygame.draw.rect(
            level_panel,
            (255, 180, 0, 180),
            level_panel.get_rect(),
            2,
            border_radius=14
        )

        level_x = self.window.get_width() // 2 - 90
        self.window.blit(level_panel, (level_x, 20))

        level_text = self.font.render(
            f"Nível {self.current_level}",
            True,
            (255, 220, 0)
        )

        self.window.blit(
            level_text,
            level_text.get_rect(
                center=(self.window.get_width() // 2, 48)
            )
        )

    def draw_level_intro(self):
        if not self.show_level_intro:
            return

        elapsed = pygame.time.get_ticks() - self.level_intro_start

        if elapsed > self.level_intro_duration:
            self.show_level_intro = False
            return

        self.draw_dark_overlay(150)

        scale = 1 + 0.08 * abs((elapsed % 600) - 300) / 300

        level_text = self.big_font.render(
            f"NÍVEL {self.current_level}",
            True,
            (255, 220, 0)
        )

        level_text = pygame.transform.scale(
            level_text,
            (
                int(level_text.get_width() * scale),
                int(level_text.get_height() * scale)
            )
        )

        rect = level_text.get_rect(
            center=(
                self.window.get_width() // 2,
                self.window.get_height() // 2 - 40
            )
        )

        shadow = self.big_font.render(
            f"NÍVEL {self.current_level}",
            True,
            (0, 0, 0)
        )

        shadow = pygame.transform.scale(
            shadow,
            (
                int(shadow.get_width() * scale),
                int(shadow.get_height() * scale)
            )
        )

        shadow_rect = shadow.get_rect(
            center=(rect.centerx + 5, rect.centery + 5)
        )

        self.window.blit(shadow, shadow_rect)
        self.window.blit(level_text, rect)

        if self.current_level == 1:
            info = "Tiros lentos"
        elif self.current_level == 2:
            info = "Tiros mais rápidos"
        else:
            info = "Perigo máximo!"

        self.draw_text_shadow(
            info,
            self.font,
            (255, 255, 255),
            (
                self.window.get_width() // 2,
                self.window.get_height() // 2 + 45
            )
        )

    def draw_game_over_screen(self):
        if not self.game_over:
            return

        self.draw_dark_overlay(210)

        pulse = pygame.time.get_ticks() % 1000
        red = 180 + int(75 * abs(pulse - 500) / 500)

        self.draw_text_shadow(
            "GAME OVER",
            self.big_font,
            (red, 0, 0),
            (
                self.window.get_width() // 2,
                self.window.get_height() // 2 - 100
            ),
            (0, 0, 0),
            6
        )

        pygame.draw.rect(
            self.window,
            (30, 30, 30),
            (
                self.window.get_width() // 2 - 250,
                self.window.get_height() // 2 - 20,
                500,
                120
            ),
            border_radius=18
        )

        pygame.draw.rect(
            self.window,
            (255, 0, 0),
            (
                self.window.get_width() // 2 - 250,
                self.window.get_height() // 2 - 20,
                500,
                120
            ),
            3,
            border_radius=18
        )

        self.draw_text_shadow(
            "ENTER  Reiniciar",
            self.font,
            (255, 255, 255),
            (
                self.window.get_width() // 2,
                self.window.get_height() // 2 + 25
            )
        )

        self.draw_text_shadow(
            "ESC  Voltar ao menu",
            self.font,
            (255, 220, 0),
            (
                self.window.get_width() // 2,
                self.window.get_height() // 2 + 70
            )
        )

    def draw_victory_screen(self):
        if not self.level_completed:
            return

        self.draw_dark_overlay(200)

        self.draw_text_shadow(
            "VOCÊ VENCEU!",
            self.big_font,
            (255, 220, 0),
            (
                self.window.get_width() // 2,
                self.window.get_height() // 2 - 90
            ),
            (0, 0, 0),
            6
        )

        self.draw_text_shadow(
            "Todas as dificuldades foram concluídas!",
            self.font,
            (255, 255, 255),
            (
                self.window.get_width() // 2,
                self.window.get_height() // 2
            )
        )

        self.draw_text_shadow(
            "ESC  Voltar ao menu",
            self.font,
            (255, 220, 0),
            (
                self.window.get_width() // 2,
                self.window.get_height() // 2 + 60
            )
        )

    def draw_pause_menu(self):
        self.draw_dark_overlay(170)

        self.draw_text_shadow(
            "PAUSADO",
            self.big_font,
            (255, 255, 255),
            (
                self.window.get_width() // 2,
                self.window.get_height() // 2 - 140
            ),
            (0, 0, 0),
            5
        )

        pygame.draw.rect(
            self.window,
            (255, 180, 0),
            self.continue_button,
            border_radius=12
        )

        pygame.draw.rect(
            self.window,
            (180, 40, 40),
            self.exit_button,
            border_radius=12
        )

        continue_text = self.font.render(
            "Continuar",
            True,
            (0, 0, 0)
        )

        exit_text = self.font.render(
            "Sair para o menu",
            True,
            (255, 255, 255)
        )

        self.window.blit(
            continue_text,
            continue_text.get_rect(center=self.continue_button.center)
        )

        self.window.blit(
            exit_text,
            exit_text.get_rect(center=self.exit_button.center)
        )

    def handle_pause_click(self, mouse_pos):
        if self.continue_button.collidepoint(mouse_pos):
            self.paused = False

        if self.exit_button.collidepoint(mouse_pos):
            return "menu"

        return None

    def draw_game_world(self):
        self.window.fill((0, 0, 0))

        for ent in self.entity_list:
            self.window.blit(ent.surf, ent.rect)

        for chest in self.chests:
            self.window.blit(chest.surf, chest.rect)

        for flag in self.flags:
            flag.move()
            self.window.blit(flag.surf, flag.rect)

        for enemy in self.enemies:
            self.window.blit(enemy.surf, enemy.rect)
        map_area = pygame.Rect(
            0,
            0,
            self.window.get_width(),
            self.window.get_height()
        )

        for bullet in self.bullets:
            if map_area.colliderect(bullet.rect):
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

    def run(self):

        while True:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:

                        if self.game_over or self.level_completed:
                            return "menu"

                        self.paused = not self.paused

                    elif event.key == pygame.K_RETURN and self.game_over:
                        self.restart_game()

                    elif event.key == pygame.K_F1 and not self.game_over:
                        self.editor_mode = not self.editor_mode

                    elif event.key == pygame.K_s:
                        keys = pygame.key.get_pressed()

                        if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                            self.save_platforms()

                if self.paused and event.type == pygame.MOUSEBUTTONDOWN:

                    if event.button == 1:
                        pause_return = self.handle_pause_click(event.pos)

                        if pause_return == "menu":
                            return "menu"

                if self.editor_mode and not self.paused:
                    self.handle_editor_events(event)

            player = self.get_player()

            if self.paused:
                self.draw_game_world()
                self.draw_hud()
                self.draw_pause_menu()

                pygame.display.flip()
                self.clock.tick(60)
                continue

            if not self.game_over and not self.level_completed and not self.show_level_intro:

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

            self.draw_game_world()
            self.draw_hud()
            self.draw_level_intro()
            self.draw_game_over_screen()
            self.draw_victory_screen()

            pygame.display.flip()
            self.clock.tick(60)