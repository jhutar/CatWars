#!/usr/bin/env python

import pygame
import sys
import random

class GroupWithDispatch(pygame.sprite.Group):
    def dispatch(self, event):
        for member in self:
            member.dispatch(event)

class EnemiesGroup(GroupWithDispatch):
    def __init__(self):
        super().__init__()

        self.spawn_timer = pygame.event.custom_type()
        pygame.time.set_timer(self.spawn_timer, 1000)

class Options():
    def __init__(self):
        self.width = 800
        self.height = 600

class Game(pygame.sprite.Sprite):
    def __init__(self, options):
        self.options = options
        self.font = pygame.font.Font("font/Pixeltype.ttf", 50)
        self.score = 0

        # Groups
        self.enemies_group = EnemiesGroup()

    def draw(self, screen):
        screen.fill("darkgreen")

        score_surf = self.font.render(f"Score: {self.score}", False, (200, 50, 100))
        score_rect = score_surf.get_rect(center=(400, 50))
        screen.blit(score_surf, score_rect)

        self.enemies_group.draw(screen)

    def dispatch(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                print(f"SCORE: {self.score}")   # TODO: Deduplicate
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    print(f"SCORE: {self.score}")   # TODO: Deduplicate
                    sys.exit()

            if event.type == self.enemies_group.spawn_timer:
                self.enemies_group.add(Enemy(game))

            self.enemies_group.dispatch(event)

    def update(self):
        self.enemies_group.update()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()

        # Refference to game data
        self.game = game

        # Sprite necessities
        self.image = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
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

options = Options()

pygame.init()
screen = pygame.display.set_mode((options.width, options.height))
pygame.display.set_caption("CatWars")
clock = pygame.time.Clock()
###bg_music = pygame.mixer.Sound("audio/music.wav")
###bg_music.play(loops=-1)

# Groups
game = Game(options)

# Main loop
while True:
    game.dispatch()
    game.draw(screen)
    game.update()

    pygame.display.update()
    clock.tick(30)
