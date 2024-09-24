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
                "bursts": 1,
                "delay": 0.3,   # Delay between bursts
                "enemies": {
                    "slime": 1,   # Count in each burst
                },
            },
            {
                "type": "attack",
                "bursts": 1,
                "delay": 0.3,   # Delay between bursts
                "enemies": {
                    "slime": 1,   # Count in each burst
                },
            },
            {
                "type": "attack",
                "bursts": 2,
                "delay": 0.3,   # Delay between bursts
                "enemies": {
                    "bat": 2,   # Count in each burst
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
                    "ghost": 2,   # Count in each burst
                },
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
                    case "bat":
                        self.game.enemies_group.add(Bat(self.game))
                    case "ghost":
                        self.game.enemies_group.add(Ghost(self.game))
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

        # Spawn point
        spawn = self.game.world.convert_tiles_to_coord(*self.game.route[0])
        self.rect.topleft = spawn

        # Movement
        self.speed = 1
        self.direction = pygame.math.Vector2(0, 0)

        # Navigation
        self.target_index = 0
        self.update_target()

        # Defaults
        self.health = 0   # initial health value of the enemy, configured in specific class
        self.health_current = None   # current value of enemy health, if None, will be set based on self health on first use

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

        self.rect.center += self.direction * self.speed

        if self.rect.colliderect(self.target_rect):
            self.update_target()

    def draw(self, screen):
        # TODO: This is duplicated, figure out better way
        if self.health_current is None:
            self.health_current = self.health

        # Health bar
        rect = pygame.Rect(self.rect.x, self.rect.y - 5, 32, 5)
        pygame.draw.rect(screen, (0, 0, 0), rect, border_radius=2)
        width = self.health_current / self.health * 30
        rect = pygame.Rect(self.rect.x + 1, self.rect.y - 4, width, 3)
        pygame.draw.rect(screen, (255, 0, 0), rect, border_radius=2)

    def demage(self):
        # TODO: This is duplicated, figure out better way
        if self.health_current is None:
            self.health_current = self.health

        power = random.randint(2, 6)
        self.health_current -= power

        if self.health_current <= 0:
            self.deeead_sound.play()
            self.kill()
            self.game.score += 1
        else:
            self.demaaage_sound.play()

    def update_target(self):
        """Update target to next one and if there is no next, this enemy made it to the end."""
        self.target_index += 1

        try:
            # Select another step from the route
            target = self.game.route[self.target_index]
            self.target_rect = self.game.world.map[target.x][target.y].rect
            self.update_direction()
        except IndexError:
            # Enemy reached final target
            self.kill()
            self.game.score -= 3
            return

    def update_direction(self):
        """Update direction of this enamy."""
        start_vec = pygame.math.Vector2(self.rect.center)
        end_vec = pygame.math.Vector2(self.target_rect.center)
        self.direction = (end_vec - start_vec).normalize()
        if self.direction.x > self.direction.y and self.direction.y < 0:
            self.set_action("walk_north")
        if self.direction.x < self.direction.y and self.direction.x < 0:
            self.set_action("walk_west")
        if self.direction.x < self.direction.y and self.direction.y > 0:
            self.set_action("walk_south")
        if self.direction.x > self.direction.y and self.direction.x > 0:
            self.set_action("walk_east")


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

class Bat(Enemy):
    def __init__(self, game):
        spritesheet_path = "graphics/enemies/bat.png"
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
        self.speed = 7.5
        self.health = 5
        self.set_action("walk_east")

class Ghost(Enemy):
    def __init__(self, game):
        spritesheet_path = "graphics/enemies/ghost.png"
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
        self.speed = 5
        self.health = 25
        self.set_action("walk_east")
