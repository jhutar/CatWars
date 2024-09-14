#!/usr/bin/env python

import pygame
import sys
import random

class Options():
    def __init__(self):
        self.width = 800
        self.height = 600

class Game(pygame.sprite.Sprite):
    def __init__(self, options):
        self.options = options
        self.font = pygame.font.Font("font/Pixeltype.ttf", 50)
        self.score = 0

    def draw(self, screen):
        score_surf = self.font.render(f"Score: {self.score}", False, (200, 50, 100))
        score_rect = score_surf.get_rect(center=(400, 50))
        screen.blit(score_surf, score_rect)

    def dispatch(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            print(f"SCORE: {self.score}")   # TODO: Deduplicate
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                print(f"SCORE: {self.score}")   # TODO: Deduplicate
                sys.exit()

    def update(self):
        pass

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
enemies_group = pygame.sprite.Group()

# Timers
spawn_timer = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_timer, 1000)
###animation_timer = pygame.USEREVENT + 2
###pygame.time.set_timer(animation_timer, 500)

# Main loop
while True:
    for event in pygame.event.get():
        game.dispatch(event)

        for enemy in enemies_group:
            enemy.dispatch(event)

        ###if event.type == animation_timer:
        ###    pass

        if event.type == spawn_timer:
            enemies_group.add(Enemy(game))


    screen.fill("darkgreen")

    game.draw(screen)

    enemies_group.draw(screen)
    enemies_group.update()

    pygame.display.update()
    clock.tick(30)
