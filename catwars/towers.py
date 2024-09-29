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
                print(f"Considering building tower on {event.pos} -> {colrow}")
                self.considered_tower = Tower(self.game, self.game.world.map[colrow[0]][colrow[1]].rect.topleft)
            if event.type == pygame.MOUSEBUTTONDOWN:
                for tile in self.game.world:
                    if tile.rect.collidepoint(event.pos):
                        self.add(Tower(self.game, tile.rect.topleft))
                        #print(f"Adding tower to {tile.rect.topleft}")

    def draw(self, screen):
        super().draw(screen)

        if self.considered_tower is not None:
            screen.blit(self.considered_tower, self.considered_tower.rect)

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
    def __init__(self, game, topleft):
        super().__init__()

        self.game = game

        # Properties
        self.range = 300

        # Sprite necessities
        img_path = os.path.join(self.game.assets_dir, "graphics/tower.png")
        self.image = pygame.image.load(img_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft
