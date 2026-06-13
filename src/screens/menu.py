import pygame

from src.assets import UIAssets


class MenuScreen:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont(None, 48)
        self.ui_assets = UIAssets()
        self.logo_image = self.ui_assets.scaled_to_fit(
            self.ui_assets.logo,
            (int(self.game.width * 0.70), int(self.game.height * 0.65)),
        )
        self.logo_rect = self.logo_image.get_rect()
        self.logo_rect.centerx = self.game.width // 2
        self.logo_rect.centery = int(self.game.height * 0.42)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.game.change_screen("player_hero_select")


    def update(self):
        pass

    def draw(self, screen):
        screen.fill((0, 0, 0))

        prompt_text = self.font.render("press space bar", True, (255, 255, 255))
        prompt_rect = prompt_text.get_rect(center=(self.game.width // 2, int(self.game.height * 0.82)))

        screen.blit(self.logo_image, self.logo_rect)
        screen.blit(prompt_text, prompt_rect)
