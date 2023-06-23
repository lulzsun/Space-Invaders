"""Scene objects for making games with PyGame."""

import os
import pygame
from videogame import rgbcolors
from videogame.sprites import Crab, Octopus, Player, Squid


# If you're interested in using abstract base classes, feel free to rewrite
# these classes.
# For more information about Python Abstract Base classes, see
# https://docs.python.org/3.8/library/abc.html


class Scene:
    """Base class for making PyGame Scenes."""

    def __init__(self,
                 screen: pygame.Surface,
                 soundtrack=None):
        """Scene initializer"""
        self._screen = screen
        self._frame_rate = 60
        self._is_valid = True
        self._soundtrack = soundtrack
        self._render_updates = None

    def draw(self):
        """Draw the scene."""
        self._screen = pygame.display.get_surface()
        self._screen.fill(rgbcolors.black)

    def process_event(self, event):
        """Process a game event by the scene."""
        if event.type == pygame.QUIT:
            print("Good Bye!")
            self._is_valid = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            print("Bye bye!")
            self._is_valid = False

    def is_valid(self):
        """Is the scene valid? A valid scene can be used to play a scene."""
        return self._is_valid

    def render_updates(self):
        """Render all sprite updates."""

    def update_scene(self):
        """Update the scene state."""

    def start_scene(self):
        """Start the scene."""
        if self._soundtrack:
            try:
                pygame.mixer.music.load(self._soundtrack)
                pygame.mixer.music.set_volume(0.2)
            except pygame.error as pygame_error:
                print("Cannot open the mixer?")
                print('\n'.join(pygame_error.args))
                raise SystemExit("broken!!") from pygame_error
            pygame.mixer.music.play(-1)

    def end_scene(self):
        """End the scene."""
        if self._soundtrack and pygame.mixer.music.get_busy():
            # Fade music out so there isn't an audible pop
            pygame.mixer.music.fadeout(500)
            pygame.mixer.music.stop()

    def frame_rate(self):
        """Return the frame rate the scene desires."""
        return self._frame_rate

class InvadersGameScene(Scene):
    """Scene with the actual gameplay of space invaders"""

    def __init__(self, screen, soundtrack=None):
        """Initialize the scene."""
        super().__init__(screen, soundtrack)
        self.player = Player()
        self.player_move = 0
        self.player_position_x = 0

    def process_event(self, event):
        """Process game events."""
        super().process_event(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a and self.player_move != -1:
                self.player_move = -1
            if event.key == pygame.K_d and self.player_move != 1:
                self.player_move = 1
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a and self.player_move == -1:
                self.player_move = 0
            if event.key == pygame.K_d and self.player_move == 1:
                self.player_move = 0

    def update_scene(self):
        """Update the scene state."""
        super().update_scene()
        self.player_position_x += self.player_move

    def draw(self):
        """Draw the scene."""
        super().draw()

        for i in range(11):
            Squid().draw(self._screen, (i*16 + 24, 64))

        for i in range(11):
            for j in range(2):
                Crab().draw(self._screen, (i*16 + 24, 64+16*(j+1)))

        for i in range(11):
            for j in range(2):
                Octopus().draw(self._screen, (i*16 + 24, 64+32+16*(j+1)))

        self.player.draw(self._screen, (self.player_position_x, 216))
