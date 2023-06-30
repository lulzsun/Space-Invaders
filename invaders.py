#!/usr/bin/env python3
# Jimmy Quach
# jminquach@csu.fullerton.edu
# @lulzsun

"""
Imports the the game demo and executes the main function.
"""

import sys
from videogame import game

if __name__ == "__main__":
    instance = game.SpaceInvadersGame()
    sys.exit(instance.run())
