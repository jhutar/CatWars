#!/usr/bin/env python

import pygame
import os


class ProjectilesGroup(pygame.sprite.Group):
    """Game specific sprite group of projectiles shoot by towers."""

    def __init__(self, level):
        super().__init__()

        self.level = level

    def dispatch(self, event):
        pass


class Projectile(pygame.sprite.Sprite):
    """Game specific tower sprite class."""

    def __init__(self, level, tower, enemy):
        super().__init__()

        self.level = level
        self.tower = tower

        # Sprite necessities
        self.image = self.level.cache.load_image("graphics/projectile.png")
        self.rect = self.image.get_rect()
        self.rect.center = self.tower.rect.center

        # Movement
        self.speed = 10
        start_vec = pygame.math.Vector2(self.rect.center)
        end_vec = pygame.math.Vector2(enemy.rect.center)
        self.direction = (end_vec - start_vec).normalize()

        # Rotate projectile to match direction
        rotation = pygame.math.Vector2(0, -1).angle_to(self.direction)
        self.image = pygame.transform.rotate(self.image, -1 * rotation)

    def update(self):
        super().update()

        change = self.direction * self.speed
        self.rect.center += change

        # Did we hit some enemy?
        for enemy in self.level.enemies_group:
            if enemy.rect.collidepoint(self.rect.center):
                self.kill()
                enemy.demage()
                self.level.logger.debug("Projectile hit enemy")

        # Did we flew too far?
        distance = pygame.math.Vector2(self.rect.center).distance_to(
            self.tower.rect.center
        )
        if distance >= self.tower.range:
            self.kill()
            self.level.logger.debug("Projectile missed")
