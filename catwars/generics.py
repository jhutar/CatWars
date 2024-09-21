import os
import pygame

class GroupWithDispatch(pygame.sprite.Group):
    """Generic sprite group that supports dispatch method."""
    def dispatch(self, event):
        """Process given event by all members of the group. Returns True when some member decides nobody else needs to process the event now."""
        for member in self:
            if member.dispatch(event):
                return True


class SpriteSheet():
    """Generic wrapper around spritesheet for character."""
    def __init__(self, path, size, config):
        """
        Load spritesheet of a character. Spritesheet have different actions
        in rows (heading north, heading east...) and animation frames in
        columns and you can specify number of frames.

            Parameters:
                path (string): Path to PNG file to load spritesheet from
                size (touple): Width and height of single sprite in the sheet
                confg (dict): Describes individual rows of the spritesheet

            Example config for spritesheet with 4 x 2 sprites:

                [
                    {
                        "action": "swing_sword",
                        "count": 3,   # optional, defaults to all of them
                        "order": [0, 1, 2, 1],   # optional, defaults to order in spritesheet
                    },
                    {
                        "action": "swing_axe",
                    },
                ]

                action (string): Just a name of the action, describing what is animated in given row of the spritesheet
                count (int): Optional, says how many columns should be loaded in case trailing columns are empty
                order (list): Option, to be used if you want to rearange frames of the animation and not use images as they follow in columns
        """
        spritesheet = pygame.image.load(path).convert_alpha()
        spritesheet_rect = spritesheet.get_rect()
        spritesheet_columns = int(spritesheet_rect.width / size[0])
        spritesheet_rows = int(spritesheet_rect.height / size[1])

        self._images = {}
        for row, action in zip(range(len(config)), config):
            # How many images we are going to load from the row
            if "count" in action:
                count = int(action["count"])
                assert count <= spritesheet_columns, f"Requested count for {action['action']} is less or equal to what we have"
            else:
                count = spritesheet_columns

            images_action = []

            # Split row in the spritesheet
            for column in range(count):
                rect = pygame.Rect((column * size[0], row * size[1], size[0], size[1]))
                image = pygame.Surface(rect.size).convert_alpha()
                image.blit(spritesheet, (0, 0), rect)
                image.set_colorkey((0, 0, 0))
                images_action.append(image)

            # Rearange if requested
            if "order" in action:
                self._images[action["action"]] = []
                for i in action["order"]:
                    self._images[action["action"]].append(images_action[i])
            else:
                self._images[action["action"]] = images_action

    def get_image(self, action, index):
        return self._images[action][index]

    def next_index(self, action, index):
        index += 1
        return index % len(self._images[action])


class AnimatedSprite(pygame.sprite.Sprite):
    """Generic animated sprite class."""
    def __init__(self, game, path, size, config):
        super().__init__()

        self.game = game

        # Load spritesheet
        path2 = os.path.join(self.game.assets_dir, path)
        self.spritesheet = SpriteSheet(path2, size, config)

        # Defaults
        self._index = 0
        self._action = config[0]["action"]

        # Sprite necesities
        self.image = self.spritesheet.get_image(self._action, self._index)
        self.rect = self.image.get_rect()

    def dispatch(self, event):
        if event.type == self.game.animation_timer:
            self._index = self.spritesheet.next_index(self._action, self._index)

    def update(self):
        self.image = self.spritesheet.get_image(self._action, self._index)

    def set_action(self, action):
        self._action = action
