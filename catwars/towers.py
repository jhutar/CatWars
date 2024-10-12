#!/usr/bin/env python

import pygame
import os

import catwars.projectiles


class TowersGroup(pygame.sprite.Group):
    """Game specific sprite group of our towers."""

    def __init__(self, game):
        super().__init__()

        self.game = game

        self.shoot_timer = pygame.event.custom_type()
        pygame.time.set_timer(self.shoot_timer, 1000)

        self.considered_tower = None

    def dispatch(self, event):
        if event.type == self.shoot_timer:
            self.consider_shooting()

        if self.considered_tower is not None:
            if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN:
                self.considered_tower.update_position(event.pos)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.considered_tower.considered_possible:
                    self.considered_tower.considered = False
                    self.add(self.considered_tower)
                    self.start_building()   # create new considered tower as this one was built

    def draw(self, screen):
        super().draw(screen)

        if self.considered_tower is not None:
            self.considered_tower.draw(screen)

    def consider_shooting(self):
        for tower in self:
            closest_enemy = None
            closest_enemy_distance = None
            for enemy in self.game.enemies_group:
                distance = pygame.math.Vector2(tower.rect.x, tower.rect.y).distance_to(
                    (enemy.rect.x, enemy.rect.y)
                )

                # Check if enemy is not out of range
                if distance > tower.range:
                    continue

                # If this is first enemy, use it
                if closest_enemy is None:
                    closest_enemy = enemy
                    closest_enemy_distance = distance
                    continue

                # If this is closest enemy we got
                if distance < closest_enemy_distance:
                    closest_enemy = enemy
                    closest_enemy_distance = distance

            # If some enemy was found
            if closest_enemy is not None:
                self.game.logger.debug(f"Closes enemy to tower {tower} is {closest_enemy} with distance {closest_enemy_distance}")
                projectile = catwars.projectiles.Projectile(
                    self.game, tower, closest_enemy
                )
                self.game.projectiles_group.add(projectile)

    def start_building(self):
        """Create considered tower, used when we enter build phase or so."""
        self.considered_tower = ArrowTower(self.game, (0, 0), considered=False)

    def stop_building(self):
        """Annulate considered tower, used when we exit build phase or so."""
        self.considered_tower = None


class Tower(pygame.sprite.Sprite):
    """Game specific tower sprite class."""

    def __init__(self, game, topleft, spritesheet_path, considered=False):
        super().__init__()

        self.game = game

        # Properties configured in specific tower class
        # self.price = 1
        # self.range = 300

        # Considered tower properties
        self.considered = considered
        self.considered_possible = False
        self.considered_tiles = []

        # Sprite necessities
        self.img_path = os.path.join(self.game.options.assets_dir, spritesheet_path)
        self.image = pygame.image.load(self.img_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft

        # If this is just a considered tower
        if self.considered:
            self.image.set_alpha(191)

        if not self.considered:
            self.game.score -= self.price
            self.game.logger.debug(f"Built tower on {self.rect.topleft}")

    def draw(self, screen):
        """This is only used when drawing considered tower during choosing place."""
        for tilespec in self.considered_tiles:
            screen.blit(*tilespec)

    def update_position(self, xy):
        """This is only used when finding locatoin for considered tower."""
        colrow = self.game.world.convert_coords_to_tiles(*xy)
        topleft = self.game.world.convert_tiles_to_coord(*colrow)
        self.rect.topleft = topleft

        self.image = pygame.image.load(self.img_path).convert_alpha()

        possible = True
        self.considered_tiles = []
        colrow = self.game.world.convert_coords_to_tiles(*self.rect.topleft)
        for c in range(2):
            for r in range(2):
                rect = pygame.Rect(c * 32, r * 32, 32, 32)
                surf = self.image.subsurface(rect)
                try:
                    not_buildable = not self.game.world.can_build(
                        colrow[0] + c, colrow[1] + r
                    )
                except catwars.world.OutOfMap:
                    not_buildable = True
                rect.x += self.rect.x
                rect.y += self.rect.y
                tower_rects = [t.rect for t in self.game.towers_group]
                collides = rect.collidelist(tower_rects) != -1
                if not_buildable or collides:
                    surf.fill("red", special_flags=pygame.BLEND_RGBA_MIN)
                    possible = False
                self.considered_tiles.append((surf, rect))
        self.considered_possible = possible

class ArrowTower(Tower):
    def __init__(self, game, topleft, considered=False):
        # Properties
        self.price = 1
        self.range = 300

        spritesheet_path = "graphics/tower2.png"
        super().__init__(game, topleft, spritesheet_path, considered)
