#!/usr/bin/env python

import pygame
import os


class TowersGroup(pygame.sprite.Group):
    """Game specific sprite group of our towers."""
    def __init__(self, game):
        super().__init__()

        self.game = game

        ###self.spawn_timer = pygame.event.custom_type()
        ###pygame.time.set_timer(self.spawn_timer, 1000)

    def dispatch(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for tile in self.game.world:
                if tile.rect.collidepoint(event.pos):
                    self.add(Tower(self.game, tile.rect.topleft))


class Tower(pygame.sprite.Sprite):
    """Game specific tower sprite class."""
    def __init__(self, game, topleft):
        super().__init__()

        self.game = game

        # Sprite necessities
        img_path = os.path.join(self.game.assets_dir, "graphics/tower.png")
        self.image = pygame.image.load(img_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft
