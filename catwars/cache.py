import os
import copy
import pygame

import catwars.helpers


class Cache:
    _cache = {}

    def __init__(self, logger):
        self.logger = logger
        self.options = catwars.helpers.Options()

    def load_image(self, image_file):
        cid = (image_file,)
        if cid in self._cache:
            self.logger.debug(f"Returning image {cid} from cache")
            return copy.copy(self._cache[cid])
        else:
            self.logger.debug(f"Loading image {cid} to cache")
            image_path = os.path.join(self.options.assets_dir, image_file)
            image = pygame.image.load(image_path).convert_alpha()
            self._cache[cid] = image
            return copy.copy(image)

    def load_font(self, font_file, size):
        cid = (font_file, size)
        if cid in self._cache:
            self.logger.debug(f"Returning font {cid} from cache")
            return self._cache[cid]
        else:
            self.logger.debug(f"Loading font {cid} to cache")
            font_path = os.path.join(self.options.assets_dir, font_file)
            font = pygame.font.Font(font_path, size)
            self._cache[cid] = font
            return font
        
