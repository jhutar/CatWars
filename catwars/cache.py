import os
import pygame

import catwars.helpers


class Cache:
    _cache = {}

    def __init__(self, logger):
        self.logger = logger
        self.options = catwars.helpers.Options()

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
        
