#!/usr/bin/env python

import pygame
import sys
import random


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (0, 300)

    def update(self):
        self.move()

    def move(self):
        self.rect.x += 1

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("CatWars")
clock = pygame.time.Clock()
score = 0
game_font = pygame.font.Font("font/Pixeltype.ttf", 50)
###bg_music = pygame.mixer.Sound("audio/music.wav")
###bg_music.play(loops=-1)

# Groups
enemies_group = pygame.sprite.Group()

# Timers
spawn_timer = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_timer, 1000)
###animation_timer = pygame.USEREVENT + 2
###pygame.time.set_timer(animation_timer, 500)

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            for enemy in enemies_group:
                if enemy.rect.collidepoint(event.pos):
                    enemy.kill()
                    score += 1

        ###if event.type == animation_timer:
        ###    pass

        if event.type == spawn_timer:
            enemies_group.add(Enemy())

    screen.fill("darkgreen")

    score_surf = game_font.render(f"Score: {score}", False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)

    enemies_group.draw(screen)
    enemies_group.update()

    pygame.display.update()
    clock.tick(30)
