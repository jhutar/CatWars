import pygame
import os
import random

import catwars.generics


class Waves():
    """Waves of enemies in level."""
    def __init__(self, game):
        self._data = [
            {
                "type": "attack",
                "bursts": 2,
                "delay": 0.3,   # Delay between bursts
                "enemies": {
                    "slime": 2,   # Count in each burst
                },
            },
            {
                "type": "idle",
                "delay": 3,
            },
            {
                "type": "attack",
                "bursts": 2,
                "delay": 0.6,   # Delay between bursts
                "enemies": {
                    "slime": 2,   # Count in each burst
                },
            },
            {
                "type": "idle",
                "delay": 10,
            },
        ]
        self._index = 0

        self.game = game
        self.wave_timer = pygame.event.custom_type()   # next waive
        self.burst_timer = pygame.event.custom_type()   # next burst in current waive

        self.handle_wave()

    def dispatch(self, event):
        if event.type == self.wave_timer:
            self.handle_wave()

        if event.type == self.burst_timer:
            self.handle_burst()

    def handle_wave(self):
        config = self._data[self._index]
        if config["type"] == "idle":
            pygame.time.set_timer(self.wave_timer, config["delay"] * 1000, loops=1)
            self._index += 1
        else:
            pygame.time.set_timer(self.burst_timer, int(config["delay"] * 1000), loops=config["bursts"])
            self._burst_counter = 0

    def handle_burst(self):
        config = self._data[self._index]
        for enemy, count in config["enemies"].items():
            for i in range(count):
                match enemy:
                    case "slime":
                        self.game.enemies_group.add(Slime(self.game))
                    case _:
                        raise Exception("Unsupported enemy type in wave config")
        self._burst_counter += 1
        if self._burst_counter == config["bursts"]:
            self._index += 1
            self.handle_wave()

class EnemiesGroup(catwars.generics.GroupWithDispatch):
    """Game specific sprite group of our enemies, also configures timers related to enemies."""
    def __init__(self, game):
        super().__init__()

        self.game = game
        self.waves = Waves(self.game)

    def draw(self,screen):
        super().draw(screen)
        for e in self:
            e.draw(screen)

    def dispatch(self, event):
        self.waves.dispatch(event)

        super().dispatch(event)


class Enemy(catwars.generics.AnimatedSprite):
    """Game specific enemy sprite class."""
    def __init__(self, game, spritesheet_path, spritesheet_size, spritesheet_config):
        super().__init__(game, spritesheet_path, spritesheet_size, spritesheet_config)

        self.rect.center = (-30, 300)

        # Sounds
        sound_path = os.path.join(self.game.assets_dir, "audio/demage.mp3")
        self.demaaage_sound = pygame.mixer.Sound(sound_path)
        sound_path = os.path.join(self.game.assets_dir, "audio/dead.mp3")
        self.deeead_sound = pygame.mixer.Sound(sound_path)
        ###self.jump_sound.set_volume(0.5)

    def dispatch(self, event):
        super().dispatch(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.demage()
                return

    def update(self):
        super().update()

        self.rect.x += self.speed

        if self.rect.x > self.game.options.width:
            self.kill()
            self.game.score -= 3

    def draw(self, screen):
        # Health bar
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(self.rect.x, self.rect.y + 100, self.health * 6.5, 5))

    def demage(self):
        power = random.randint(2, 6)
        self.health -= power
        if self.health <= 0:
            self.deeead_sound.play()
            self.kill()
            self.game.score += 1
        else:
            self.demaaage_sound.play()


class Slime(Enemy):
    def __init__(self, game):
        spritesheet_path = "graphics/enemies/slime.png"
        spritesheet_size = (32, 32)
        spritesheet_config = [
            {
                "action": "walk_north",
                "order": [0, 1, 2, 1],
            },
            {
                "action": "walk_west",
                "order": [0, 1, 2, 1],
            },
            {
                "action": "walk_south",
                "order": [0, 1, 2, 1],
            },
            {
                "action": "walk_east",
                "order": [0, 1, 2, 1],
            },
        ]

        super().__init__(game, spritesheet_path, spritesheet_size, spritesheet_config)

        # Properties
        self.speed = 3
        self.health = 10
        self.set_action("walk_east")
