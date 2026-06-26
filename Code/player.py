#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from Code.entity import Entity


class Player(Entity):

    def __init__(self, position):
        super().__init__("player/Biker_idle/sprite_0", position)

        self.speed = 4

        self.gravity = 0.7
        self.jump_force = -14
        self.velocity_y = 0

        self.on_ground = False

        # evita pulo infinito segurando ↑
        self.jump_pressed = False

        self.facing_right = True

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

        self.frame = 0
        self.animation_speed = 0.18

        self.state = "idle"

        self.surf = self.idle[0]

    def animate(self):

        self.frame += self.animation_speed

        if self.state == "idle":

            if self.frame >= len(self.idle):
                self.frame = 0

            image = self.idle[int(self.frame)]

        elif self.state == "run":

            if self.frame >= len(self.run):
                self.frame = 0

            image = self.run[int(self.frame)]

        else:

            if self.frame >= len(self.jump):
                self.frame = 0

            image = self.jump[int(self.frame)]

        if not self.facing_right:
            image = pygame.transform.flip(image, True, False)

        self.surf = image

    def update(self, platforms):

        keys = pygame.key.get_pressed()

        moving = False

        # esquerda
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            moving = True
            self.facing_right = False

        # direita
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            moving = True
            self.facing_right = True

        # pulo apenas quando aperta
        if keys[pygame.K_UP]:

            if not self.jump_pressed:

                self.jump_pressed = True

                if self.on_ground:
                    self.velocity_y = self.jump_force
                    self.on_ground = False

        else:
            self.jump_pressed = False

        self.velocity_y += self.gravity

        if self.velocity_y > 12:
            self.velocity_y = 12

        self.rect.y += self.velocity_y

        self.on_ground = False

        for platform in platforms:

                if (
                    self.rect.colliderect(platform.rect)
                    and self.velocity_y >= 0
                    and self.rect.bottom - self.velocity_y <= platform.rect.top + 8
                ):

                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.on_ground = True

        # animações

        if not self.on_ground:

            self.state = "jump"

        elif moving:

            if self.state != "run":
                self.frame = 0

            self.state = "run"

        else:

            if self.state != "idle":
                self.frame = 0

            self.state = "idle"

        self.animate()

    def move(self):
        pass