import pygame
from .level_base import Level
from sprites import Player, Monster


class Level01(Level):

    def __init__(self):
        super().__init__(Level02, "static/test_map.png", [400, 400], [0, 0])
        #self.sprites.append(Monster([200, 200]))
        #self.sprites.append(Monster([300, 300]))
        #self.sprites.append(Monster([400, 400]))
        #self.sprites.append(Monster([500, 500]))
        self.sprites.append(Monster([100, 100]))

    def tick(self):
        for sprite in self.sprites:

            if str(sprite) == "Monster":
                if self.get_distance_between_positions(sprite.position, self.sprites[0].position) <= sprite.hunt_range:
                    """ BUG!!! -- IF OLLY IS DIRECTLY ABOVE OR BELOW, CONDITION TRIGGERS TRUE... INSPECT self.get_distance_between_positions() METHOD!!! """
                    sprite.isHunting = True
                    sprite.player_pos = self.sprites[0].get_position_on_screen()
                    if sprite.isCollidingWithPlayer:
                        self.sprites[0].isLive = False

                else:
                    sprite.isHunting = False

            elif str(sprite) == "Player":
                pass

            sprite.tick()


class Level02(Level):

    def __init__(self):
        super().__init__(0, "")


