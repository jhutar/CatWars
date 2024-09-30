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

        if self.game.buttons_group.build_button.active:
            if event.type == pygame.MOUSEMOTION:
                colrow = self.game.world.convert_coords_to_tiles(*event.pos)
                topleft = self.game.world.convert_tiles_to_coord(*colrow)
                self.considered_tower = Tower(self.game, topleft, considered=True)

            if event.type == pygame.MOUSEBUTTONDOWN:
                colrow = self.game.world.convert_coords_to_tiles(*event.pos)
                topleft = self.game.world.convert_tiles_to_coord(*colrow)
                if self.considered_tower.considered_possible:
                    self.add(Tower(self.game, topleft))

    def draw(self, screen):
        super().draw(screen)

        if self.considered_tower is not None:
            self.considered_tower.draw(screen)

    def consider_placing(self):
        pass

    def consider_shooting(self):
        for tower in self:
            closest_enemy = None
            closest_enemy_distance = None
            for enemy in self.game.enemies_group:
                distance = pygame.math.Vector2(tower.rect.x, tower.rect.y).distance_to((enemy.rect.x, enemy.rect.y))

                # Check if enemy is not out of range
                if distance > tower.range:
                    continue

                # If this is first enemy, use it
                if closest_enemy is None:
                    closest_enemy = enemy
                    closest_enemy_distance = distance
                    continue

                # If this is closes enemy we got
                if distance < closest_enemy_distance:
                    closest_enemy = enemy
                    closest_enemy_distance = distance

            # If some enemy was found
            if closest_enemy is not None:
                #print(f"Closes enemy to tower {tower} is {closest_enemy} with distance {closest_enemy_distance}")
                projectile = catwars.projectiles.Projectile(self.game, tower, closest_enemy)
                self.game.projectiles_group.add(projectile)


class Tower(pygame.sprite.Sprite):
    """Game specific tower sprite class."""
    def __init__(self, game, topleft, considered=False):
        super().__init__()

        self.game = game

        # Properties
        self.range = 300

        # Considered tower properties
        self.considered = considered
        self.considered_possible = False

        # Sprite necessities
        img_path = os.path.join(self.game.assets_dir, "graphics/tower.png")
        self.image = pygame.image.load(img_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft

        # If this is just a considered tower
        if self.considered:
            self.image.set_alpha(191)

    def draw(self, screen, unable=[]):
        """This is only used when drawing considered tower during choosing place."""
        possible = True
        colrow = self.game.world.convert_coords_to_tiles(*self.rect.topleft)
        for c in range(2):
            for r in range(2):
                rect = pygame.Rect(c * 32, r * 32, 32, 32)
                surf = self.image.subsurface(rect)
                not_buildable = not self.game.world.can_build(colrow[0] + c, colrow[1] + r)
                rect.x += self.rect.x
                rect.y += self.rect.y
                collides = rect.collidelist([t.rect for t in self.game.towers_group]) != -1
                if not_buildable or collides:
                    surf.fill("red", special_flags=pygame.BLEND_RGBA_MIN)
                    possible = False
                screen.blit(surf, rect)
        self.considered_possible = possible
