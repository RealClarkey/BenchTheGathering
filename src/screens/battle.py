import pygame
from src.cards.card import Card
from src.ui.hand_view import HandView

from src.cards.card import Card
from src.cards.ability import Ability
from src.cards.buff import Buff


class BattleScreen:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont(None, 48)
        self.card_font = pygame.font.SysFont(None, 20)

        self.create_layout()
        self.create_cards()

        self.hand_view = HandView(self.cards, self.hand_rect)

    def create_layout(self):
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
    
    def create_cards(self):
        fire_blast = Ability(name="Fire Blast", attack_damage=8, mana_cost=3)
        dark_inferno = Ability( name="Dark Inferno", attack_damage=15, mana_cost=6)

        burning = Buff(name="Burning", description="Deals 2 damage per turn")

        voldemort = Card(name="Voldemort", hero_type="Fire", hit_points=30)

        voldemort.abilities.append(fire_blast)
        voldemort.evolution_abilities.append(dark_inferno)
        voldemort.buffs.append(burning)

        knight = Card("Knight", "Neutral", 20)
        elf = Card("Elf", "Nature", 20)



        self.cards = [voldemort, knight, elf]

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

        self.draw_zone(screen, self.enemy_battlefield_rect, (200, 50, 50), "Enemy Battlefield")
        self.draw_zone(screen, self.player_battlefield_rect, (255, 50, 50), "Player Battlefield")
        self.draw_zone(screen, self.stats_rect, (0, 0, 255), "Current Stats")
        self.draw_zone(screen, self.next_rect, (255, 255, 0), "Next", text_colour=(0, 0, 0))
        self.draw_zone(screen, self.hand_rect, (55, 0, 150), "Hand")
        self.draw_zone(screen, self.player_hero_rect, (0, 100, 100), "Player Hero")
        self.draw_zone(screen, self.enemy_hero_rect, (255, 100, 100), "Enemy Hero")

        info_text = self.font.render("Press ESC to return to menu", True, (255, 255, 255))

        screen.blit(info_text, (330, 350))

        self.hand_view.draw(screen)

    def draw_zone(self, screen, rect, colour, label, text_colour=(255, 255, 255)):
        pygame.draw.rect(screen, colour, rect)
        text = self.font.render(label, True, text_colour)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)
