import pygame
import os
import inspect

import catwars.helpers
import catwars.enemies

class Game():
    """Game specific class that wires all peces needed for the bame."""
    def __init__(self):
        self.options = catwars.helpers.Options()

        _dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
        self.assets_dir = os.path.join(_dir, "assets/")

        self.font = pygame.font.Font(os.path.join(self.assets_dir, "font/Pixeltype.ttf"), 50)
        self.score = 0

        # Groups
        self.enemies_group = catwars.enemies.EnemiesGroup()

    def draw(self, screen):
        screen.fill("darkgreen")

        score_surf = self.font.render(f"Score: {self.score}", False, (200, 50, 100))
        score_rect = score_surf.get_rect(center=(400, 50))
        screen.blit(score_surf, score_rect)

        self.enemies_group.draw(screen)

    def dispatch(self):
        """Iterate through events in the queue and makes sure all child
           entities have a chance to react to the events as well."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self._quit()

            if event.type == self.enemies_group.spawn_timer:
                self.enemies_group.add(catwars.enemies.Enemy(self))

            self.enemies_group.dispatch(event)

    def update(self):
        self.enemies_group.update()

    def _quit(self):
        pygame.quit()
        print(f"SCORE: {self.score}")
        sys.exit()