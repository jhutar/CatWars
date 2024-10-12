import os
import inspect

class Options:
    """Game specific class just to wrap game settings."""

    def __init__(self):
        self.width = 1152
        self.height = 864
        self.size = (self.width, self.height)

        _dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
        self.assets_dir = os.path.join(_dir, "assets/")
