"""Scene objects for making games with PyGame."""

import random
from typing import List
import pygame
from videogame import save_scores, load_scores
from videogame.sound import (
    BGM, DeathSFX, ExplodeSFX, ShootSFX
)
from videogame.sprites import (
    Bullet, Cuttlefish, Shield, Crab, Font, 
    Octopus, Player, Squid
)


class Scene:
    """Base class for the game."""

    def __init__(self, screen: pygame.Surface, soundtrack=None):
        """Scene initializer"""
        self._screen = screen
        self._frame_rate = 60
        self._is_valid = True
        self._is_exiting = False
        self._soundtrack = soundtrack
        self._render_updates = None

        self._secret = False
        self._frames = 0
        self._hi_score = load_scores()[0][1]
        self._p1_score = 0
        self._next_life = 0
        self._lives = 3
        self._level = 0
        self._credit = 0

    def draw(self):
        """Draw the scene."""
        # Draw persistant UI
        Font().draw(self._screen, (8, 8), text="SCORE<1> HI-SCORE SCORE<2>")
        Font().draw(self._screen, (24, 24), text=str(self._p1_score).zfill(4))
        Font().draw(self._screen, (88, 24), text=str(self._hi_score).zfill(4))
        Font().draw(self._screen, (168, 24), text="0000")
        if self._secret:
            Font().draw(self._screen, (80, 32), text="LULZSUN")
        Font().draw(self._screen, (8, 240), text=str(max(min(self._lives, 99), 0)))
        # Draw lives
        for i in range(min(self._lives-1, 6)):
            Player().draw(self._screen, (24+(i*16), 240))

        Font().draw(self._screen, (136, 240), 
                    text=f"CREDIT {str(self._credit).zfill(2)}"
        )

    def process_event(self, event):
        """Process a game event by the scene."""
        if event.type == pygame.QUIT:
            print("Good Bye!")
            self.next_scene()
            self._is_exiting = True
            self._is_valid = False

    def next_scene(self):
        self._frames = 0
        self._is_valid = False

    def is_exiting(self):
        return self._is_exiting

    def is_valid(self):
        """Is the scene valid? A valid scene can be used to play a scene."""
        return self._is_valid

    def render_updates(self):
        """Render all sprite updates."""
        # create a color overlay in certain areas of the screen
        # this mimics 1978 space invaders coloring
        overlay_rect = pygame.Surface((self._screen.get_width(), 32), pygame.SRCALPHA)
        overlay_rect.fill((254, 30, 30))
        self._screen.blit(overlay_rect, (0, 32), special_flags=pygame.BLEND_RGB_MULT)

        overlay_rect = pygame.Surface((self._screen.get_width(), 56), pygame.SRCALPHA)
        overlay_rect.fill((30, 254, 30))
        self._screen.blit(overlay_rect, (0, 184), special_flags=pygame.BLEND_RGB_MULT)

        overlay_rect = pygame.Surface((111, 16), pygame.SRCALPHA)
        overlay_rect.fill((30, 254, 30))
        self._screen.blit(overlay_rect, (25, 240), special_flags=pygame.BLEND_RGB_MULT)

    def update_scene(self):
        """Update the scene state."""
        self._frames += 1
        self._screen.fill("black")

    def start_scene(self):
        """Start the scene."""
        if self._soundtrack:
            try:
                pygame.mixer.music.load(self._soundtrack)
                pygame.mixer.music.set_volume(0.2)
            except pygame.error as pygame_error:
                print("Cannot open the mixer?")
                print('\n'.join(pygame_error.args))
                raise SystemExit("broken!!") from pygame_error
            pygame.mixer.music.play(-1)

    def end_scene(self):
        """End the scene with a fading effect."""
        self._frames += 10
        if self._soundtrack and pygame.mixer.music.get_busy():
            # Fade music out so there isn't an audible pop
            pygame.mixer.music.fadeout(500)
            pygame.mixer.music.stop()
            self._soundtrack = None
        
        bottom = pygame.Surface((self._frames, 239-32))
        bottom.fill((0, 0, 0))
        self._screen.blit(bottom, (0, 32))

        if self._frames >= self._screen.get_width():
            self._frames = 0
            return True
        return False

    def frame_rate(self):
        """Return the frame rate the scene desires."""
        return self._frame_rate


class CreditScene(Scene):
    """Scene of my credit scene unrelated to space invaders"""

    def __init__(self, screen, soundtrack=None):
        super().__init__(screen, soundtrack)

    def process_event(self, event):
        """Process a game event by the scene."""
        super().process_event(event)
        if event.type == pygame.KEYDOWN:
            self.next_scene()

    def draw(self):
        Font().draw(self._screen, (84, 64), text="CREDITS")
        Font().draw(self._screen, (8, 88), text=
                    "This game was developed by")
        Font().draw(self._screen, (72, 104), text=
                    "Jimmy Quach")
        Font().draw(self._screen, (40, 128), text=
                    "Summer 2023 CPSC385")
        Font().draw(self._screen, (40, 144), text=
                    "CAL STATE FULLERTON")
        Font().draw(self._screen, (48, 184), text=
                    "Press any button")
        Font().draw(self._screen, (64, 200), text=
                    "to continue")
        super().draw()


class TitleScene(Scene):
    """Scene of space invaders' title screen(s)"""

    def __init__(self, screen, soundtrack=None):
        super().__init__(screen, soundtrack)
        self._constant_strings = [
            "PLAY",
            "SPACE  INVADERS       ",
            "*SCORE ADVANCE TABLE*",
            "=? MYSTERY",
            "=30 POINTS",
            "=20 POINTS",
            "=10 POINTS"
        ]
        self._anim_state = 0
        self._strings = [''] * len(self._constant_strings)

    def process_event(self, event):
        """Process a game event by the scene."""
        super().process_event(event)
        if event.type == pygame.KEYDOWN:
            self.next_scene()

    def update_scene(self):
        """Update scene state."""
        super().update_scene()

        # animating the type writer effect
        if self._frames % (self.frame_rate() / 12) == 0:
            if self._anim_state != 2 and self._anim_state < len(self._constant_strings):
                tmp = self._constant_strings[self._anim_state]
                txt = tmp[:len(self._strings[self._anim_state])+1]
                self._strings[self._anim_state] = txt
                if self._strings[self._anim_state] == self._constant_strings[self._anim_state]:
                    self._anim_state += 1
            elif self._anim_state == 2:
                self._strings[2] = self._constant_strings[2]
                self._anim_state += 1

    def draw(self):
        """Draw the scene."""
        Font().draw(self._screen, (96, 64), text=self._strings[0])
        Font().draw(self._screen, (56, 88), text=self._strings[1])
        Font().draw(self._screen, (32, 120), text=self._strings[2])
        Font().draw(self._screen, (80, 136), text=self._strings[3])
        Font().draw(self._screen, (80, 152), text=self._strings[4])
        Font().draw(self._screen, (80, 168), text=self._strings[5])
        Font().draw(self._screen, (80, 184), text=self._strings[6])
        if self._strings[2] != '':
            Cuttlefish((60, 136)).draw(self._screen, relative=True)
            Squid((64, 152)).draw(self._screen, relative=True)
            Crab((64, 168)).draw(self._screen, relative=True)
            Octopus((64, 184)).draw(self._screen, relative=True)
        super().draw()


class LeaderboardScene(Scene):
    """Scene of leaderboard, not part of original game"""

    def __init__(self, screen, soundtrack=None):
        super().__init__(screen, soundtrack)
        self.hi_score = 0
        self.current_name = "aaa"
        self.name_char_index = 0

        self._anim_state = 0
        self._title_txt = ""
        self._leaderboard = load_scores()
        self._top_5_txt = ['', '', '', '', '']

    def process_event(self, event):
        """Process a game event by the scene."""
        super().process_event(event)
        if self.name_char_index == 3:
            self._leaderboard.append((self.current_name, self.hi_score))
            save_scores(self._leaderboard)
            return
        current_char = self.current_name[self.name_char_index]
        if event.type == pygame.KEYDOWN and self._top_5_txt[4] != "":
            if event.key == pygame.K_SPACE:
                self.name_char_index += 1
                if self.name_char_index == 3:
                    self.next_scene()
            if event.key in {pygame.K_a, pygame.K_LEFT}:
                if current_char == 'a':
                    current_char = 'z'
                else:
                    current_char = chr(ord(current_char) - 1)
                updated_name = (
                    self.current_name[:self.name_char_index] +
                    current_char +
                    self.current_name[self.name_char_index+1:]
                )
                self.current_name = updated_name
            if event.key in {pygame.K_d, pygame.K_RIGHT}:
                if current_char == 'z':
                    current_char = 'a'
                else:
                    current_char = chr(ord(current_char) + 1)
                updated_name = (
                    self.current_name[:self.name_char_index] +
                    current_char +
                    self.current_name[self.name_char_index+1:]
                )
                self.current_name = updated_name

    def update_scene(self):
        """Update scene state."""
        super().update_scene()

        # animating the type writer effect
        if self._frames % (self.frame_rate() / 12) == 0:
            txt = "* LEADER BOARD *"
            if self._title_txt != txt:
                self._title_txt = txt[:self._anim_state+1]
                self._anim_state += 1
                if self._title_txt == txt:
                    self._anim_state = 0
                return

            if self._anim_state != 5:
                i = self._anim_state
                try:
                    self._top_5_txt[i] = (
                        f"{i+1}   {self._leaderboard[i][0]}   " +
                        f"{str(self._leaderboard[i][1]).zfill(4)}"
                    )
                except:
                    self._top_5_txt[i] = f"{i+1}   aaa   0000"
            else:
                return
            self._anim_state += 1

    def draw(self):
        Font().draw(self._screen, (48, 64), text=self._title_txt)

        for i, score in enumerate(self._top_5_txt):
            Font().draw(self._screen, (56, 88+(i*16)), text=score)

        if self._top_5_txt[4] != "":
            Font().draw(self._screen, (56, 176+8), 
                text=f"    {self.current_name}   {str(self.hi_score).zfill(4)}")
            carat = pygame.Surface((8, 1))
            carat.fill((255, 255, 255))
            if self.name_char_index != 3:
                self._screen.blit(carat, (87+(self.name_char_index*8), 194))
            Font().draw(self._screen, (64, 208), text="Enter  name")
        super().draw()


class InvadersGameScene(Scene):
    """Scene with the actual gameplay of space invaders"""

    def __init__(self, screen, soundtrack=None):
        """Initialize the scene."""
        super().__init__(screen, soundtrack)

        self._anim_state = 0
        self.loading = True
        self.game_over_txt = ""

        self.player = Player()

        self.shields: List[Shield]
        self.shields = []

        self.aliens: List[
            List[Squid],
            List[Crab], List[Crab],
            List[Octopus], List[Octopus]
        ]
        self.aliens = [[], [], [], [], []]
        self.alien_move = 2
        self.alien_position_x = 0
        self.alien_position_y = 0

        self.BGM = BGM()

        self.bullets: List[Bullet]
        self.bullets = []

    def process_event(self, event):
        """Process game events."""
        super().process_event(event)

        if self.loading == True:
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self._secret = not self._secret

        self.player.move(event)
        self.player.shoot(event)

    def update_scene(self):
        """Update the scene state."""
        super().update_scene()

        # animating the loading effect
        if self.loading == True:
            if self._anim_state == 0:
                if len(self.shields) == 4:
                    self.shields.clear()
                self.shields.append(Shield((31+((24+22)*len(self.shields)), 192)))
                if len(self.shields) == 4:
                    self._anim_state += 1
            elif self._anim_state == 1:
                self.aliens[4].append(
                    Octopus((len(self.aliens[4])*16 + 24, 128), (len(self.aliens[4]), 4))
                )
                if len(self.aliens[4]) == 11:
                    self._anim_state += 1
            elif self._anim_state == 2:
                self.aliens[3].append(
                    Octopus((len(self.aliens[3])*16 + 24, 112), (len(self.aliens[3]), 3))
                )
                if len(self.aliens[3]) == 11:
                    self._anim_state += 1
            elif self._anim_state == 3:
                self.aliens[2].append(
                    Crab((len(self.aliens[2])*16 + 24, 96), (len(self.aliens[2]), 2))
                )
                if len(self.aliens[2]) == 11:
                    self._anim_state += 1
            elif self._anim_state == 4:
                self.aliens[1].append(
                    Crab((len(self.aliens[1])*16 + 24, 80), (len(self.aliens[1]), 1))
                )
                if len(self.aliens[1]) == 11:
                    self._anim_state += 1
            elif self._anim_state == 5:
                self.aliens[0].append(
                    Squid((len(self.aliens[0])*16 + 24, 64), (len(self.aliens[0]), 0))
                )
                if len(self.aliens[0]) == 11:
                    self._anim_state += 1
            elif self._anim_state == 6:
                self._anim_state = 0
                self.loading = False
                self.alien_line_of_sight = [alien.grid_position for alien in self.aliens[4]]
            return

        # check if player was hit and play animation
        if self.player._explode_frame != 0:
            if self._frames % 5 == 0:
                done = self.player.explode()
                if done:
                    self._lives -= 1
                    self.player._explode_frame = 0
                    self._frames = 0
                    if self._lives <= 0:
                        return
                    self.player.respawn()
            return

        # check for gameover and play gameover animation
        if self._lives <= 0:
            txt = "GAME OVER               "
            if self._frames % (self.frame_rate() / 12) == 0:
                self.game_over_txt = txt[:self._anim_state+1]
                self._anim_state += 1
                if self.game_over_txt == txt:
                    self._anim_state = 0
                    self.next_scene()
            return

        # check if all aliens are dead
        if sum(len(x) for x in self.aliens) == 0:
            self.player.velocity = 0
            self.bullets.clear()
            # reseting the game
            if self._frames % self.frame_rate() == 0:
                self._frames = 0
                self.BGM = BGM()
                self.player = Player()
                self.alien_move = 2
                self.alien_position_x = 0
                self.alien_position_y = 0
                self._level += 1
                self.loading = True
            return

        # play BGM
        if self._frames % self.BGM.timing == 0:
            changed = self.BGM.play((5+sum(len(x) for x in self.aliens)))
            if changed == True:
                self._frames = 0

        for bullet in self.bullets:
            # move bullets
            position = bullet.position
            if bullet._explode_frame == 0:
                if bullet.is_player_owned:
                    position = bullet.move((0, -4))
                else:
                    position = bullet.move((0, 1))
            else:
                done = bullet.explode()
                if done:
                    self.bullets.remove(bullet)
                continue

            if position[1] < 34:
                if bullet._explode_frame == 0:
                    bullet.move((0, 4))
                bullet.explode(True)

            if position[1] > 231:
                bullet.explode()

            # bullet collision check
            for alien_row in self.aliens:
                for alien in alien_row:
                    if bullet.is_player_owned and alien.is_colliding(bullet):
                        ExplodeSFX().play()
                        alien.explode()
                        self.bullets.remove(bullet)
                        self._p1_score += alien.points
                        self._next_life += alien.points
                        if self._next_life >= 1500:
                            self._lives += 1
                            self._next_life -= 1500
                        return

            for shield in self.shields:
                if shield.is_colliding(bullet):
                    bullet.explode()
                    shield.damage(bullet)
                    continue

            if self.player.is_colliding(bullet):
                DeathSFX().play()
                self.bullets.clear()
                self.player.explode()
                return

        for alien_row in self.aliens:
            for alien in alien_row:
                # check if alien passed y-axis limit (gameover)
                if alien.position[1] >= 216:
                    self._lives = 0
                    self.player.explode()
                    return

                # check if alien collided into a shield
                for shield in self.shields:
                    if shield.is_colliding(alien):
                        shield.damage(alien)

                # make sure aliens only have 1 bullet on screen
                if not any(bullet.is_player_owned == False for bullet in self.bullets):
                    shooter_pos = random.choice(self.alien_line_of_sight)
                    if alien.grid_position == shooter_pos and alien._is_alive:
                        self.bullets.append(Bullet((alien.position[0]+6, alien.position[1]+8)))

                if alien._explode_frame != 0:
                    done = alien.explode()
                    if done:
                        alien._explode_frame = 0
                        alien._is_alive = False
                        if sum(len(x) for x in self.aliens) == 0:
                            self._frames = 0
                    return
        
        # make sure player only has 1 bullet on screen
        if not any(bullet.is_player_owned for bullet in self.bullets):
            if self.player.shooting:
                ShootSFX().play()
                self.bullets.append(Bullet((self.player.position_x+7, 211), is_player_owned=True))

        # alien movement, overly complicated, but in a nutshell,
        # this allows one alien to move per frame. the less aliens
        # on the screen, the faster the aliens move. this is awesome
        index = 1
        new_los = None
        for alien_row in self.aliens:
            for alien in alien_row:
                if self.alien_position_x == index:
                    new_x = alien.position[0] + self.alien_move
                    alien.position = (new_x, alien.position[1])
                    self.alien_position_x -= 1
                    alien.anim()
                if self.alien_position_y == index:
                    new_y = alien.position[1] + 8
                    alien.position = (alien.position[0], new_y)
                    self.alien_position_y -= 1

                if alien._is_alive == True:
                    if self.alien_line_of_sight[alien.grid_position[0]] == None:
                        if new_los == None or new_los[1] < alien.grid_position[1]:
                            new_los = alien.grid_position

                index += 1

        if new_los != None:
            self.alien_line_of_sight.pop(new_los[0])
            self.alien_line_of_sight.insert(new_los[0], new_los)

        if self.alien_position_x == 0:
            move_down = False
            for alien_row in self.aliens:
                for alien in alien_row:
                    if alien._is_alive == False:
                        if alien.grid_position in self.alien_line_of_sight:
                            los_index = self.alien_line_of_sight.index(alien.grid_position)
                            self.alien_line_of_sight.pop(los_index)
                            self.alien_line_of_sight.insert(los_index, None)
                        alien_row.remove(alien)
                
                if len(alien_row) == 0:
                    continue

                first = alien_row[0]
                last = alien_row[-1]

                if first.position[0] < 16 - 8:
                    move_down = True
                elif last.position[0] > self._screen.get_width() - (16*2) + 8:
                    move_down = True

            self.alien_position_x = sum(len(x) for x in self.aliens)
            if move_down:
                self.alien_position_y = sum(len(x) for x in self.aliens)
                self.alien_move *= -1

    def draw(self):
        """Draw the scene."""

        # draw game over message
        Font().draw(self._screen, (96-16-8, 64-8), text=self.game_over_txt)

        # draw screen border
        bottom = pygame.Surface((self._screen.get_width(), 1))
        bottom.fill((255, 255, 255))
        self._screen.blit(bottom, (0, 239))

        # render player
        self.player.draw(self._screen, (self.player.position_x, 216))

        # render shields
        for shield in self.shields:
            shield.draw(self._screen, (0, 0), relative=True)

        # render aliens
        for alien_row in self.aliens:
            for alien in alien_row:
                alien.draw(self._screen, (0, 0), relative=True)

        # render bullets
        for bullet in self.bullets:
            bullet.draw(self._screen, relative=True)
        super().draw()
