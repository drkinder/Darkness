import pygame
from sprites import Player
from levels import levels


class MainGame:

    def __init__(self):
        pygame.init()
        self.display_size = (800, 600)
        self.screen = pygame.display.set_mode(self.display_size)
        self.clock = pygame.time.Clock()

        self.is_game_running = True
        self.is_night = False

        self.runtime = 0
        self.current_level = levels.Level01()

        self.main()

    def main(self):

        while self.is_game_running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_game_running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.is_night = not self.is_night

            self.draw_screen()

            if self.current_level.sprites[0].isLive:
                self.current_level.handle_event(pygame.key.get_pressed())
                self.current_level.tick()
            else:
                self.death()
                pygame.display.update()

            self.clock.tick(60)
            self.runtime += 1

    def draw_screen(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.current_level.map, self.current_level.map_position)
        self.draw_live_sprites()
        pygame.display.flip()

    def draw_live_sprites(self):
        for sprite in self.current_level.sprites:
            if sprite.isLive:
                self.screen.blit(sprite.image, sprite.position)

                if str(sprite) == "Player":
                    if self.is_night:
                        if not self.runtime%10:
                            self.draw_darkness(sprite.flashlight)

    def draw_darkness(self, flashlight):
        for y in range(self.display_size[1]+1):
            for x in range(self.display_size[0]+1):
                coords = (x, y)
                if not flashlight.is_point_between_light_lines(coords):
                    self.screen.set_at(coords, (0, 0, 0))
                    print("BLACK")
                '''
                coords = [x, y]
                # flashlight.is_point_between_light_lines(coords) or
                if coords not in ((100, 100),(101, 100),(102, 100),(100, 101),(100, 102),(101, 101),(102, 102)):
                    self.screen.set_at(coords, (0, 0, 0))
                else:
                    print("LIGHT")
                '''

    def switch_screen_color(self):
        if self.screen_color == (0, 0, 0):
            self.screen_color = (255, 255, 255)
        else:
            self.screen_color = (0, 0, 0)

    def text_objects(self, text, font):
        text_surface = font.render(text, True, (0, 0, 0))
        return text_surface, text_surface.get_rect()

    def message_display(self, text):
        largeText = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = self.text_objects(text, largeText)
        TextRect.center = ((self.display_size[0] / 2), (self.display_size[1] / 2))
        self.screen.blit(TextSurf, TextRect)

    def death(self):
        self.message_display("You Died!")


if __name__ == "__main__":
    game = MainGame()
