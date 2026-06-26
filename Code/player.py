#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from Code.entity import Entity


class Player(Entity):

    def __init__(self, position):
        super().__init__("player/Biker_idle/sprite_0", position)

        self.speed = 2

        # Física
        self.velocity_y = 0
        self.gravity = 0.8
        self.jump_force = -16
        self.on_ground = False

        # Direção
        self.facing_right = True

        # Animações
        self.idle = [
            pygame.image.load("./assets/player/Biker_idle/sprite_0.png").convert_alpha(),
            pygame.image.load("./assets/player/Biker_idle/sprite_1.png").convert_alpha(),
            pygame.image.load("./assets/player/Biker_idle/sprite_2.png").convert_alpha(),
            pygame.image.load("./assets/player/Biker_idle/sprite_3.png").convert_alpha()
        ]

        self.run = [
            pygame.image.load("./assets/player/Biker_run/sprite_0.png").convert_alpha(),
            pygame.image.load("./assets/player/Biker_run/sprite_1.png").convert_alpha(),
            pygame.image.load("./assets/player/Biker_run/sprite_2.png").convert_alpha(),
            pygame.image.load("./assets/player/Biker_run/sprite_3.png").convert_alpha(),
            pygame.image.load("./assets/player/Biker_run/sprite_4.png").convert_alpha(),
            pygame.image.load("./assets/player/Biker_run/sprite_5.png").convert_alpha()
        ]

        self.jump = [
            pygame.image.load("./assets/player/Biker_jump/sprite_0.png").convert_alpha(),
            pygame.image.load("./assets/player/Biker_jump/sprite_1.png").convert_alpha(),
            pygame.image.load("./assets/player/Biker_jump/sprite_2.png").convert_alpha(),
            pygame.image.load("./assets/player/Biker_jump/sprite_3.png").convert_alpha()
        ]

        self.state = "idle"
        self.frame = 0
        self.animation_speed = 0.20

        self.surf = self.idle[0]

    def get_current_frame(self):
        if self.state == "idle":
            image = self.idle[int(self.frame)]

        elif self.state == "run":
            image = self.run[int(self.frame)]

        elif self.state == "jump":
            image = self.jump[int(self.frame)]

        else:
            image = self.idle[0]

        if not self.facing_right:
            image = pygame.transform.flip(image, True, False)

        return image

    def animate(self):
        self.frame += self.animation_speed

        if self.state == "idle":
            if self.frame >= len(self.idle):
                self.frame = 0

        elif self.state == "run":
            if self.frame >= len(self.run):
                self.frame = 0

        elif self.state == "jump":
            if self.frame >= len(self.jump):
                self.frame = 0

        self.surf = self.get_current_frame()

    def update(self, platforms):
        keys = pygame.key.get_pressed()

        moving = False

        # Movimento para esquerda
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.facing_right = False
            moving = True

        # Movimento para direita
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.facing_right = True
            moving = True

        # Pulo com seta para cima
        if keys[pygame.K_UP] and self.on_ground:
            self.velocity_y = self.jump_force
            self.on_ground = False

        # Gravidade
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        # Colisão vertical
        self.on_ground = False

        for plat in platforms:
            if self.rect.colliderect(plat.rect):

                # Caindo em cima da plataforma
                if self.velocity_y > 0:
                    self.rect.bottom = plat.rect.top
                    self.velocity_y = 0
                    self.on_ground = True

                # Batendo a cabeça por baixo
                elif self.velocity_y < 0:
                    self.rect.top = plat.rect.bottom
                    self.velocity_y = 0

        # Estado da animação
        if not self.on_ground:
            self.state = "jump"
        elif moving:
            self.state = "run"
        else:
            self.state = "idle"

        self.animate()

    def move(self):
        pass