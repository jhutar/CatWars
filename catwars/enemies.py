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

        self.animation_timer = pygame.event.custom_type()
        pygame.time.set_timer(self.animation_timer, 200)

    def draw(self,screen):
        super().draw(screen)
        for e in self:
            e.draw(screen)

    def dispatch(self, event):
        if event.type == self.spawn_timer:
            self.add(Enemy(self.game))

        super().dispatch(event)


class Enemy(pygame.sprite.Sprite):
    """Game specific enemy sprite class."""
    def __init__(self, game):
        super().__init__()

        # Refference to game data
        self.game = game

        # Sprite necessities
        self.images = []
        self.index = 0
        spritesheet_path = os.path.join(self.game.assets_dir, "graphics/enemies/slime.png")
        spritesheet = pygame.image.load(spritesheet_path).convert_alpha()
        for i in range(3):
            rect = pygame.Rect((i * 32, 0, 32, 32))
            image = pygame.Surface(rect.size).convert_alpha()
            image.blit(spritesheet, (0, 0), rect)
            image.set_colorkey((0,0,0))
            self.images.append(image)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (-30, 300)

        # Sounds
        sound_path = os.path.join(self.game.assets_dir, "audio/demage.mp3")
        self.demaaage_sound = pygame.mixer.Sound(sound_path)
        sound_path = os.path.join(self.game.assets_dir, "audio/dead.mp3")
        self.deeead_sound = pygame.mixer.Sound(sound_path)
        ###self.jump_sound.set_volume(0.5)

        # Entity properties
        self.health = 10

    def dispatch(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.demage()
                return

        if event.type == self.game.enemies_group.animation_timer:
            self.index += 1
            self.index = self.index % len(self.images)
            return

    def update(self):
        self.rect.x += 5

        self.image = self.images[self.index]

        if self.rect.x > self.game.options.width:
            self.kill()
            self.game.score -= 3

    def draw(self,screen):
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

