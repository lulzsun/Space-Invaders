"""Sprite objects for creating text and game entities."""

import os
import pygame

class Sprite:
    """Base class for making a sprite."""

    def __init__(self, filename, position=(0, 0)):
        self._position = position
        self._sheet = pygame.image.load(os.path.join(os.path.dirname(__file__), 'data', filename)).convert()
        self._rect = pygame.Rect((0, 0, 16, 8))
        self._surf = pygame.Surface(self._rect.size).convert()

    def draw(self, surf: pygame.Surface, position=(0, 0), relative=False):
        """Draw the sprite on a surface at position"""
        position = (position[0], position[1])
        self._surf.blit(self._sheet, (0, 0), self._rect)
        if relative is False:
            self._position = position
            surf.blit(self._surf, self._position)
        else:
            self._position = (self._position[0]+position[0], self._position[1]+position[1])
            surf.blit(self._surf, self._position)
    
class Player(Sprite):
    def __init__(self):
        """Initialize the Player."""
        super().__init__('player.png')

class Alien(Sprite):
    def __init__(self, filename, position):
        """Initialize the Alien."""
        super().__init__(filename, position)
    
    def draw(self, surf: pygame.Surface, position=(0, 0), relative=False):
        super().draw(surf, position, relative)
        if position != (0, 0):
            if self._rect.left == 0:
                self._rect = pygame.Rect((16, 0, 16, 8))
            else:
                self._rect = pygame.Rect((0, 0, 16, 8))
            self._surf = pygame.Surface(self._rect.size).convert()

class Squid(Alien):
    def __init__(self, position):
        """Initialize the Squid alien."""
        super().__init__('alien1.png', position)

class Crab(Alien):
    def __init__(self, position):
        """Initialize the Crab alien."""
        super().__init__('alien2.png', position)

class Octopus(Alien):
    def __init__(self, position):
        """Initialize the Octopus alien."""
        super().__init__('alien3.png', position)