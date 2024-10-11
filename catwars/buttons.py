import pygame
import os.path

import catwars.generics


class ButtonsGroup(catwars.generics.GroupWithDispatch):
    """Generic group of UI buttons."""

    def __init__(self, game):
        super().__init__()

        self.game = game

        size = self.game.world.size
        self.build_button = Button(self.game, (0, size[1] - 100))
        self.add(self.build_button)


class Button(pygame.sprite.Sprite):
    """Generic button sprite class."""

    def __init__(self, game, topleft):
        super().__init__()

        self.game = game
        self.active = False

        # Sprite necessities
        img_path_idle = os.path.join(
            self.game.options.assets_dir, "graphics/ui/button-build-idle.png"
        )
        i = pygame.image.load(img_path_idle).convert_alpha()
        img_path_active = os.path.join(
            self.game.options.assets_dir, "graphics/ui/button-build-active.png"
        )
        self.images = {
            False: pygame.image.load(img_path_idle).convert_alpha(),
            True: pygame.image.load(img_path_active).convert_alpha(),
        }
        self.image = self.images[self.active]
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft

    def dispatch(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
                self.game.logger.debug("Clcked button")
                self.game.towers_group.stop_building()
                return True

    def update(self):
        self.image = self.images[self.active]
