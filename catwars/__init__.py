#!/usr/bin/env python

import pygame

import catwars.flow

def play():
    pygame.init()
    clock = pygame.time.Clock()

    game = catwars.flow.Game()

    screen = pygame.display.set_mode((game.options.width, game.options.height))
    pygame.display.set_caption("CatWars")

    # Main loop
    while True:
        game.dispatch()
        game.draw(screen)
        game.update()

        pygame.display.update()
        clock.tick(30)

if __name__ == "__main__":
    play()