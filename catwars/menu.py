import sys
import pygame

import catwars.helpers

class Menu:
    """Game specific class for menu."""

    def __init__(self, logger):
        self.logger = logger

        self.options = catwars.helpers.Options()
        pygame.display.set_mode(self.options.size)

        self.is_active = True

    def draw(self, screen):
        pass

    def dispatch(self, event):
        """Iterate through events in the queue and makes sure all child
        entities have a chance to react to the events as well."""
        pass

    def update(self):
        pass
