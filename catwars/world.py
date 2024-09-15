import pytmx

class World():
    def __init__(self, level):
        self.tmxdata = pytmx.util_pygame.load_pygame(level)
        self.world_size = (
            self.tmxdata.width * self.tmxdata.tilewidth,
            self.tmxdata.height * self.tmxdata.tileheight,
        )

    def draw(self, screen):
        for layer in self.tmxdata:
            if layer.name == "ground":
                for tile in layer.tiles():
                    x_top_left = tile[0] * self.tmxdata.tilewidth
                    y_top_left = tile[1] * self.tmxdata.tileheight
                    screen.blit(tile[2], (x_top_left, y_top_left))
