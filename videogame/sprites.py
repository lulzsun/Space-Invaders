"""Sprite objects for creating text and game entities."""

import os
import pygame

class Sprite:
    """Base class for making a sprite."""

    def __init__(self, filename, position=(0, 0)):
        self.position = position
        self._sheet = pygame.image.load(os.path.join(os.path.dirname(__file__), 'data', filename)).convert()
        self._rect = pygame.Rect((0, 0, 16, 8))
        self._surf = pygame.Surface(self._rect.size)

    def draw(self, surf: pygame.Surface, position=(0, 0), relative=False):
        """Draw the sprite on a surface at position"""
        pygame.Surface.set_colorkey(self._surf, [0, 0, 0], pygame.RLEACCEL)
        if not isinstance(self, Font):
            self._surf.blit(self._sheet, (0, 0), self._rect)
        if relative is False:
            self.position = position
            surf.blit(self._surf, self.position)
        else:
            self.position = (self.position[0]+position[0], self.position[1]+position[1])
            surf.blit(self._surf, self.position)

    def is_colliding(self, sprite):
        """Check collision between another sprite."""
        # this is definitely not the right way to do it...
        # my "sprite" classes are not actually sprite objects, so instead
        # i am just temporarily creating the sprites to use collide_mask()
        # i am too stubborn to do things the right way, i may regret this later
        if isinstance(self, Alien) and self._is_alive is False:
            return False

        if isinstance(sprite, Alien) and sprite._is_alive is False:
            return False

        real_sprite1 = pygame.sprite.Sprite()
        real_sprite1.image = self._surf
        real_sprite1.rect = pygame.Rect((
            self.position[0], self.position[1],
            self._rect.width, self._rect.height
        ))
        real_sprite1.mask = pygame.mask.from_surface(self._surf)

        real_sprite2 = pygame.sprite.Sprite()
        real_sprite2.image = sprite._surf
        real_sprite2.rect = pygame.Rect((
            sprite.position[0], sprite.position[1],
            sprite._rect.width, sprite._rect.height
        ))
        real_sprite2.mask = pygame.mask.from_surface(sprite._surf)

        return pygame.sprite.collide_mask(real_sprite1, real_sprite2)

class Player(Sprite):
    """Player sprite class which the user controls"""

    def __init__(self):
        """Initialize the Player."""
        super().__init__('player.png')
        self.velocity = 0
        self.position_x = 24
        self.shooting = False

    def move(self, event):
        """Keyboard controls for moving"""
        if event.type == pygame.KEYDOWN:
            if event.key in {pygame.K_a, pygame.K_LEFT}:
                if self.velocity != -1:
                    self.velocity = -1
            if event.key in {pygame.K_d, pygame.K_RIGHT}:
                if self.velocity != 1:
                    self.velocity = 1
        elif event.type == pygame.KEYUP:
            if event.key in {pygame.K_a, pygame.K_LEFT}:
                if self.velocity == -1:
                    self.velocity = 0
            if event.key in {pygame.K_d, pygame.K_RIGHT}:
                if self.velocity == 1:
                    self.velocity = 0

    def shoot(self, event):
        """Keyboard controls for shooting"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.shooting = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                self.shooting = False

    def draw(self, surf: pygame.Surface, position=(0, 0), relative=False):
        """Draw player wit velocity/position"""
        self.position_x += self.velocity
        self.position_x = max(min(self.position_x, 224-16*2), 16)
        super().draw(surf, position, relative)

class Alien(Sprite):
    """Base alien class for all types of aliens"""

    def __init__(self, filename, position, grid_position):
        """Initialize the Alien."""
        super().__init__(filename, position)
        self.points = 0
        self._is_alive = True
        self._explode_frame = 0
        self._idle_frame = 0
        self.grid_position = grid_position

    def anim(self):
        """Alternative between 2 alien frames"""
        if self._is_alive and self._explode_frame == 0:
            self._rect = pygame.Rect((16*self._idle_frame, 0, 16, 8))
            self._surf = pygame.Surface(self._rect.size)
            if self._idle_frame == 0:
                self._idle_frame = 1
            else:
                self._idle_frame = 0

    def explode(self):
        """Play explosion animation.
        Return True when done"""
        if self._explode_frame == 0:
            self._rect = pygame.Rect((32, 0, 16, 8))
            # self.position = (self.position[0]-2, self.position[1])
            self._surf = pygame.Surface(self._rect.size)

        self._explode_frame += 1
        return self._explode_frame == 15

    def draw(self, surf: pygame.Surface, position=(0, 0), relative=False):
        """Draw the sprite, only if alien is alive"""
        if self._is_alive:
            super().draw(surf, position, relative)

class Squid(Alien):
    """Squid class sprite, an alien varient"""

    def __init__(self, position, grid_position):
        """Initialize the Squid alien."""
        super().__init__('alien1.png', position, grid_position)
        self.points = 30

class Crab(Alien):
    """Crab class sprite, an alien varient"""

    def __init__(self, position, grid_position):
        """Initialize the Crab alien."""
        super().__init__('alien2.png', position, grid_position)
        self.points = 20

class Octopus(Alien):
    """Octopus class sprite, an alien varient"""

    def __init__(self, position, grid_position):
        """Initialize the Octopus alien."""
        super().__init__('alien3.png', position, grid_position)
        self.points = 10

class Shield(Sprite):
    """Shield class for displaying shield sprite"""

    def __init__(self, position):
        """Initialize the Shield."""
        super().__init__('shield.png', position)
        self._rect = pygame.Rect((0, 0, 24, 16))
        self._surf = pygame.Surface(self._rect.size)

class Bullet(Sprite):
    """Bullet class for displaying bullet sprites"""

    def __init__(self, position, projectile=0, is_player_owned=False):
        """Initialize the bullet projectile."""
        super().__init__('bullet.png', position)
        self.is_player_owned = is_player_owned
        self._rect = pygame.Rect((projectile*4*3, 0, 3, 8))
        if self.is_player_owned:
            self._rect = pygame.Rect((14*3, 0, 3, 8))
        self._surf = pygame.Surface(self._rect.size)
        self._projectile = projectile
        self._explode_frame = 0
        self._move_frame = 0

    def move(self, position):
        """Move bullet and return current position"""
        new_position = (self.position[0] + position[0],
                        self.position[1] + position[1])
        self.position = new_position

        # animation
        if self.is_player_owned is False:
            if self._explode_frame == 0:
                self._rect = pygame.Rect(((self._projectile*4*3)+(3*self._move_frame), 0, 3, 8))
            self._move_frame += 1
            if self._move_frame == 4:
                self._move_frame = 0
        return self.position

    def explode(self, miss=False, hidden=False):
        """Play explosion animation.
        If miss is True, play a different sprite
        If hidden is True, don't show sprite
        Return True when done"""
        if self._explode_frame == 0:
            if miss:
                self._rect = pygame.Rect((3*12, 0, 0 if hidden else 6, 8))
                self.position = (self.position[0]-2, self.position[1])
            else:
                self._rect = pygame.Rect((3*15, 0, 0 if hidden else 8, 8))
                self.position = (self.position[0]-2, self.position[1])
            self._surf = pygame.Surface(self._rect.size)

        self._explode_frame += 1
        return self._explode_frame == 15

    def draw(self, surf: pygame.Surface, position=(0, 0), relative=False):
        super().draw(surf, position, relative)

class Font(Sprite):
    """Font class for displaying 8x8 ascii sprites"""

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

    def draw(self, surf: pygame.Surface, position=(0, 0), relative=False, text=""):
        self._rect = pygame.Rect((0, 0, len(text)*8, 8))
        self._surf = pygame.Surface(self._rect.size)

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
