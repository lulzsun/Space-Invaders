# Jimmy Quach
# jminquach@csu.fullerton.edu
# @lulzsun
"""Game objects to create PyGame based games."""

import os
import warnings

import pygame
import pygame._sdl2 as sdl2

from videogame.scene import (
    ControlsScene, CreditScene, InvadersGameScene,
    LeaderboardScene, Scene, TitleScene
)


class SpaceInvadersGame():
    """The bread and butter of the operation. The game."""

    def __init__(self):
        """Init the game."""
        pygame.init()
        window_width = 224
        window_height = 256
        self._window_size = (window_width, window_height)
        self._clock = pygame.time.Clock()
        self._screen = pygame.display.set_mode(
            self._window_size, pygame.SCALED | pygame.RESIZABLE
        )

        initial_scale_factor = 3  # <-- adjustable
        window = sdl2.Window.from_display_module()
        window.size = (
            window_width * initial_scale_factor,
            window_height * initial_scale_factor
        )
        window.position = sdl2.WINDOWPOS_CENTERED
        window.show()

        pygame.display.set_caption("1978 Space Invaders")

        if not pygame.font:
            warnings.warn("Fonts disabled.", RuntimeWarning)
        if not pygame.mixer:
            warnings.warn("Sound disabled.", RuntimeWarning)
        self._scene_graph = None

        self._main_dir = os.path.dirname(__file__)
        self._data_dir = os.path.join(os.path.dirname(__file__), 'data')
        print(f"Our main directory is {self._main_dir}")
        print(f"Our data directory is {self._data_dir}")
        self.build_scene_graph()

    def build_scene_graph(self):
        """Build scene graph for the game demo."""
        self._scene_graph = [
            CreditScene(self._screen),  # i have no idea but
            ControlsScene,              # without this, we
            TitleScene,                 # would get seg faults...
            InvadersGameScene,
            LeaderboardScene,
        ]

    def run(self):
        """Run the game; the main game loop."""
        index = 0
        current_scene = self._scene_graph[0]
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
            while (not current_scene.end_scene()
                   and not current_scene.is_exiting):
                self._clock.tick(current_scene.frame_rate())
                for event in pygame.event.get():
                    Scene(self._screen).process_event(event)
                pygame.display.update()
            if current_scene.is_exiting:
                break

            hi_score = 0
            if isinstance(current_scene, InvadersGameScene):
                hi_score = current_scene.p1_score

            if isinstance(current_scene, LeaderboardScene):
                index = 1
            index += 1
            current_scene = self._scene_graph[index](self._screen)
            if isinstance(current_scene, LeaderboardScene):
                current_scene.hi_score = hi_score
        pygame.quit()
        return 0
