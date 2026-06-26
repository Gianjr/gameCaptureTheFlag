#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from Code.bullet import Bullet


class Enemy:

    def __init__(self, position):
        self.name = "enemy"

        self.width = 66
        self.height = 66

        self.frames = [
            pygame.image.load("./assets/enemy/Attack/sprite_0.png").convert_alpha(),
            pygame.image.load("./assets/enemy/Attack/sprite_1.png").convert_alpha(),
            pygame.image.load("./assets/enemy/Attack/sprite_2.png").convert_alpha(),
            pygame.image.load("./assets/enemy/Attack/sprite_3.png").convert_alpha()
        ]

        self.frames = [
            pygame.transform.scale(frame, (self.width, self.height))
            for frame in self.frames
        ]

        self.frame = 0
        self.animation_speed = 0.12

        self.surf = self.frames[0]
        self.rect = self.surf.get_rect(topleft=position)

        # Se a imagem estiver virada errada, troque este valor:
        # True  = inverte a imagem
        # False = mantém normal
        self.invert_sprite = True

        self.facing_right = False

        self.last_shot_time = 0

        # Será alterado pelo Level conforme a dificuldade
        self.shoot_delay = 1600
        self.bullet_speed = 4
        self.bullet_color = (255, 220, 0)

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

            bullet = Bullet(
                self.rect.centerx,
                self.rect.centery,
                player.rect.centerx,
                player.rect.centery,
                self.bullet_speed,
                self.bullet_color
            )

            bullets.append(bullet)

        self.animate()

    def move(self):
        pass