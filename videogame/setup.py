# Jimmy Quach
# jminquach@csu.fullerton.edu
# @lulzsun
""" Simple setup.py """

# Jimmy: I'm unsure why pylint is complaining about how it is unable
# to import setuptools, even though it compiles and runs without issues
# So, I've decided to just ignore this lint warning
# pylint: disable-next=import-error
from setuptools import setup

setup_info = {
    "name": "videogame",
    "version": "0.1",
    "description": "A package to support writing games with PyGame",
    "author": "Jimmy Quach",
    "author_email": "jminquach@csu.fullerton.edu",
    "url": "https://github.com/cpsc-summer-2023/cpsc-386-04-scene-lulzsun",
}

setup(**setup_info)
