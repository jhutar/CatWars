#!/usr/bin/env python

import pygame
import os


class ProjectilesGroup(pygame.sprite.Group):
    """Game specific sprite group of projectiles shoot by towers."""
    def __init__(self, game):
        super().__init__()

        self.game = game

    def dispatch(self, event):
        pass


class Projectile(pygame.sprite.Sprite):
    """Game specific tower sprite class."""
    def __init__(self, game, tower, enemy):
        super().__init__()

        self.game = game
        self.tower = tower

        # Sprite necessities
        img_path = os.path.join(self.game.assets_dir, "graphics/projectile.png")
        self.image = pygame.image.load(img_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = self.tower.rect.center

        # Movement
        self.speed = 10
        start_vec = pygame.math.Vector2(self.rect.center)
        end_vec = pygame.math.Vector2(enemy.rect.center)
        self.direction = (end_vec - start_vec).normalize()

    def update(self):
        super().update()

        change = self.direction * self.speed
        self.rect.center += change

        # Did we hit some enemy?
        for enemy in self.game.enemies_group:
            if enemy.rect.collidepoint(self.rect.center):
                self.kill()
                enemy.demage()

        # Did we flew too far?
        distance = pygame.math.Vector2(self.rect.center).distance_to(self.tower.rect.center)
        if distance >= self.tower.range:
            self.kill()
