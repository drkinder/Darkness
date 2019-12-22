import pygame
from PIL import Image
from sprites import Player, Flashlight
import math


class Level:

    def __init__(self, next_level, map_filepath, player_start_pos, map_start_pos): # Put levels in list and increment through them.
        self.display_size = (800, 600)
        self.next_level = next_level
        self.map = pygame.image.load(map_filepath)
        self.map_size = self.get_image_dimensions(map_filepath)
        self.map_position = map_start_pos
        self.sprites = []
        self.sprites.append(Player(player_start_pos))

    def handle_event(self, pressed):

        screen_map_collisions = self.get_screen_collision_with_edge_of_map()
        movement = [0, 0] # How much the player moved

        if pressed[pygame.K_w]:
            if (self.sprites[0].get_position_on_screen()[1] <= self.display_size[1]/2 and
                    "top" not in screen_map_collisions):
                self.map_position[1] += self.sprites[0].movement_speed
                movement[1] += self.sprites[0].movement_speed # Shift other sprites
            else:
                self.sprites[0].move((0, -self.sprites[0].movement_speed))

        if pressed[pygame.K_s]:
            if (self.sprites[0].get_position_on_screen()[1] >= self.display_size[1]/2 and
                    "bottom" not in screen_map_collisions):
                self.map_position[1] -= self.sprites[0].movement_speed
                movement[1] += -self.sprites[0].movement_speed # Shift other sprites
            else:
                self.sprites[0].move((0, self.sprites[0].movement_speed))

        if pressed[pygame.K_a]:
            if (self.sprites[0].get_position_on_screen()[0] <= self.display_size[0]/2 and
                    "left" not in screen_map_collisions):
                self.map_position[0] += self.sprites[0].movement_speed
                movement[0] += self.sprites[0].movement_speed # Shift other sprites
            else:
                self.sprites[0].move((-self.sprites[0].movement_speed, 0))

        if pressed[pygame.K_d]:
            if (self.sprites[0].get_position_on_screen()[0] >= self.display_size[0]/2 and
                    "right" not in screen_map_collisions):
                self.map_position[0] -= self.sprites[0].movement_speed
                movement[0] += -self.sprites[0].movement_speed # Shift other sprites
            else:
                self.sprites[0].move((self.sprites[0].movement_speed, 0))

        self.move_non_player_sprites(movement)

    def move_non_player_sprites(self, coord_change):
        for sprite in self.sprites:
            if str(sprite) != "Player":
                sprite.move(coord_change)

    def get_screen_collision_with_edge_of_map(self):
        collisions = []
        if self.map_position[0] >= 0:
            collisions.append("left")
        if self.map_position[0] <= -self.map_size[0]+self.display_size[0]:
            collisions.append("right")
        if self.map_position[1] >= 0:
            collisions.append("top")
        if self.map_position[1] <= -self.map_size[1]+self.display_size[1]:
            collisions.append("bottom")
        return collisions

    def get_image_dimensions(self, image_path):
        width, height = Image.open(image_path).size
        return tuple((width, height))

    def get_distance_between_positions(self, pos1, pos2):
        x = math.pow(pos2[0] - pos1[0], 2)
        y = math.pow(pos2[1] - pos1[1], 2)
        return math.sqrt(x + y)

    def tick(self):
        pass
