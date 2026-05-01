import pygame
from src.cards.card import Card
from src.ui.hand_view import HandView

from src.cards.card import Card
from src.cards.ability import Ability
from src.cards.buff import Buff

from src.gameplay.player import Player


class BattleScreen:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont(None, 48)
        self.card_font = pygame.font.SysFont(None, 20)

        self.create_layout()
        self.create_cards()

        self.player = Player()
        self.selected_card = None

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
        # Dummy data for current development.
        fire_blast = Ability(name="Fire Blast", attack_damage=8, mana_cost=3)
        dark_inferno = Ability( name="Dark Inferno", attack_damage=15, mana_cost=6)

        burning = Buff(name="Burning", description="Deals 2 damage per turn")

        voldemort = Card(name="Voldemort", hero_type="Fire", hit_points=30)

        voldemort.abilities.append(fire_blast)
        voldemort.evolution_abilities.append(dark_inferno)
        voldemort.buffs.append(burning)

        knight = Card("Knight", "Neutral", 20)
        elf = Card("Elf", "Nature", 20)
        wizard = Card("Wizard", "Magic", 100)
        troll = Card("Troll", "Dark", 80)



        self.cards = [voldemort, knight, elf, wizard, troll]

    # Draw player hero from dropped card.
    def draw_player_hero(self, screen):
        pygame.draw.rect(screen,(0, 100, 100), self.player_hero_rect)

        if self.player.hero is None:
            text = self.font.render("Drop Here", True, (255, 255, 255))
            text_rect = text.get_rect(center=self.player_hero_rect.center)
            screen.blit(text, text_rect)
            return
        
        name_text = self.card_font.render(self.player.hero.name, True, (255, 255, 255))
        hp_text = self.card_font.render(f"HP: {self.player.current_hp}/{self.player.max_hp}", True, (255, 255, 255))
        mana_text = self.card_font.render(f"Mana: {self.player.current_mana}/{self.player.max_mana}", True, (255, 255, 255))

        screen.blit(name_text, (self.player_hero_rect.x + 15, self.player_hero_rect.y + 20))
        screen.blit(hp_text, (self.player_hero_rect.x + 15, self.player_hero_rect.y + 55))
        screen.blit(mana_text, (self.player_hero_rect.x + 15, self.player_hero_rect.y + 90))


    def handle_event(self, event):
        # ESC handling for current development
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                print("Returning to menu screen")
                self.game.change_screen("menu")

        # Let HandView process drag/drop first
        self.hand_view.handle_event(event)

        # Handles the result of the drop
        if self.hand_view.dropped_card:
            dropped_card = self.hand_view.dropped_card
            drop_pos = self.hand_view.drop_position

            if self.player_hero_rect.collidepoint(drop_pos):
                # Condition to only allow if no player hero selected
                if self.player.hero is None:
                    self.player.set_hero(dropped_card)
                    self.cards.remove(dropped_card)
                    self.hand_view.build_fan()
                else:
                    print("Hero already exists") # change this later to a ui pop up messaged

            # reset drop state
            self.hand_view.dropped_card = None
            self.hand_view.drop_position = None

        # Right click
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                card = self.get_card_under_mouse()

                if card:
                    self.selected_card = card


    def get_card_under_mouse(self):
        mouse_pos = pygame.mouse.get_pos()

        for card_view in reversed(self.hand_view.card_views):
            if card_view.rect().collidepoint(mouse_pos):
                return card_view.card
        
        return None
    

    def draw_card_info(self, screen, card):
        x = self.stats_rect.x + 10
        y = self.stats_rect.y + 20

        name_text = self.card_font.render(card.name, True, (255, 255, 255))
        type_text = self.card_font.render(f"Type: {card.hero_type}", True, (255, 255, 255))
        hp_text = self.card_font.render(f"HP: {card.hit_points}", True, (255, 255, 255))

        screen.blit(name_text, (x, y))
        screen.blit(type_text, (x, y + 30))
        screen.blit(hp_text, (x, y + 60))

        # abilities
        y_offset = 100
        for ability in card.abilities:
            ability_text = self.card_font.render(
                f"{ability.name} ({ability.mana_cost}) dmg:{ability.attack_damage}",
                True,
                (255, 255, 255)
            )
            screen.blit(ability_text, (x, y + y_offset))
            y_offset += 25


    def update(self):
        self.hand_view.update()




    def draw(self, screen):
        screen.fill((30, 110, 30))

        self.draw_zone(screen, self.enemy_battlefield_rect, (200, 50, 50), "Enemy Battlefield")
        self.draw_zone(screen, self.player_battlefield_rect, (255, 50, 50), "Player Battlefield")

        #Current stats
        pygame.draw.rect(screen, (0, 0, 255), self.stats_rect)

        if self.selected_card is None:
            text = self.font.render("Right click a card", True, (255, 255, 255))
            text_rect = text.get_rect(center=self.stats_rect.center)
            screen.blit(text, text_rect)
        else:
            self.draw_card_info(screen, self.selected_card)

        self.draw_zone(screen, self.next_rect, (255, 255, 0), "Next", text_colour=(0, 0, 0))
        self.draw_zone(screen, self.hand_rect, (55, 0, 150), "Hand")
        self.draw_player_hero(screen)
        self.draw_zone(screen, self.enemy_hero_rect, (255, 100, 100), "Enemy Hero")

        info_text = self.font.render("Press ESC to return to menu", True, (255, 255, 255))

        screen.blit(info_text, (330, 350))

        self.hand_view.draw(screen)

    def draw_zone(self, screen, rect, colour, label, text_colour=(255, 255, 255)):
        pygame.draw.rect(screen, colour, rect)
        text = self.font.render(label, True, text_colour)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)
