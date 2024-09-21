import pygame
import os
import random

import catwars.generics


class EnemiesGroup(catwars.generics.GroupWithDispatch):
    """Game specific sprite group of our enemies, also configures timers related to enemies."""
    def __init__(self, game):
        super().__init__()

        self.game = game

        self.spawn_timer = pygame.event.custom_type()
        pygame.time.set_timer(self.spawn_timer, 1000)

    def draw(self,screen):
        super().draw(screen)
        for e in self:
            e.draw(screen)

    def dispatch(self, event):
        if event.type == self.spawn_timer:
            self.add(Slime(self.game))

        super().dispatch(event)


class Enemy(catwars.generics.AnimatedSprite):
    """Game specific enemy sprite class."""
    def __init__(self, game, spritesheet_path, spritesheet_size, spritesheet_config):
        super().__init__(game, spritesheet_path, spritesheet_size, spritesheet_config)

        self.rect.center = (-30, 300)

        # Sounds
        sound_path = os.path.join(self.game.assets_dir, "audio/demage.mp3")
        self.demaaage_sound = pygame.mixer.Sound(sound_path)
        sound_path = os.path.join(self.game.assets_dir, "audio/dead.mp3")
        self.deeead_sound = pygame.mixer.Sound(sound_path)
        ###self.jump_sound.set_volume(0.5)

    def dispatch(self, event):
        super().dispatch(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.demage()
                return

    def update(self):
        super().update()

        self.rect.x += self.speed

        if self.rect.x > self.game.options.width:
            self.kill()
            self.game.score -= 3

    def draw(self, screen):
        # Health bar
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(self.rect.x, self.rect.y + 100, self.health * 6.5, 5))

    def demage(self):
        power = random.randint(2, 6)
        self.health -= power
        if self.health <= 0:
            self.deeead_sound.play()
            self.kill()
            self.game.score += 1
        else:
            self.demaaage_sound.play()


class Slime(Enemy):
    def __init__(self, game):
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

        super().__init__(game, spritesheet_path, spritesheet_size, spritesheet_config)

        # Properties
        self.speed = 3
        self.health = 10
        self.set_action("walk_east")
