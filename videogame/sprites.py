"""Sprite objects for creating text and game entities."""

from collections import namedtuple
import os
import pygame

Position = namedtuple("Position", "x y")

class Sprite:
    """Base class for making a sprite."""

    def __init__(self, filename):
        self.position = Position(x=0, y=0)
        self._sheet = pygame.image.load(os.path.join(os.path.dirname(__file__), 'data', filename)).convert()
        self._rect = pygame.Rect((0, 0, 16, 8))
        self._surf = pygame.Surface(self._rect.size).convert()

    def draw(self, surf: pygame.Surface, position=Position(x=0, y=0)):
        """Draw the sprite on a surface at position"""
        self._surf.blit(self._sheet, (0, 0), self._rect)
        surf.blit(self._surf, position)
    
class Player(Sprite):
    def __init__(self):
        """Initialize the Player."""
        super().__init__('player.png')

class Alien(Sprite):
    def __init__(self, filename):
        """Initialize the Alien."""
        super().__init__(filename)

class Squid(Alien):
    def __init__(self):
        """Initialize the Squid alien."""
        super().__init__('alien1.png')

class Crab(Alien):
    def __init__(self):
        """Initialize the Crab alien."""
        super().__init__('alien2.png')

class Octopus(Alien):
    def __init__(self):
        """Initialize the Octopus alien."""
        super().__init__('alien3.png')