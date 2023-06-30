"""Moduel of objects for playing sound."""

import os
import pygame


class Sound:
    """Base class for making sound."""
    def __init__(self, channel=0, filename=""):
        self._filename = filename
        self._channel = channel

    def filepath(self):
        """Return full file path of sound file"""
        return os.path.join(os.path.dirname(__file__), 'data', self._filename)

    def play(self):
        """Play sound file, stop sound if one is already playing"""
        pygame.mixer.Channel(self._channel).stop()
        pygame.mixer.Channel(self._channel).play(pygame.mixer.Sound(self.filepath()))


class BGM(Sound):
    """Background music, aka the pulsing sound effect"""
    def __init__(self):
        super().__init__(0)
        self._tone = 0
        self.timing = 60

    def play(self, new_timing=60):
        """Plays 4 tones of the BGM, return True if timing changed"""
        self._filename = f"sfx_menu_move{self._tone+1}.wav"
        super().play()
        self._tone += 1
        if self._tone == 4:
            self._tone = 0
            self.timing = new_timing
            return True
        return False


class ShootSFX(Sound):
    """Player shooting sound effect"""
    def __init__(self):
        super().__init__(1, "sfx_wpn_laser9.wav")


class ExplodeSFX(Sound):
    """Alien exploding/death sound effect"""
    def __init__(self):
        super().__init__(1, "sfx_sounds_interaction25.wav")


class DeathSFX(Sound):
    """Player exploding/death sound effect"""
    def __init__(self):
        super().__init__(1, "sfx_exp_medium4.wav")


class PowerUpSFX(Sound):
    """Player life gain sound effect"""
    def __init__(self):
        super().__init__(2, "sfx_sounds_pause6_in.wav")
