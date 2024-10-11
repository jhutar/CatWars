import os
import inspect

class Options:
    """Game specific class just to wrap game settings."""

    def __init__(self):
        self.width = 800
        self.height = 600
        self.size = (self.width, self.height)

        _dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
        self.assets_dir = os.path.join(_dir, "assets/")
