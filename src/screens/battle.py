import pygame
from src.cards.card import Card
from src.ui.hand_view import HandView


class BattleScreen:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont(None, 48)
        self.card_font = pygame.font.SysFont(None, 20)

        #Based on screen resolution 1536(width) x 864(height)
        width = self.game.width
        height = self.game.height

        # Layout uses percentages of screen size so UI scales across resolutions
        # pygame.Rect format: (x, y, width, height)

        # Player battlefield area
        self.player_battlefield_rect = pygame.Rect(int(width * 0.20), int(height * 0.34), int(width * 0.60), int(height * 0.34))
        self.player_battlefield_rect.centerx = width // 2 

        # Enemy battlefield area
        self.enemy_battlefield_rect = pygame.Rect(int(width * 0.20), 0, int(width * 0.60), int(height * 0.34))
        self.enemy_battlefield_rect.centerx = width // 2 
        
        # Game stats area
        self.stats_rect = pygame.Rect(0, 0, int(width * 0.20), 330)
        self.stats_rect.topright = (width, 0)
        
        # Next action area
        self.next_rect = pygame.Rect(int(width * 0.80), int(height * 0.90), int(width * 0.19), int(height * 0.070))

        # Hand area (cards) THIS WILL NEED TO BE LOOKED AT DUE TO MOVING HAND FEATURE OVER
        self.hand_rect = pygame.Rect(0, 0, int(width * 0.60), int(height * 0.33))
        self.hand_rect.centerx = width // 2
        self.hand_rect.bottom = height

        # Player hero area
        self.player_hero_rect = pygame.Rect(0, 0, int(width * 0.20), int(width * 0.20))
        self.player_hero_rect.bottom = height

        # Enemy hero area
        self.enemy_hero_rect = pygame.Rect(0, 0, int(width * 0.20), int(width * 0.20))

        self.cards = [
            Card("Voldemort", 10),
            Card("AM-Wizard", 8),
            Card("SS-Animal", 11),
            Card("LC-Elf", 11),
            Card("JP-Giant", 11),
            Card("NP-Treeant", 11),
            Card("KitKat", 9)
            
        ]

        self.hand_view = HandView(self.cards, self.hand_rect)


    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                print("Returning to menu screen")
                self.game.change_screen("menu")

        self.hand_view.handle_event(event)

    

    def update(self):
        self.hand_view.update()

    def draw(self, screen):
        screen.fill((30, 110, 30))

        # Player Battlefield Area
        pygame.draw.rect(screen, (255, 50, 50), self.player_battlefield_rect) 
        text = self.font.render("Battle Field", True, (255, 255, 255))
        text_rect = text.get_rect(center=self.player_battlefield_rect.center)
        screen.blit(text, text_rect)

        # Enemy Battlefield Area
        pygame.draw.rect(screen, (200, 50, 50), self.enemy_battlefield_rect) 
        text = self.font.render("Battle Field", True, (150, 255, 255))
        text_rect = text.get_rect(center=self.enemy_battlefield_rect.center)
        screen.blit(text, text_rect)

        # Card Area
        pygame.draw.rect(screen, (0, 0, 255), self.stats_rect) 
        text = self.font.render("Current Stats", True, (255, 255, 255))
        text_rect = text.get_rect(center=self.stats_rect.center)
        screen.blit(text, text_rect)

        # Next Area
        pygame.draw.rect(screen, (255, 255, 0), self.next_rect) 
        text = self.font.render("Next Field", True, (255, 255, 255))
        text_rect = text.get_rect(center=self.next_rect.center)
        screen.blit(text, text_rect)

        # Hand Area
        pygame.draw.rect(screen, (55, 0, 150), self.hand_rect) 
        text = self.font.render("Hand Field", True, (255, 255, 255))
        text_rect = text.get_rect(center=self.hand_rect.center)
        screen.blit(text, text_rect)

        # Player Hero Area
        pygame.draw.rect(screen, (0, 100, 100), self.player_hero_rect) 
        text = self.font.render("Player", True, (255, 255, 255))
        text_rect = text.get_rect(center=self.player_hero_rect.center)
        screen.blit(text, text_rect)

        # Enemy Hero Area
        pygame.draw.rect(screen, (255, 100, 100), self.enemy_hero_rect) 
        text = self.font.render("Enemy", True, (255, 255, 255))
        text_rect = text.get_rect(center=self.enemy_hero_rect.center)
        screen.blit(text, text_rect)

        info_text = self.font.render("Press ESC to return to menu", True, (255, 255, 255))

        screen.blit(info_text, (330, 350))

        self.hand_view.draw(screen)