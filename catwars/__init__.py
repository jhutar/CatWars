#!/usr/bin/env python

import pygame

import catwars.logs
import catwars.ui


def play(logger):
    pygame.init()
    clock = pygame.time.Clock()

    ui = catwars.ui.UI(logger)

    # Main loop
    while True:
        for event in pygame.event.get():
            if not ui.is_active:
                break

            if event.type == pygame.QUIT:
                ui.is_active = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    ui.is_active = False

            ui.dispatch(event)

        ui.draw()
        ui.update()

        if not ui.is_active:
            break

        pygame.display.update()
        clock.tick(30)

    ui.level.score.print()
    pygame.quit()


def safe_play():
    logger = catwars.logs.setup_logger("CatWars")
    try:
        play(logger)
    except Exception as e:
        logger.exception(e)


if __name__ == "__main__":
    safe_play()
