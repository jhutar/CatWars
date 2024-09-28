import pygame
import pytmx

class GroundTile(pygame.sprite.Sprite):
    """
    Generic ground sprite class for map tiles.

        Parameters:
            image (pygame.Surface): Image of a tile
            topleft (tuple): Position of top-left corner of the tile image on the screen
    """
    def __init__(self, image, topleft, colrow, props):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft
        self.colrow = colrow
        self.props = props


class World(pygame.sprite.Group):
    def __init__(self, level):
        super().__init__()

        tmxdata = pytmx.util_pygame.load_pygame(level)
        self.dimensions = (tmxdata.width, tmxdata.height)
        self.tilesize = (tmxdata.tilewidth, tmxdata.tileheight)
        self.size = (
            tmxdata.width * tmxdata.tilewidth,
            tmxdata.height * tmxdata.tileheight,
        )
        self.starts = []   # tiles where to spawn enemies
        self.ends = []   # tiles enemies want to reach

        # Construct datastructure that will be populated by all tiles
        self.map = []
        for c in range(self.dimensions[0]):
            col = []
            for r in range(self.dimensions[1]):
                col.append(None)
            self.map.append(col)

        # Create all the tiles and add them to the group and also to the map for easier refference
        for layer in tmxdata:
            if layer.name == "ground":
                for tile in layer.tiles():
                    topleft = self.convert_tiles_to_coord(tile[0], tile[1])
                    props = tmxdata.get_tile_properties(tile[0], tile[1], 0)
                    tile_obj = GroundTile(tile[2], topleft, (tile[0], tile[1]), props)
                    self.add(tile_obj)   # adding tile sprite to the group
                    self.map[tile[0]][tile[1]] = tile_obj   # adding tile to the map

        # Load waypoints
        for obj in tmxdata.objects:
            if obj.name == "start":
                tile_coords = self.convert_coords_to_tiles(obj.x, obj.y)
                tile = self.map[tile_coords[0]][tile_coords[1]]
                self.starts.append(tile)
            if obj.name == "end":
                tile_coords = self.convert_coords_to_tiles(obj.x, obj.y)
                tile = self.map[tile_coords[0]][tile_coords[1]]
                self.ends.append(tile)

    def is_walkable(self, x, y):
        props = self.map[x][y].props
        if props is None:
            return False   # If no tile is specified in the map
        else:
            return props["can_walk"]

    def convert_tiles_to_coord(self, column, row):
        """Convert (column, row) tile spec on the map to (x, y) in pixels on the map."""
        x = column * self.tilesize[0]
        y = row * self.tilesize[1]
        return pygame.math.Vector2(x, y)

    def convert_coords_to_tiles(self, x, y):
        """Convert (x, y) in pixels on the map to (column, row) tile spec on the map."""
        column = int(x // self.tilesize[0])
        row = int(y // self.tilesize[1])
        return (column, row)
