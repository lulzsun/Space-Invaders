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
        pygame.Surface.set_colorkey(self._surf, [0, 0, 0], pygame.RLEACCEL)
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
        self.velocity = 0
        self.position_x = 24
        self.shooting = False

    def move(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                if self.velocity != -1:
                    self.velocity = -1
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                if self.velocity != 1:
                    self.velocity = 1
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                if self.velocity == -1:
                    self.velocity = 0
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                if self.velocity == 1:
                    self.velocity = 0

    def shoot(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.shooting = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                self.shooting = False

    def draw(self, surf: pygame.Surface, position=(0, 0), relative=False):
        # Update player position
        self.position_x += self.velocity
        self.position_x = max(min(self.position_x, 224-16*2), 16)
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

class Shield(Alien):
    def __init__(self, position):
        """Initialize the Shield."""
        super().__init__('shield.png', position)
        self._rect = pygame.Rect((0, 0, 24, 16))
        self._surf = pygame.Surface(self._rect.size).convert()

class Bullet(Sprite):
    def __init__(self, position, type=0, is_player_owned=False):
        """Initialize the bullet projectile."""
        super().__init__('bullet.png', position)
        self.is_player_owned = is_player_owned
        self._rect = pygame.Rect((type*4*3, 0, 3, 8))
        if self.is_player_owned:
            self._rect = pygame.Rect((14*3, 0, 3, 8))
        self._surf = pygame.Surface(self._rect.size).convert()
        self._type = type
        self._explode_frame = 0
        self._move_frame = 0
            

    def move(self, position):
        """Move bullet and return current position"""
        new_position = (self._position[0] + position[0], 
                        self._position[1] + position[1])
        self._position = new_position

        # animation
        if self.is_player_owned == False:
            if self._explode_frame == 0:
                self._rect = pygame.Rect(((self._type*4*3)+(3*self._move_frame), 0, 3, 8))
            self._move_frame += 1
            if self._move_frame == 4:
                self._move_frame = 0
        return self._position
    
    def explode(self, miss=False):
        """Play explosion animation."""
        """If miss is True, play a different sprite"""
        """Return True when done"""
        if self._explode_frame == 0:
            if miss:
                self._rect = pygame.Rect((3*12, 0, 6, 8))
                self._position = (self._position[0]-2, self._position[1])
            else:
                self._rect = pygame.Rect((3*15, 0, 8, 8))
                self._position = (self._position[0]-2, self._position[1])
            self._surf = pygame.Surface(self._rect.size).convert()
        
        self._explode_frame += 1
        return self._explode_frame == 10

    def draw(self, surf: pygame.Surface, position=(0, 0), relative=False):
        super().draw(surf, position, relative)

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
