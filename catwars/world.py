import pygame
import pytmx

class GroundTile(pygame.sprite.Sprite):
    """
    Generic ground sprite class for map tiles.

        Parameters:
            image (pygame.Surface): Image of a tile
            topleft (tuple): Position of top-left corner of the tile image on the screen
    """
    def __init__(self, image, topleft):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft


class World(pygame.sprite.Group):
    def __init__(self, level):
        super().__init__()

        self.tmxdata = pytmx.util_pygame.load_pygame(level)
        self.dimensions = (self.tmxdata.width, self.tmxdata.height)
        self.size = (
            self.tmxdata.width * self.tmxdata.tilewidth,
            self.tmxdata.height * self.tmxdata.tileheight,
        )

        for layer in self.tmxdata:
            if layer.name == "ground":
                for tile in layer.tiles():
                    x_top_left = tile[0] * self.tmxdata.tilewidth
                    y_top_left = tile[1] * self.tmxdata.tileheight
                    self.add(GroundTile(tile[2], (x_top_left, y_top_left)))

    def is_walkable(self, x, y):
        props = self.tmxdata.get_tile_properties(x, y, 0)
        if props is None:
            return False   # If no tile is specified in the map
        else:
            return props["can_walk"]

    def convert_tiles_to_coord(self, x_tiles, y_tiles):
        x = x_tiles * self.tmxdata.tilewidth
        y = y_tiles * self.tmxdata.tileheight
        return pygame.math.Vector2(x, y)
