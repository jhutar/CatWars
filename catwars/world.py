import pygame
import pytmx

class GroundTile(pygame.sprite.Sprite):
    """Generic ground sprite class for map tiles."""
    def __init__(self, image, topleft):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft


class World(pygame.sprite.Group):
    def __init__(self, level):
        super().__init__()

        self.tmxdata = pytmx.util_pygame.load_pygame(level)
        self.world_size = (
            self.tmxdata.width * self.tmxdata.tilewidth,
            self.tmxdata.height * self.tmxdata.tileheight,
        )

        for layer in self.tmxdata:
            if layer.name == "ground":
                for tile in layer.tiles():
                    x_top_left = tile[0] * self.tmxdata.tilewidth
                    y_top_left = tile[1] * self.tmxdata.tileheight
                    self.add(GroundTile(tile[2], (x_top_left, y_top_left)))
