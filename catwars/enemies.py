import pygame
import os
import random

import catwars.generics


class EnemiesGroup(catwars.generics.GroupWithDispatch):
    """Game specific sprite group of our enemies, also configures timers related to enemies."""
    def __init__(self):
        super().__init__()

        self.spawn_timer = pygame.event.custom_type()
        pygame.time.set_timer(self.spawn_timer, 1000)


class Enemy(pygame.sprite.Sprite):
    """Game specific enemy sprite class."""
    def __init__(self, game):
        super().__init__()

        # Refference to game data
        self.game = game

        # Sprite necessities
        img_path = os.path.join(self.game.assets_dir, "graphics/player/player_walk_1.png")
        self.image = pygame.image.load(img_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (-30, 300)

        # Entity properties
        self.health = 10

    def dispatch(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.demage()

    def update(self):
        self.rect.x += 5

        if self.rect.x > self.game.options.width:
            self.kill()
            self.game.score -= 3

    def demage(self):
        power = random.randint(2, 6)
        self.health -= power
        if self.health <= 0:
            self.kill()
            self.game.score += 1

