import pygame
import os
import inspect
import sys

import catwars.logs
import catwars.helpers
import catwars.world
import catwars.enemies
import catwars.towers
import catwars.projectiles
import catwars.buttons
import catwars.pathfinding
import catwars.waves


class Countdown():
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(os.path.join(self.game.assets_dir, "font/Pixeltype.ttf"), 50)

    def draw(self, screen):
        if self.game.waves.next_wave_in is not None:
            now = pygame.time.get_ticks()
            wave_in = self.game.waves.next_wave_in * 1000 - (now - self.game.waves.next_wave_started)
            score_surf = self.font.render(f"Next wave: {(wave_in/1000):.0f}", False, "black")
            score_rect = score_surf.get_rect(topleft=(20, 20))
            screen.blit(score_surf, score_rect)


class Score():
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(os.path.join(self.game.assets_dir, "font/Pixeltype.ttf"), 50)
        self.score = 0

    def __iadd__(self, other):
        self.score += other
        self.game.logger.debug(f"Increades score by {other} to {self.score}")
        return self

    def __isub__(self, other):
        self.score -= other
        self.game.logger.debug(f"Decreades score by {other} to {self.score}")
        return self

    def draw(self, screen):
        score_surf = self.font.render(f"Paws: {self.score}", False, "black")
        size = self.game.world.size
        score_rect = score_surf.get_rect(bottomleft=(80, size[1] - 50))
        screen.blit(score_surf, score_rect)

    def print(self):
        print(f"SCORE: {self.score}")


class Game():
    """Game specific class that wires all peces needed for the bame."""
    def __init__(self, logger):
        self.logger = logger
        self.logger.info("Welcome in CatWars!")

        self.options = catwars.helpers.Options()

        _dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
        self.assets_dir = os.path.join(_dir, "assets/")

        self.is_active = True

        # World
        self.world = catwars.world.World(self, "levels/level1.tmx")
        self.waves = catwars.waves.Waves(self, "levels/level1.json")

        # User interface
        self.score = Score(self)
        self.countdown = Countdown(self)

        # Paths
        pathfinding = catwars.pathfinding.Pathfinding(self)
        self.routes = []
        for start_tile in self.world.starts:
            for end_tile in self.world.ends:
                start = start_tile.colrow
                end = end_tile.colrow
                route = pathfinding.find(start, end)
                self.routes.append(route)

        # Timer for animations
        self.animation_timer = pygame.event.custom_type()
        pygame.time.set_timer(self.animation_timer, 200)

        # Groups
        self.enemies_group = catwars.enemies.EnemiesGroup(self)
        self.towers_group = catwars.towers.TowersGroup(self)
        self.projectiles_group = catwars.projectiles.ProjectilesGroup(self)
        self.buttons_group = catwars.buttons.ButtonsGroup(self)

    def draw(self, screen):
        self.world.draw(screen)
        self.enemies_group.draw(screen)
        self.towers_group.draw(screen)
        self.projectiles_group.draw(screen)
        self.buttons_group.draw(screen)
        self.countdown.draw(screen)
        self.score.draw(screen)

    def dispatch(self):
        """Iterate through events in the queue and makes sure all child
           entities have a chance to react to the events as well."""
        for event in pygame.event.get():
            if not self.is_active:
                self._quit()

            if event.type == pygame.QUIT:
                self._quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self._quit()

            # If this returns True, it means nobody else needs to process the event now
            if self.buttons_group.dispatch(event):
                continue
            if self.enemies_group.dispatch(event):
                continue
            if self.towers_group.dispatch(event):
                continue

    def update(self):
        self.enemies_group.update()
        self.towers_group.update()
        self.projectiles_group.update()
        self.buttons_group.update()

    def _quit(self):
        self.logger.info("Game ended")
        pygame.quit()
        self.score.print()
        sys.exit()
