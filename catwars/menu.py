import sys
import os
import pygame

import catwars.generics
import catwars.helpers
import catwars.cache


class MenuGroup(catwars.generics.GroupWithDispatch):
    """Game specific class for menu."""

    def __init__(self, logger):
        super().__init__()

        self.logger = logger

        self.cache = catwars.cache.Cache(self.logger)

        # What should UI do
        #   active ... menu is on the screen
        #   go ... level should be started
        self.what_now = "active"

        self.add(MenuButton(self, True))

    def update(self):
        pass

class MenuButton(pygame.sprite.Sprite):
    def __init__(self, menu_group, is_active):
        super().__init__()

        self.is_active = is_active

        self.menu_group = menu_group

        self.font = self.menu_group.cache.load_font("font/Pixeltype.ttf", 50)

        # Sprite necessities
        self.rect = pygame.Rect((100, 100), (300, 100))
        self.image = pygame.Surface(self.rect.size).convert_alpha()

        pygame.draw.rect(self.image, "blue", pygame.Rect(0, 0, 300, 100), border_radius=10)
        pygame.draw.rect(self.image, "gray", pygame.Rect(3, 3, 294, 94), border_radius=10)
        score_surf = self.font.render("Start", False, "white")
        score_rect = score_surf.get_rect(center=(150, 50))
        self.image.blit(score_surf, score_rect)

    def dispatch(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.menu_group.what_now = "go"
                return
