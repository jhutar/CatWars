#!/usr/bin/env python

import pygame

import catwars.logs
import catwars.flow

def play(logger):
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((1, 1))

    game = catwars.flow.Game(logger)

    screen = pygame.display.set_mode(game.world.size)
    pygame.display.set_caption("CatWars")

    # Main loop
    while True:
        game.dispatch()
        game.draw(screen)
        game.update()

        pygame.display.update()
        clock.tick(30)

def safe_play():
    logger = catwars.logs.setup_logger("CatWars")
    try:
        play(logger)
    except Exception as e:
        logger.exception(e)

if __name__ == "__main__":
    safe_play()
