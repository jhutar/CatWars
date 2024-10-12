import pygame
import os
import random

import catwars.generics


class EnemiesGroup(catwars.generics.GroupWithDispatch):
    """Game specific sprite group of our enemies, also configures timers related to enemies."""

    def __init__(self, level):
        super().__init__()

        self.level = level

    def draw(self, screen):
        super().draw(screen)
        for e in self:
            e.draw(screen)

    def dispatch(self, event):
        self.level.waves.dispatch(event)

        super().dispatch(event)


class Enemy(catwars.generics.AnimatedSprite):
    """Game specific enemy sprite class."""

    def __init__(self, level, spritesheet_path, spritesheet_size, spritesheet_config):
        super().__init__(level, spritesheet_path, spritesheet_size, spritesheet_config)

        # Select my route
        self.route = random.choice(self.level.routes)

        # Spawn point
        spawn = pygame.math.Vector2(self.route[0].rect.center)
        self.rect.topleft = spawn + (random.randint(-8, 8), random.randint(-8, 8))

        # Movement
        self.speed = 1
        self.direction = pygame.math.Vector2(0, 0)

        # Navigation
        self.target_index = 0
        self.update_target()

        # Defaults
        self.health = (
            0  # initial health value of the enemy, configured in specific class
        )
        self.health_current = None  # current value of enemy health, if None, will be set based on self health on first use

        # Sounds
        sound_path = os.path.join(self.level.options.assets_dir, "audio/demage.mp3")
        self.demaaage_sound = pygame.mixer.Sound(sound_path)
        sound_path = os.path.join(self.level.options.assets_dir, "audio/dead.mp3")
        self.deeead_sound = pygame.mixer.Sound(sound_path)
        ###self.jump_sound.set_volume(0.5)

        self.level.logger.debug("Instantiated enemy {spritesheet_path}")

    def dispatch(self, event):
        super().dispatch(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.demage()
                return

    def update(self):
        super().update()

        change = self.direction * self.speed
        new_center = self.rect.center + change

        # Detect if we are coliding with some other enemy
        for e in self.level.enemies_group:
            if e == self:
                continue
            if (e.rect.center - new_center).length() < 8:
                new_center += (random.randint(-4, 4), random.randint(-4, 4))
                break
        self.rect.center = new_center
        self.update_direction()

        # If we reached another waypoint
        if self.rect.colliderect(self.target_rect):
            self.update_target()

    def draw(self, screen):
        # TODO: This is duplicated, figure out better way
        if self.health_current is None:
            self.health_current = self.health

        # Health bar
        rect = pygame.Rect(self.rect.x, self.rect.y - 5, 32, 5)
        pygame.draw.rect(screen, (0, 0, 0), rect, border_radius=2)
        width = self.health_current / self.health * 30
        rect = pygame.Rect(self.rect.x + 1, self.rect.y - 4, width, 3)
        pygame.draw.rect(screen, (255, 0, 0), rect, border_radius=2)

    def demage(self):
        # TODO: This is duplicated, figure out better way
        if self.health_current is None:
            self.health_current = self.health

        power = random.randint(2, 6)
        self.health_current -= power

        if self.health_current <= 0:
            self.deeead_sound.play()
            self.kill()
            self.level.score += 1
        else:
            self.demaaage_sound.play()

    def update_target(self):
        """Update target to next one and if there is no next, this enemy made it to the end."""
        self.target_index += 1

        try:
            # Select another step from the route
            self.target_rect = self.route[self.target_index].rect
            self.update_direction()
        except IndexError:
            # Enemy reached final target
            self.kill()
            self.level.score -= 3
            return

    def update_direction(self):
        """Update direction of this enamy."""
        start_vec = pygame.math.Vector2(self.rect.center)
        end_vec = pygame.math.Vector2(self.target_rect.center)
        self.direction = (end_vec - start_vec).normalize()
        if self.direction.x > self.direction.y and self.direction.y < 0:
            self.set_action("walk_north")
        if self.direction.x < self.direction.y and self.direction.x < 0:
            self.set_action("walk_west")
        if self.direction.x < self.direction.y and self.direction.y > 0:
            self.set_action("walk_south")
        if self.direction.x > self.direction.y and self.direction.x > 0:
            self.set_action("walk_east")


class Slime(Enemy):
    def __init__(self, level):
        spritesheet_path = "graphics/enemies/slime.png"
        spritesheet_size = (32, 32)
        spritesheet_config = [
            {
                "action": "walk_north",
                "order": [0, 1, 2, 1],
            },
            {
                "action": "walk_west",
                "order": [0, 1, 2, 1],
            },
            {
                "action": "walk_south",
                "order": [0, 1, 2, 1],
            },
            {
                "action": "walk_east",
                "order": [0, 1, 2, 1],
            },
        ]

        super().__init__(level, spritesheet_path, spritesheet_size, spritesheet_config)

        # Properties
        self.speed = 3
        self.health = 10
        self.set_action("walk_east")


class Bat(Enemy):
    def __init__(self, level):
        spritesheet_path = "graphics/enemies/bat.png"
        spritesheet_size = (32, 32)
        spritesheet_config = [
            {
                "action": "walk_north",
                "order": [0, 1, 2, 1],
            },
            {
                "action": "walk_west",
                "order": [0, 1, 2, 1],
            },
            {
                "action": "walk_south",
                "order": [0, 1, 2, 1],
            },
            {
                "action": "walk_east",
                "order": [0, 1, 2, 1],
            },
        ]

        super().__init__(level, spritesheet_path, spritesheet_size, spritesheet_config)

        # Properties
        self.speed = 7.5
        self.health = 5
        self.set_action("walk_east")


class Ghost(Enemy):
    def __init__(self, level):
        spritesheet_path = "graphics/enemies/ghost.png"
        spritesheet_size = (32, 32)
        spritesheet_config = [
            {
                "action": "walk_north",
                "order": [0, 1, 2, 1],
            },
            {
                "action": "walk_west",
                "order": [0, 1, 2, 1],
            },
            {
                "action": "walk_south",
                "order": [0, 1, 2, 1],
            },
            {
                "action": "walk_east",
                "order": [0, 1, 2, 1],
            },
        ]

        super().__init__(level, spritesheet_path, spritesheet_size, spritesheet_config)

        # Properties
        self.speed = 5
        self.health = 25
        self.set_action("walk_east")
