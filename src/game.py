import sys
import pygame

from src.screens.menu import MenuScreen
from src.screens.battle import BattleScreen


class Game:
    def __init__(self):
        pygame.init()

        #1280 x 720, 1536 x 864
        self.width = 1536
        self.height = 864



        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("BenchTheGathering")

        self.clock = pygame.time.Clock()
        self.running = True

        self.screens = {
            "menu": MenuScreen(self),
            "battle": BattleScreen(self)
        }

        self.current_screen = self.screens["menu"]

    def change_screen(self, screen_name):
        self.current_screen = self.screens[screen_name]

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            else:
                self.current_screen.handle_event(event)

    def update(self):
        self.current_screen.update()

    def draw(self):
        self.current_screen.draw(self.screen)
        pygame.display.flip()