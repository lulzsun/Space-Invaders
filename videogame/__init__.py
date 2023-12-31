# Jimmy Quach
# jminquach@csu.fullerton.edu
# @lulzsun
"""Init file for the videogame module."""

__all__ = ["game", "scene", "sprites"]

import pickle


def save_scores(leaderboard):
    """Write leaderboard to 'leaderboard.pkl'"""
    with open('leaderboard.pkl', 'wb') as file_handle:
        pickle.dump(leaderboard, file_handle, pickle.HIGHEST_PROTOCOL)


def load_scores():
    """Read the contents of 'leaderboard.pkl',
    decode it, and return it"""
    leaderboard = [("aaa", 0)]
    try:
        with open('leaderboard.pkl', 'rb') as file_handle:
            leaderboard = pickle.load(file_handle)
        leaderboard.sort(key=lambda x: x[1], reverse=True)
        return leaderboard
    except FileNotFoundError:
        return leaderboard
