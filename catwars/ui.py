import pygame

import catwars.menu
import catwars.flow


class UI:
    """Game specific class for overall UI."""

    def __init__(self, logger):
        self.logger = logger

        self.is_active = True

        self.options = catwars.helpers.Options()
        self.screen = pygame.display.set_mode(self.options.size)
        pygame.display.set_caption("CatWars")

        self.menu = catwars.menu.MenuGroup(logger)
        self.level = catwars.flow.Level(logger)

    def draw(self):
        if self.menu.what_now == "active":
            self.menu.draw(self.screen)
        elif self.menu.what_now == "go":
            self.level.draw(self.screen)
        else:
            raise Exception("What to do?")

    def dispatch(self, event):
        if self.menu.what_now == "active":
            self.menu.dispatch(event)
        elif self.menu.what_now == "go":
            self.level.dispatch(event)
        else:
            raise Exception("What to do?")

    def update(self):
        if self.menu.what_now == "active":
            self.menu.update()
        elif self.menu.what_now == "go":
            self.level.update()
            if not self.level.is_active:
                self.is_active = False
        else:
            raise Exception("What to do?")
