import pygame


class MenuScreen:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont(None, 48)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.game.change_screen("player_hero_select")


    def update(self):
        pass

    def draw(self, screen):
        screen.fill((40, 40, 90))

        title_text = self.font.render("MENU SCREEN", True, (255, 255, 255))
        info_text = self.font.render("Press SPACE to choose Player Hero", True, (255, 255, 255))

        screen.blit(title_text, (450, 250))
        screen.blit(info_text, (350, 350))
