"""Game objects to create PyGame based games."""

import os
from typing import List
import warnings

import pygame
import pygame._sdl2 as sdl2

from videogame.scene import CreditScene, InvadersGameScene, Scene, TitleScene


def display_info():
    """Print out information about the display driver and video information."""
    print(f'The display is using the "{pygame.display.get_driver()}" driver.')
    print("Video Info:")
    print(pygame.display.Info())


# If you're interested in using abstract base classes, feel free to rewrite
# these classes.
# For more information about Python Abstract Base classes, see
# https://docs.python.org/3.8/library/abc.html


class VideoGame:
    """Base class for creating PyGame games."""

    def __init__(
        self,
        window_width=224,
        window_height=256,
        window_title="My Awesome Game",
    ):
        """Initialize a new game with the given window size and title."""
        pygame.init()
        self._window_size = (window_width, window_height)
        self._clock = pygame.time.Clock()
        self._screen = pygame.display.set_mode(self._window_size, pygame.SCALED | pygame.RESIZABLE)

        initial_scale_factor = 3  # <-- adjustable
        window = sdl2.Window.from_display_module()
        window.size = (window_width * initial_scale_factor, window_height * initial_scale_factor)
        window.position = sdl2.WINDOWPOS_CENTERED
        window.show()

        self._title = window_title
        pygame.display.set_caption(self._title)

        if not pygame.font:
            warnings.warn("Fonts disabled.", RuntimeWarning)
        if not pygame.mixer:
            warnings.warn("Sound disabled.", RuntimeWarning)
        self._scene_graph = None


class SpaceInvadersGame(VideoGame):
    """The bread and butter of the operation. The game."""

    def __init__(self):
        """Init the Pygame demo."""
        super().__init__(window_title="1978 Space Invaders")
        self._main_dir = os.path.dirname(__file__)
        self._data_dir = os.path.join(os.path.dirname(__file__), 'data')
        print(f"Our main directory is {self._main_dir}")
        print(f"Our data directory is {self._data_dir}")
        self.build_scene_graph()

    def build_scene_graph(self):
        """Build scene graph for the game demo."""
        screen = pygame.display.get_surface()
        self._scene_graph: List[Scene]
        self._scene_graph = [
            CreditScene(screen),
            TitleScene(screen),
            InvadersGameScene(screen)
        ]

    def run(self):
        """Run the game; the main game loop."""
        scene_iterator = iter(self._scene_graph)
        current_scene = next(scene_iterator)
        while True:
            current_scene.start_scene()
            while current_scene.is_valid():
                self._clock.tick(current_scene.frame_rate())
                for event in pygame.event.get():
                    current_scene.process_event(event)
                current_scene.update_scene()
                current_scene.draw()
                current_scene.render_updates()
                pygame.display.update()
            while not current_scene.end_scene() and not current_scene._is_exiting:
                self._clock.tick(current_scene.frame_rate())
                for event in pygame.event.get():
                    Scene(self._screen).process_event(event)
                pygame.display.update()
            if current_scene.is_exiting():
                break
            current_scene = next(scene_iterator)
        pygame.quit()
        return 0
