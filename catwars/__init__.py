#!/usr/bin/env python

import pygame

import catwars.logs
import catwars.menu
import catwars.flow


def play(logger):
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((1, 1), pygame.HIDDEN)

    is_active = True

    ###menu = catwars.menu.Menu(logger)
    game = catwars.flow.Game(logger)

    screen = pygame.display.get_surface()
    pygame.display.set_caption("CatWars")

    # Main loop
    while True:
        for event in pygame.event.get():
            ###if not self.menu.is_active:
            ###    break

            if event.type == pygame.QUIT:
                is_active = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    is_active = False

            ###menu.dispatch(event)
            game.dispatch(event)

        ###menu.draw(screen)
        ###menu.update()
        game.draw(screen)
        game.update()

        if not game.is_active:
            is_active = False

        if is_active:
            pygame.display.update()
            clock.tick(30)
        else:
            break

    pygame.quit()


def safe_play():
    logger = catwars.logs.setup_logger("CatWars")
    try:
        play(logger)
    except Exception as e:
        logger.exception(e)


if __name__ == "__main__":
    safe_play()
