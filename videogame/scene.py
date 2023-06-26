"""Scene objects for making games with PyGame."""

import os
from typing import List
import pygame
from videogame.sprites import (
    Alien, Bullet, Shield, Crab, Font, 
    Octopus, Player, Squid
)


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
        self._screen.fill("black")

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
        self.secret = False

        self.frames = 0
        self.player = Player()

        self.shields: List[Shield]
        self.shields = []

        self.aliens: List[Alien]
        self.aliens = []
        self.alien_move = 1
        self.alien_position_x = 0
        self.alien_position_y = 0
        self.alien_move_frame = 0

        self.bullets: List[Bullet]
        self.bullets = []

        for i in range(4):
            self.shields.append(Shield((31+(31*(i*1.5)), 192)))

        for i in range(11):
            self.aliens.append(Squid((i*16 + 24, 64)))

        for i in range(11):
            for j in range(2):
                self.aliens.append(Crab((i*16 + 24, 64+16*(j+1))))

        for i in range(11):
            for j in range(2):
                self.aliens.append(Octopus((i*16 + 24, 64+32+16*(j+1))))

    def process_event(self, event):
        """Process game events."""
        super().process_event(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.secret = not self.secret

        self.player.move(event)
        self.player.shoot(event)

    def update_scene(self):
        """Update the scene state."""
        self.frames += 1
        super().update_scene()

        if self.player.shooting:
            # make sure player only has 1 bullet on screen
            if not any(bullet.is_player_owned is True for bullet in self.bullets):
                self.bullets.append(Bullet((self.player.position_x+7, 211), is_player_owned=True))

        # Update alien(s) position
        if self.alien_position_x == 0:
            if self.frames % (2 * self.frame_rate()) == 0:
                self.alien_position_x = len(self.aliens)

        if self.aliens[0]._position[0] == 24 + 16:
            if self.alien_move != -1:
                self.alien_position_y = len(self.aliens)
                self.alien_move = -1
        elif self.aliens[0]._position[0] == 16:
            if self.alien_move != 1:
                self.alien_position_y = len(self.aliens)
                self.alien_move = 1

        for bullet in self.bullets:
            # move bullets
            position = bullet._position
            if bullet._explode_frame == 0:
                position = bullet.move((0, -4))
            else:
                done = bullet.explode()
                if done:
                    self.bullets.remove(bullet)
                continue

            if position[1] < 34:
                if bullet._explode_frame == 0:
                    bullet.move((0, 4))
                bullet.explode()

            # bullet collision check
            for alien in self.aliens:
                if alien.is_colliding(bullet):
                    self.bullets.remove(bullet)
                    self.aliens.remove(alien)

            for shield in self.shields:
                if shield.is_colliding(bullet):
                    bullet.explode()
                    # TODO: implement shield damage
                    continue

    def render_updates(self):
        """Render additional screen updates."""
        super().render_updates()
        # create a color overlay in certain areas of the screen
        # this mimics 1978 space invaders coloring
        overlay_rect = pygame.Surface((self._screen.get_width(), 32), pygame.SRCALPHA)
        overlay_rect.fill((254, 30, 30))
        self._screen.blit(overlay_rect, (0, 32), special_flags=pygame.BLEND_RGB_MULT)

        overlay_rect = pygame.Surface((self._screen.get_width(), 56), pygame.SRCALPHA)
        overlay_rect.fill((30, 254, 30))
        self._screen.blit(overlay_rect, (0, 184), special_flags=pygame.BLEND_RGB_MULT)

        overlay_rect = pygame.Surface((111, 16), pygame.SRCALPHA)
        overlay_rect.fill((30, 254, 30))
        self._screen.blit(overlay_rect, (25, 240), special_flags=pygame.BLEND_RGB_MULT)

    def draw(self):
        """Draw the scene."""
        super().draw()
        Font().draw(self._screen, "SCORE<1> HI-SCORE SCORE<2>", (8, 8))
        Font().draw(self._screen, "0000", (24, 24))
        Font().draw(self._screen, "0000", (88, 24))
        Font().draw(self._screen, "0000", (168, 24))
        if self.secret:
            Font().draw(self._screen, "LULZSUN", (80, 32))

        bottom = pygame.Surface((self._screen.get_width(), 1))
        bottom.fill((255, 255, 255))
        self._screen.blit(bottom, (0, 239))
        Font().draw(self._screen, "3", (8, 240))
        Player().draw(self._screen, (24, 240))
        Player().draw(self._screen, (24+16, 240))
        Font().draw(self._screen, "CREDIT 00", (136, 240))

        # render player
        self.player.draw(self._screen, (self.player.position_x, 216))

        # render shields
        for shield in self.shields:
            shield.draw(self._screen, (0, 0), relative=True)

        # render aliens
        for alien in self.aliens:
            alien.draw(self._screen, (0, 0), relative=True)
        
        if self.alien_position_x > 0:
            self.alien_position_x -= 1
            try:
                self.aliens[self.alien_position_x].draw(self._screen, (2*self.alien_move, 0), relative=True)
            except IndexError:
                pass

        if self.alien_position_y > 0:
            self.alien_position_y -= 1
            try:
                self.aliens[self.alien_position_y].draw(self._screen, (2*self.alien_move, 8), relative=True)
            except IndexError:
                pass

        # render bullets
        for bullet in self.bullets:
            bullet.draw(self._screen, relative=True)
