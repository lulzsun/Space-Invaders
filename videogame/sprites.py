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
        if type(self) is not Font().__class__:
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

    def draw(self, surf: pygame.Surface, position=(0, 0), relative=False):
        super().draw(surf, position, relative)

class Alien(Sprite):
    def __init__(self, filename, position):
        """Initialize the Alien."""
        super().__init__(filename, position)
        self._is_alive = True
    
    def draw(self, surf: pygame.Surface, position=(0, 0), relative=False):
        super().draw(surf, position, relative)

        # on every 'move', the alien will alternate between sprites
        # in the sprite sheet, as part of its animation
        if position != (0, 0) and self._is_alive:
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

class Barrier(Alien):
    def __init__(self, position):
        """Initialize the Barrier."""
        super().__init__('barrier.png', position)
        self._rect = pygame.Rect((0, 0, 24, 16))
        self._surf = pygame.Surface(self._rect.size).convert()

class Font(Sprite):
    def __init__(self):
        """Initialize the Font."""
        super().__init__('font.png')
        self._rect = None
        self._surf = None
        self._font_map = [
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '<', '>', '=',
            '*', '?', '-'
        ]

    def draw(self, surf: pygame.Surface, text="", position=(0, 0), relative=False):
        self._rect = pygame.Rect((0, 0, len(text)*8, 8))
        self._surf = pygame.Surface(self._rect.size).convert()

        for i, letter in enumerate(text):
            letter = letter.lower()
            letter_pos = 40
            if letter in self._font_map:
                letter_pos = self._font_map.index(letter)
            if letter == ' ':
                continue
            letter_x = letter_pos % (self._sheet.get_width() // 8)
            letter_rect = pygame.Rect(letter_x * 8, 0, 8, 8)
            self._surf.blit(self._sheet, (i * 8, 0), letter_rect)
        super().draw(surf, position, relative)
