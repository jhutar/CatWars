import pygame
import os.path

import catwars.generics


class ButtonsGroup(catwars.generics.GroupWithDispatch):
    """Generic group of UI buttons."""

    def __init__(self, level):
        super().__init__()

        self.level = level

        self.build_button = ButtonToggle(
            self.level,
            (0, self.level.world.size[1] - 100),
            "graphics/ui/button-build-idle.png",
            "graphics/ui/button-build-active.png",
            self.level.towers_group.start_building,
            self.level.towers_group.stop_building,
        )
        self.add(self.build_button)

        self.skip_button = ButtonOneshot(
            self.level,
            (72, self.level.world.size[1] - 100),
            "graphics/ui/button-skip-idle.png",
            "graphics/ui/button-skip-active.png",
            self.level.waves.skip_to_wave,
        )
        self.add(self.skip_button)


class ButtonToggle(pygame.sprite.Sprite):
    """Generic button sprite class you can click to activate and then click to deactivate."""

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
            False: self.level.cache.load_image(image_idle),
            True: self.level.cache.load_image(image_active),
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


class ButtonOneshot(pygame.sprite.Sprite):
    """Generic button sprite class you can simply click to trigger action."""

    def __init__(self, level, topleft, image_idle, image_active, trigger_activate):
        super().__init__()

        self.level = level
        self.active = False

        self.trigger_activate = trigger_activate

        self.animation_timer = pygame.event.custom_type()

        # Sprite necessities
        img_path_idle = os.path.join(self.level.options.assets_dir, image_idle)
        img_path_active = os.path.join(self.level.options.assets_dir, image_active)
        self.images = {   # TODO: Once upon a time this should be animated, so we need two buttons
            False: self.level.cache.load_image(image_idle),
            True: self.level.cache.load_image(image_active),
        }
        self.image = self.images[self.active]
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft

    def dispatch(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.trigger_activate()
                pygame.time.set_timer(self.animation_timer, 100, loops=1)
                self.level.logger.debug("Clicked button")
                self.active = True
                return True

        if event.type == self.animation_timer:
            self.active = False

    def update(self):
        self.image = self.images[self.active]
