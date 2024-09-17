import pygame
import os
import inspect
import sys

import catwars.helpers
import catwars.world
import catwars.enemies
import catwars.towers

class Game():
    """Game specific class that wires all peces needed for the bame."""
    def __init__(self):
        self.options = catwars.helpers.Options()

        _dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
        self.assets_dir = os.path.join(_dir, "assets/")

        self.font = pygame.font.Font(os.path.join(self.assets_dir, "font/Pixeltype.ttf"), 50)
        self.score = 0

        # World
        self.world = catwars.world.World(os.path.join(self.assets_dir, "tileset/CatWars-level1.tmx"))

        # Groups
        self.enemies_group = catwars.enemies.EnemiesGroup(self)
        self.towers_group = catwars.towers.TowersGroup(self)

    def draw(self, screen):
        self.world.draw(screen)

        score_surf = self.font.render(f"Score: {self.score}", False, (200, 50, 100))
        score_rect = score_surf.get_rect(center=(400, 50))
        screen.blit(score_surf, score_rect)

        self.enemies_group.draw(screen)

        self.towers_group.draw(screen)

    def dispatch(self):
        """Iterate through events in the queue and makes sure all child
           entities have a chance to react to the events as well."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self._quit()

            self.enemies_group.dispatch(event)
            self.towers_group.dispatch(event)

    def update(self):
        self.enemies_group.update()

    def _quit(self):
        pygame.quit()
        print(f"SCORE: {self.score}")
        sys.exit()
