import os
import sys
import inspect

class Options:
    """Game specific class just to wrap game settings."""

    def __init__(self):
        self.width = 1152
        self.height = 864
        self.size = (self.width, self.height)

        # If this is running in pyInstaller, sys._MEIPASS is set and we need
        # to load data from there from "catwars/". If running directly in dev
        # mode, just use current file diractory as a starting point.
        # https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile
        _dir = getattr(sys, '_MEIPASS', None)
        if _dir is None:
            _dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
        else:
            _dir = os.path.join(_dir, "catwars/")
        self.assets_dir = os.path.join(_dir, "assets/")
