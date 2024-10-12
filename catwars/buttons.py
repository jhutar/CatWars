import pygame
import os.path

import catwars.generics


class ButtonsGroup(catwars.generics.GroupWithDispatch):
    """Generic group of UI buttons."""

    def __init__(self, level):
        super().__init__()

        self.level = level

        self.build_button = Button(
            self.level,
            (0, self.level.world.size[1] - 100),
            "graphics/ui/button-build-idle.png",
            "graphics/ui/button-build-active.png",
            self.level.towers_group.start_building,
            self.level.towers_group.stop_building,
        )
        self.add(self.build_button)


class Button(pygame.sprite.Sprite):
    """Generic button sprite class."""

    def __init__(self, level, topleft, image_idle, image_active, trigger_activate, trigger_deactivate):
        super().__init__()

        self.level = level
        self.active = False

        self.trigger_activate = trigger_activate
        self.trigger_deactivate = trigger_deactivate

        # Sprite necessities
        img_path_idle = os.path.join(self.level.options.assets_dir, image_idle)
        img_path_active = os.path.join(self.level.options.assets_dir, image_active)
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
                if self.active:
                    self.trigger_deactivate()
                else:
                    self.trigger_activate()
                self.active = not self.active
                self.level.logger.debug("Clicked button")
                return True

    def update(self):
        self.image = self.images[self.active]
