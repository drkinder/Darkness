from PIL import Image
import pygame
from random import randint
import math


class Sprite:

    def __init__(self, position):
        self.display_size = (800, 600) # DISPLAY SIZE HARDCODING
        self.tick_count = 0

        self.position = position

        self.image, self.size = 0, 0
        self.image_dict = {"idle": "static/no_img.png"}  # Each child class must override
        self.set_image("idle")  # Each child class must call set_img after overriding image_dict

        self.isLive = True
        self.canMove = True
        self.movement_speed = 2

        self.facing = ""

    def set_image(self, img_key):
        self.image = pygame.image.load(self.image_dict[img_key])
        self.size = self.get_image_dimensions(self.image_dict[img_key])

    def move(self, coord_change):
        """ Accepts tuple (x, y) to represent change in position. """
        if self.canMove:
            self.position[0] += coord_change[0]
            self.position[1] += coord_change[1]

    def get_image_dimensions(self, image_path):
        width, height = Image.open(image_path).size
        return tuple((width, height))

    def get_screen_border_collisions(self):
        collisions = []
        if self.position[0] <= 0:
            collisions.append("left")
        if self.position[0]+self.size[0] >= self.display_size[0]:
            collisions.append("right")
        if self.position[1] <= 0:
            collisions.append("top")
        if self.position[1]+self.size[1] >= self.display_size[1]:
            collisions.append("bottom")
        return collisions

    def get_position_on_screen(self, position="center"):
        if position == "center":
            return tuple((self.position[0]+self.size[0]/2, self.position[1]+self.size[1]/2))

    def tick(self):
        self.tick_count += 1

    def __str__(self):
        return "Sprite"


class Player(Sprite):

    def __init__(self, position):
        super().__init__(position)

        self.image_dict = {
            "idle": "static/olly.png",
            "right": "static/olly.png",
        }
        self.set_image("idle")

        self.flashlight = Flashlight([position[0], position[1]])
        self.movement_speed = 2

    def move(self, coord_change):

        if self.canMove:
            collision_check = self.get_screen_border_collisions()

            # X-Axis Movement
            if coord_change[0] > 0:
                if "right" not in collision_check:
                    self.position[0] += coord_change[0]
            elif coord_change[0] < 0:
                if "left" not in collision_check:
                    self.position[0] += coord_change[0]

            # Y-Axis Movement
            if coord_change[1] > 0:
                if "bottom" not in collision_check:
                    self.position[1] += coord_change[1]
            elif coord_change[1] < 0:
                if "top" not in collision_check:
                    self.position[1] += coord_change[1]

    def tick(self):
        self.flashlight.move_to(self.position)
        self.flashlight.tick()

    def __str__(self):
        return "Player"


class Flashlight(Sprite):

    def __init__(self, origin):
        super().__init__(origin)
        self.offset = (0, 0)
        self.position = [origin[0] + self.offset[0], origin[1] + self.offset[1]]

        self.image_dict = {
            "idle": "static/blank_light.png",
        }
        self.set_image("idle")

        self.angle = 0

        self.slope = 0
        self.radius = 50
        self.light_width = 50
        self.light_line1 = [0, 0]
        self.light_line2 = [0, 0]

        self.mouse_pos = pygame.mouse.get_pos()

    def move_to(self, position):
        self.position = [position[0] + self.offset[0], position[1] + self.offset[1]]

    def update_mouse_pos(self):
        self.mouse_pos = pygame.mouse.get_pos()

    def update_slope(self):
        try:
            self.slope = self.mouse_pos[1] - self.position[1] / self.mouse_pos[0] - self.position[1]
        except ZeroDivisionError:
            pass

    def get_max_light_coordinates(self):
        x = self.radius/math.sqrt(1+self.slope*self.slope)
        y = self.slope*x
        return [x, y]

    def rotate_point(self, point_coords, degrees):
        x_rot = (point_coords[0]*math.cos(degrees)) - (point_coords[1]*math.sin(degrees))
        y_rot = (point_coords[1]*math.cos(degrees)) + (point_coords[0]*math.sin(degrees))
        return [x_rot, y_rot]

    def update_light_lines(self):
        center_point = self.get_max_light_coordinates()
        self.light_line1 = self.rotate_point(center_point, self.light_width/2)
        self.light_line2 = self.rotate_point(center_point, -self.light_width/2)

    def is_point_above_line(self, point, line):
        slope = (line[0] - self.position[0]) / (line[1] - self.position[1])
        return line[1] > slope*line[0]

    def is_point_within_radius(self, point):
        return point[0]*point[0] + point[1]*point[1] <= self.radius*self.radius

    def is_point_between_light_lines(self, coords):
        mouse_distance = [self.mouse_pos[0] - self.position[0], self.mouse_pos[1] - self.position[1]]

        if mouse_distance[1] < 0 < mouse_distance[0]:  # Cursor in Quadrant II
            print("QUAD II")
            return (not self.is_point_above_line(coords, self.light_line1)
                    and self.is_point_above_line(coords, self.light_line2)
                    and self.is_point_within_radius(coords))

    def tick(self):
        self.update_mouse_pos()
        self.update_slope()
        self.update_light_lines()


class Flashlight1(Sprite):

    def __init__(self, origin):
        super().__init__(origin)
        self.offset = (-150, -100)
        self.position = [origin[0]+self.offset[0], origin[1]+self.offset[1]]

        self.image_dict = {
            "idle": "static/light_screen1.png",
            "test": "static/light_screen_test.png",
        }
        self.set_image("test")

        self.angle = 0

    def move_to(self, position):
        self.position = [position[0] + self.offset[0], position[1] + self.offset[1]]

    def update_angle(self):
        mouse_pos = pygame.mouse.get_pos()
        player_pos = self.get_position_on_screen()
        #print(player_pos)

        mouse_distance = [mouse_pos[0] - player_pos[0], mouse_pos[1] - player_pos[1]]

        try:
            degree = math.degrees(math.atan(abs(mouse_distance[0])/abs(mouse_distance[1]))) # Calculate atan in degrees

            if mouse_distance[1] < 0 < mouse_distance[0]:  # Cursor in Quadrant II
                self.angle = degree
                print("A")
            elif mouse_distance[0] > 0 and mouse_distance[1] > 0:  # Cursor in Quadrant III
                self.angle = 180-degree
                print("B")
            elif mouse_distance[0] < 0 < mouse_distance[1]:  # Cursor in Quadrant VI
                self.angle = 180+degree
                print("C")
            else:  # Cursor in Quadrant I
                self.angle = 360-degree
                print("D")

        except ZeroDivisionError:

            if mouse_distance[0] == 0:
                if mouse_distance[1] > 0:  # Facing North
                    self.angle = 270
                else:  # Facing South
                    self.angle = 90
            elif mouse_distance[1] == 0:
                if mouse_distance[0] > 0:  # Facing East
                    self.angle = 0
                else:  # Facing West
                    self.angle = 180

    def tick(self):
        self.update_angle()
        self.set_image("test")
        self.image = pygame.transform.rotate(self.image, -self.angle)


class Monster(Sprite):

    def __init__(self, position):
        super().__init__(position)

        self.image_dict = {
            "idle": "static/shadow-monster.png",
            "left": "static/shadow-monster.png",
        }
        self.set_image("idle")

        self.isHunting = False
        self.isCollidingWithPlayer = False
        self.hunt_range = 200
        self.player_pos = []
        self.player_size = [32, 32]

    def move_random(self):
        collisions = self.get_screen_border_collisions()
        movement = [0, 0]

        if "left" not in collisions:
            if randint(0, 1):
                movement[0] += -self.movement_speed
            elif "right" not in collisions:
                if randint(0, 1):
                    movement[0] += self.movement_speed
        if "top" not in collisions:
            if randint(0, 1):
                movement[1] += -self.movement_speed
            elif "bottom" not in collisions:
                if randint(0, 1):
                    movement[1] += self.movement_speed

        self.move(movement)

    def move_towards_player(self):
        movement = [0, 0]
        if self.player_pos[0] - self.get_position_on_screen()[0] < 0:
            movement[0] += -self.movement_speed
        elif self.player_pos[0] - self.get_position_on_screen()[0] > 0:
            movement[0] += self.movement_speed

        if self.player_pos[1] - self.get_position_on_screen()[1] < 0:
            movement[1] += -self.movement_speed
        elif self.player_pos[1] - self.get_position_on_screen()[1] > 0:
            movement[1] += self.movement_speed

        self.move(movement)

    def check_collision_with_player(self):

        if (self.player_pos[0]-self.player_size[0]/3 <=
                self.get_position_on_screen()[0] <
                self.player_pos[0]+self.player_size[0]/3 and
                self.player_pos[1]-self.player_size[1]/3 <=
                self.get_position_on_screen()[1] <
                self.player_pos[1]+self.player_size[1]/3):
            self.isCollidingWithPlayer = True

    def tick(self):
        if self.isHunting:
            if not self.tick_count%2:
                self.move_towards_player()
            self.check_collision_with_player()

        self.tick_count += 1

    def __str__(self):
        return "Monster"
