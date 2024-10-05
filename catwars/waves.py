import pygame
import os
import json

import catwars.enemies

class Waves():
    """Waves of enemies in level."""
    def __init__(self, game, data_path_rel):
        self.game = game

        # Load waves data
        data_path = os.path.join(self.game.assets_dir, data_path_rel)
        with open(data_path, "r") as fd:
            self._data = json.load(fd)
        self._index = 0

        self.wave_timer = pygame.event.custom_type()   # next waive
        self.burst_timer = pygame.event.custom_type()   # next burst in current waive

        self.handle_wave()

    def dispatch(self, event):
        if event.type == self.wave_timer:
            self.handle_wave()

        if event.type == self.burst_timer:
            self.handle_burst()

    def handle_wave(self):
        # Handle case during init when we are initializing group
        enemies_group_initializing = "enemies_group" not in dir(self.game)

        # No more waves available
        no_more_waves = self._index >= len(self._data)

        # If there are no enemies and there is no more waves, quit
        if not enemies_group_initializing:
            if len(self.game.enemies_group) == 0:
                if no_more_waves:
                    self.game.is_active = False
                    return

        # If we are still running and there are no more waves, just sleep
        if no_more_waves:
            config = {"type": "idle", "delay": 1}
        else:
            config = self._data[self._index]

        # Process the wave
        if config["type"] == "idle":
            pygame.time.set_timer(self.wave_timer, config["delay"] * 1000, loops=1)
            self.game.logger.debug(f"Starting idle wave {self._index} in {config['delay']} seconds")
            self._index += 1
        else:
            pygame.time.set_timer(self.burst_timer, int(config["delay"] * 1000), loops=config["bursts"])
            self.game.logger.debug(f"Starting burst wave {self._index} in {config['delay']} seconds")
            self._burst_counter = 0

    def handle_burst(self):
        config = self._data[self._index]
        self.game.logger.debug(f"Starting burst {self._burst_counter} of {config['bursts']} from wave {self._index}")
        for enemy, count in config["enemies"].items():
            for i in range(count):
                match enemy:
                    case "slime":
                        self.game.enemies_group.add(catwars.enemies.Slime(self.game))
                    case "bat":
                        self.game.enemies_group.add(catwars.enemies.Bat(self.game))
                    case "ghost":
                        self.game.enemies_group.add(catwars.enemies.Ghost(self.game))
                    case _:
                        raise Exception("Unsupported enemy type in wave config")
        self._burst_counter += 1
        if self._burst_counter == config["bursts"]:
            self._index += 1
            self.handle_wave()
