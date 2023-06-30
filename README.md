# Space Invaders
My take on the classic 1978 Space Invaders arcade game. Game mechanics and design are heavily inspired by the original, and done as faithful as possible (to the best of my abilities + time constraint; deadline). Built using pygame.

An assignment done for CPSC 385 @ CSUF in Summer 2023

## Install and execute
Unix:
```bash
pip install -r requirements.txt
./invaders.py
```
Windows:
```bash
pip install -r requirements.txt
python invaders.py
```
Optionally, you can enter a virtualenv and install requirements.

## Controls
| Action | Controls |
| ----------- | ----------- |
| Movement | A, D, or Left Arrow, Right Arrow |
| Fire, Select | Space |

## Notes
As I did my best to recreate the original game as faithful as possible, some things were not implemented properly or are completely different.

Factors include due to time constraints, professor requirements, my motives, and my abilities.

Here is a list of features/functions and my details on them (potential for future changes):
- Leaderboard system
    - As per requirement of professor's [REQUIREMENTS.md](REQUIREMENTS.md), this had to be implemented while the original game does not have this
- Sound system
    - The original game used a tone generator, due to my abilities in understanding the original tones and sounds, I've opt'd to use sound files to substitute. Interestingly, [most emulators do the same](https://www.github.com/MiSTer-devel/Arcade-SpaceInvaders_MiSTer/issues/3) because of this difficulty.
- Initial credits screen
    - My personal addition, not in original game
- Title screen
    - Current title screen does not implement the little easter eggs scenes or demo scenes
- Credits/Coin system
    - Not implemented
- Alien attack sequence
    - In the original game, the aliens can have at most 3 projectiles on screen. However this remake only allows 1 projectile on screen
- Alien projectile
    - In the original game, the aliens have 3 different projectile sprites tha they randomly switch between upon shooting. This remake is only using one sprite projectile
    - There is no alien projectile collision with player's projectile
- Two player mode
    - Only one player mode is avaliable at the time of writing
- No bonus opportunity
    - AKA, the flying ufo or 'Cuttlefish' is not implemented at the time of writing
- Segmentation Fault
    - There is a chance of a random occurance of a seg. fault. I have no idea why and when it occurs. (Hope it doesn't occur during grading).

... and probably many more that I forgot about.

## References
These are some specific references I used during the making of this game:
- http://tips.retrogames.com/gamepage/invaders.html
- https://gamedev.stackexchange.com/questions/202505/how-were-the-invaders-programmed-to-shoot-in-the-original-arcade-version-of-spac
- https://tobiasvl.github.io/blog/space-invaders/

## License
All game resources are properly licensed/credited in [videogame/data/LICENSE.md](./videogame/data/LICENSE.md)