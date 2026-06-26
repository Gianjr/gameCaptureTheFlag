#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import random
from Code.bullet import Bullet


class Enemy:

    def __init__(self, position):
        self.name = "enemy"

        self.width = 66
        self.height = 66

        self.frames = self.load_frames()

        self.frame = 0
        self.animation_speed = 0.10

        self.surf = self.frames[0]
        self.rect = self.surf.get_rect(topleft=position)

        self.invert_sprite = True
        self.facing_right = False

        self.last_shot_time = 0

        self.shoot_delay = 1700
        self.bullet_speed = 3
        self.bullet_color = (255, 220, 0)

    def load_frames(self):
        frames = []

        possible_paths = [
            "./assets/enemy/Attack/sprite_{}.png",
            "./assets/enemy/Idle/sprite_{}.png",
            "./assets/enemy/Enemy_idle/sprite_{}.png",
            "./assets/enemy/Soldier_idle/sprite_{}.png",
        ]

        for i in range(4):
            image_loaded = None

            for path in possible_paths:
                try:
                    image_loaded = pygame.image.load(
                        path.format(i)
                    ).convert_alpha()
                    break
                except:
                    pass

            if image_loaded is None:
                image_loaded = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
                pygame.draw.rect(image_loaded, (120, 0, 180), (10, 10, 76, 76))
                pygame.draw.rect(image_loaded, (255, 255, 255), (30, 30, 12, 12))
                pygame.draw.rect(image_loaded, (255, 255, 255), (55, 30, 12, 12))

            image_loaded = pygame.transform.scale(
                image_loaded,
                (self.width, self.height)
            )

            frames.append(image_loaded)

        return frames

    def set_difficulty(self, shoot_delay, bullet_speed, bullet_color):
        self.shoot_delay = shoot_delay
        self.bullet_speed = bullet_speed
        self.bullet_color = bullet_color

    def animate(self):
        self.frame += self.animation_speed

        if self.frame >= len(self.frames):
            self.frame = 0

        image = self.frames[int(self.frame)]

        should_flip = self.facing_right

        if self.invert_sprite:
            should_flip = not should_flip

        if should_flip:
            image = pygame.transform.flip(image, True, False)

        self.surf = image

    def update(self, player, bullets):
        if player.rect.centerx > self.rect.centerx:
            self.facing_right = True
        else:
            self.facing_right = False

        now = pygame.time.get_ticks()

        if now - self.last_shot_time >= self.shoot_delay:
            self.last_shot_time = now

            # Pequena variação para o tiro não ficar sempre igual
            aim_offset_x = random.randint(-25, 25)
            aim_offset_y = random.randint(-20, 20)

            bullet = Bullet(
                self.rect.centerx,
                self.rect.centery,
                player.rect.centerx + aim_offset_x,
                player.rect.centery + aim_offset_y,
                self.bullet_speed,
                self.bullet_color
            )

            bullets.append(bullet)

        self.animate()

    def move(self):
        pass