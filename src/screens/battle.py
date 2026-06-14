import pygame
from src.ui.hand_view import HandView

from src.assets import UIAssets
from src.cards.card_catalog import create_default_enemy_setup, create_demo_deck
from src.gameplay.battle_state import BattleState, PlayResult


class BattleScreen:
    BATTLEFIELD_SLOT_COUNT = 4

    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont(None, 48)
        self.card_font = pygame.font.SysFont(None, 20)
        self.ui_assets = UIAssets()

        self.create_layout()
        self.create_scaled_assets()
        player_hero = self.game.selected_player_hero
        deck_cards = create_demo_deck(player_hero)
        enemy_hero, enemy_board_cards = create_default_enemy_setup()

        self.battle_state = BattleState(
            player_hero,
            deck_cards,
            starting_hand_size=7,
            enemy_hero=enemy_hero,
            enemy_board_cards=enemy_board_cards,
        )
        self.selected_card = None
        self.selected_attacker = None
        self.status_message = "Choose cards to play"

        self.hand_view = HandView(self.battle_state.player_hand.cards, self.hand_rect)

    def create_layout(self):
        #Based on screen resolution 1536(width) x 864(height)
        width = self.game.width
        height = self.game.height

        # Layout uses percentages of screen size so UI scales across resolutions
        # pygame.Rect format: (x, y, width, height)

        # Player battlefield area
        self.player_battlefield_rect = pygame.Rect(int(width * 0.20), int(height * 0.34), int(width * 0.60), int(height * 0.34))
        self.player_battlefield_rect.centerx = width // 2 

        slot_width = int(self.player_battlefield_rect.width * 0.20)
        slot_height = int(self.player_battlefield_rect.height * 0.75)
        slot_gap = int(self.player_battlefield_rect.width * 0.04)

        total_width = (slot_width * self.BATTLEFIELD_SLOT_COUNT) + (slot_gap * (self.BATTLEFIELD_SLOT_COUNT - 1))
        start_x = self.player_battlefield_rect.centerx - total_width // 2
        slot_y = self.player_battlefield_rect.centery - slot_height // 2

        self.player_battlefield_slots = []

        for i in range(self.BATTLEFIELD_SLOT_COUNT):
            slot_rect = pygame.Rect(
                start_x + i * (slot_width + slot_gap),
                slot_y,
                slot_width,
                slot_height
            )
            self.player_battlefield_slots.append(slot_rect)


        # Enemy battlefield area
        self.enemy_battlefield_rect = pygame.Rect(int(width * 0.20), 0, int(width * 0.60), int(height * 0.34))
        self.enemy_battlefield_rect.centerx = width // 2 

        enemy_slot_width = int(self.enemy_battlefield_rect.width * 0.20)
        enemy_slot_height = int(self.enemy_battlefield_rect.height * 0.75)
        enemy_slot_gap = int(self.enemy_battlefield_rect.width * 0.04)

        enemy_total_width = (enemy_slot_width * self.BATTLEFIELD_SLOT_COUNT) + (enemy_slot_gap * (self.BATTLEFIELD_SLOT_COUNT - 1))
        enemy_start_x = self.enemy_battlefield_rect.centerx - enemy_total_width // 2
        enemy_slot_y = self.enemy_battlefield_rect.centery - enemy_slot_height // 2

        self.enemy_battlefield_slots = []

        for i in range(self.BATTLEFIELD_SLOT_COUNT):
            slot_rect = pygame.Rect(
                enemy_start_x + i * (enemy_slot_width + enemy_slot_gap),
                enemy_slot_y,
                enemy_slot_width,
                enemy_slot_height
            )
            self.enemy_battlefield_slots.append(slot_rect)
        
        # Game stats area
        self.stats_rect = pygame.Rect(0, 0, int(width * 0.20), 330)
        self.stats_rect.topright = (width, 0)
        
        # Next action area
        self.next_rect = self.ui_assets.next_turn.get_rect()
        self.next_rect.bottomright = (width - 15, height - 15)

        # Mulligan area
        self.mulligan_rect = pygame.Rect(0, 0, self.next_rect.width, 60)
        self.mulligan_rect.bottomright = (self.next_rect.right, self.next_rect.top - 15)

        # Hand area (cards) THIS WILL NEED TO BE LOOKED AT DUE TO MOVING HAND FEATURE OVER
        self.hand_rect = pygame.Rect(0, 0, int(width * 0.60), int(height * 0.33))
        self.hand_rect.centerx = width // 2
        self.hand_rect.bottom = height

        # Player hero area
        self.player_hero_rect = self.ui_assets.player_hero.get_rect()
        self.player_hero_rect.bottom = height

        # Enemy hero area
        self.enemy_hero_rect = self.ui_assets.enemy_hero.get_rect()

        # Status message area
        self.status_rect = pygame.Rect(int(width * 0.25), int(height * 0.54), int(width * 0.50), 45)

    def create_scaled_assets(self):
        self.background_image = self.ui_assets.scaled(
            self.ui_assets.background,
            (self.game.width, self.game.height),
        )
        self.player_hero_image = self.ui_assets.player_hero
        self.enemy_hero_image = self.ui_assets.enemy_hero
        self.next_turn_image = self.ui_assets.next_turn
    
    def draw_player_hero(self, screen):
        screen.blit(self.player_hero_image, self.player_hero_rect)

        player = self.battle_state.player

        if player.hero is None:
            text = self.font.render("Drop Here", True, (255, 255, 255))
            text_rect = text.get_rect(center=self.player_hero_rect.center)
            screen.blit(text, text_rect)
            return
        
        name_text = self.card_font.render(player.hero.name, True, (255, 255, 255))
        hp_text = self.card_font.render(f"{player.current_hp}/{player.max_hp}", True, (255, 255, 255))
        mana_text = self.card_font.render(f"{player.current_mana}/{player.max_mana}", True, (255, 255, 255))

        screen.blit(name_text, (self.player_hero_rect.x + 95, self.player_hero_rect.y + 12))
        screen.blit(hp_text, (self.player_hero_rect.x + 65, self.player_hero_rect.y + 205))
        screen.blit(mana_text, (self.player_hero_rect.x + 175, self.player_hero_rect.y + 205))


    def handle_event(self, event):
        # ESC handling for current development
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.set_status_message("Returning to menu")
                self.game.change_screen("menu")

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.next_rect.collidepoint(event.pos):
                result = self.battle_state.advance_phase()
                self.selected_attacker = None

                if result is not None:
                    self.handle_draw_result(result)

            if event.button == 1 and self.mulligan_rect.collidepoint(event.pos):
                result = self.battle_state.mulligan()
                self.handle_mulligan_result(result)

        # Let HandView process drag/drop first
        self.hand_view.handle_event(event)

        # Handles the result of the drop
        if self.hand_view.dropped_card:
            dropped_card = self.hand_view.dropped_card
            drop_pos = self.hand_view.drop_position

            if self.player_hero_rect.collidepoint(drop_pos):
                if dropped_card.card_type == "Mana":
                    result = self.battle_state.play_mana_card(dropped_card)
                    self.handle_play_result(result)
                else:
                    self.set_status_message("Player Hero is already selected")
            else:
                for index, slot in enumerate(self.player_battlefield_slots):
                    if slot.collidepoint(drop_pos):
                        result = self.play_card_on_battlefield_slot(dropped_card, index)
                        self.handle_play_result(result)
                        break

            # reset drop state
            self.hand_view.dropped_card = None
            self.hand_view.drop_position = None

        # Right click
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.handle_combat_click(event.pos)

            if event.button == 3:
                card = self.get_card_under_mouse()

                if card:
                    self.selected_card = card

    def set_status_message(self, message):
        self.status_message = message

    def handle_combat_click(self, pos):
        if self.battle_state.turn_manager.current_phase != "action":
            return

        attacker = self.get_player_battlefield_card_at_pos(pos)

        if attacker is not None:
            self.selected_attacker = attacker
            self.set_status_message(f"Selected attacker: {attacker.name}")
            return

        if self.selected_attacker is None:
            return

        target = self.get_enemy_target_at_pos(pos)

        if target is None:
            return

        result = self.battle_state.attack(self.selected_attacker, target)

        if result.success:
            if result.game_over:
                self.set_status_message(f"{self.selected_attacker.name} dealt {result.damage} damage. You win!")
            else:
                self.set_status_message(f"{self.selected_attacker.name} spent 1 mana and dealt {result.damage} damage")
            self.selected_attacker = None
        elif result.message:
            self.set_status_message(result.message)

    def handle_play_result(self, result):
        if result.success:
            self.hand_view.build_fan()
            self.set_status_message("Card played")
        elif result.message:
            self.set_status_message(result.message)

    def play_card_on_battlefield_slot(self, card, slot_index):
        if card.card_type == "Skill":
            active_heroes = self.battle_state.player_board.active_heroes

            if slot_index >= len(active_heroes):
                return PlayResult(False, "Skill target must be a hero on your battlefield")

            return self.battle_state.play_skill_card(card, active_heroes[slot_index])

        return self.battle_state.play_card_to_player_battlefield(card)

    def handle_draw_result(self, result):
        if not result.success:
            self.set_status_message("Deck is empty")
            return

        self.hand_view.build_fan()

        if result.discarded_cards:
            self.set_status_message("Hand is full. Excess drawn cards were discarded.")
        else:
            self.set_status_message("Drew 1 card")

    def handle_mulligan_result(self, result):
        if result.success:
            self.hand_view.build_fan()

        if result.message:
            self.set_status_message(result.message)

    def get_card_under_mouse(self):
        mouse_pos = pygame.mouse.get_pos()

        for card_view in reversed(self.hand_view.card_views):
            if card_view.rect().collidepoint(mouse_pos):
                return card_view.card
            
        for i, card in enumerate(self.battle_state.player_board.active_heroes):
            if self.get_card_rect_for_slot(self.player_battlefield_slots[i]).collidepoint(mouse_pos):
                return card

        for i, card in enumerate(self.battle_state.enemy_board.active_heroes):
            if self.get_card_rect_for_slot(self.enemy_battlefield_slots[i]).collidepoint(mouse_pos):
                return card

        if self.enemy_hero_rect.collidepoint(mouse_pos):
            return self.battle_state.enemy.hero
        
        return None

    def get_card_rect_for_slot(self, slot):
        card_rect = pygame.Rect(0, 0, int(slot.width * 0.75), int(slot.height * 0.85))
        card_rect.center = slot.center
        return card_rect

    def get_player_battlefield_card_at_pos(self, pos):
        for i, card in enumerate(self.battle_state.player_board.active_heroes):
            if self.get_card_rect_for_slot(self.player_battlefield_slots[i]).collidepoint(pos):
                return card

        return None

    def get_enemy_target_at_pos(self, pos):
        for i, card in enumerate(self.battle_state.enemy_board.active_heroes):
            if self.get_card_rect_for_slot(self.enemy_battlefield_slots[i]).collidepoint(pos):
                return card

        if self.enemy_hero_rect.collidepoint(pos):
            return self.battle_state.enemy.hero

        return None
    
    def draw_player_battlefield_slots(self, screen):
        pass

    def draw_enemy_battlefield_slots(self, screen):
        pass
    
    def draw_player_battlefield_cards(self, screen):
        for i, card in enumerate(self.battle_state.player_board.active_heroes):
            slot = self.player_battlefield_slots[i]

            rect = self.get_card_rect_for_slot(slot)

            pygame.draw.rect(screen, (220, 220, 220), rect)
            border_colour = (255, 215, 0) if card == self.selected_attacker else (0, 0, 0)
            pygame.draw.rect(screen, border_colour, rect, 3)

            self.draw_battlefield_card_text(screen, card, rect)

    def draw_enemy_battlefield_cards(self, screen):
        for i, card in enumerate(self.battle_state.enemy_board.active_heroes):
            slot = self.enemy_battlefield_slots[i]
            rect = self.get_card_rect_for_slot(slot)

            pygame.draw.rect(screen, (220, 220, 220), rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 2)

            self.draw_battlefield_card_text(screen, card, rect)

    def draw_battlefield_card_text(self, screen, card, rect):
        name_text = self.card_font.render(card.name, True, (0, 0, 0))
        hp_text = self.card_font.render(f"{card.current_hit_points}/{card.hit_points}", True, (0, 0, 0))
        attack_text = self.card_font.render(f"ATK: {card.attack}", True, (0, 0, 0))
        cost_text = self.card_font.render("Cost: 1", True, (0, 0, 0))

        screen.blit(name_text, (rect.x + 8, rect.y + 18))
        screen.blit(hp_text, (rect.x + 8, rect.y + 48))
        screen.blit(attack_text, (rect.x + 8, rect.y + 78))
        screen.blit(cost_text, (rect.x + 8, rect.y + 108))
            

    def draw_card_info(self, screen, card):
        x = self.stats_rect.x + 10
        y = self.stats_rect.y + 20

        name_text = self.card_font.render(card.name, True, (255, 255, 255))
        type_text = self.card_font.render(f"Type: {card.hero_type}", True, (255, 255, 255))
        card_type_text = self.card_font.render(f"Card: {card.card_type}", True, (255, 255, 255))
        hp_text = self.card_font.render(f"HP: {card.hit_points}", True, (255, 255, 255))

        screen.blit(name_text, (x, y))
        screen.blit(type_text, (x, y + 30))
        screen.blit(card_type_text, (x, y + 60))
        screen.blit(hp_text, (x, y + 90))

        if card.card_type == "Hero":
            current_hp_text = self.card_font.render(f"Current HP: {card.current_hit_points}", True, (255, 255, 255))
            attack_text = self.card_font.render(f"Attack: {card.attack}", True, (255, 255, 255))
            screen.blit(current_hp_text, (x, y + 120))
            screen.blit(attack_text, (x, y + 145))

        if card.card_type == "Mana":
            mana_text = self.card_font.render(f"Adds Mana: {card.mana_value}", True, (255, 255, 255))
            screen.blit(mana_text, (x, y + 120))

        if card.card_type == "Skill":
            skill_text = self.card_font.render(f"Attack Buff: +{card.attack_bonus}", True, (255, 255, 255))
            screen.blit(skill_text, (x, y + 120))
            cost_text = self.card_font.render(f"Cost: {card.mana_cost}", True, (255, 255, 255))
            screen.blit(cost_text, (x, y + 145))

        # abilities
        y_offset = 155
        for ability in card.abilities:
            ability_text = self.card_font.render(
                f"{ability.name} ({ability.mana_cost}) dmg:{ability.attack_damage}",
                True,
                (255, 255, 255)
            )
            screen.blit(ability_text, (x, y + y_offset))
            y_offset += 25

    def draw_deck_info(self, screen):
        x = self.stats_rect.x + 10
        y = self.stats_rect.bottom - 150

        phase_text = self.card_font.render(f"Phase: {self.battle_state.turn_manager.current_phase}", True, (255, 255, 255))
        turn_text = self.card_font.render(f"Turn: {self.battle_state.turn_manager.turn_number}", True, (255, 255, 255))
        deck_text = self.card_font.render(f"Deck: {len(self.battle_state.player_deck)}", True, (255, 255, 255))
        hand_text = self.card_font.render(f"Hand: {len(self.battle_state.player_hand)}/{self.battle_state.player_hand.max_size}", True, (255, 255, 255))
        discard_text = self.card_font.render(f"Discard: {len(self.battle_state.player_discard_pile)}", True, (255, 255, 255))

        screen.blit(phase_text, (x, y))
        screen.blit(turn_text, (x, y + 25))
        screen.blit(deck_text, (x, y + 50))
        screen.blit(hand_text, (x, y + 75))
        screen.blit(discard_text, (x, y + 100))

    def draw_enemy_hero(self, screen):
        screen.blit(self.enemy_hero_image, self.enemy_hero_rect)

        enemy = self.battle_state.enemy

        name_text = self.card_font.render(enemy.hero.name, True, (255, 255, 255))
        hp_text = self.card_font.render(f"{enemy.hero.current_hit_points}/{enemy.hero.hit_points}", True, (255, 255, 255))
        mana_text = self.card_font.render(f"{enemy.current_mana}/{enemy.max_mana}", True, (255, 255, 255))

        screen.blit(name_text, (self.enemy_hero_rect.x + 95, self.enemy_hero_rect.y + 12))
        screen.blit(hp_text, (self.enemy_hero_rect.x + 65, self.enemy_hero_rect.y + 215))
        screen.blit(mana_text, (self.enemy_hero_rect.x + 175, self.enemy_hero_rect.y + 215))

    def draw_status_message(self, screen):
        pygame.draw.rect(screen, (20, 20, 20), self.status_rect)
        pygame.draw.rect(screen, (255, 255, 255), self.status_rect, 2)

        text = self.card_font.render(self.status_message, True, (255, 255, 255))
        text_rect = text.get_rect(center=self.status_rect.center)
        screen.blit(text, text_rect)


    def update(self):
        self.hand_view.update()




    def draw(self, screen):
        screen.blit(self.background_image, (0, 0))

        self.draw_enemy_battlefield_slots(screen)
        self.draw_enemy_battlefield_cards(screen)
        self.draw_player_battlefield_slots(screen)
        self.draw_player_battlefield_cards(screen)

        #Current stats
        pygame.draw.rect(screen, (0, 0, 255), self.stats_rect)

        if self.selected_card is None:
            text = self.font.render("Right click a card", True, (255, 255, 255))
            text_rect = text.get_rect(center=self.stats_rect.center)
            screen.blit(text, text_rect)
        else:
            self.draw_card_info(screen, self.selected_card)

        self.draw_deck_info(screen)

        self.draw_zone(screen, self.mulligan_rect, (230, 230, 230), "Mulligan", text_colour=(0, 0, 0))
        self.draw_next_phase_button(screen)
        self.draw_player_hero(screen)
        self.draw_enemy_hero(screen)

        self.hand_view.draw(screen)
        self.draw_status_message(screen)

    def draw_next_phase_button(self, screen):
        screen.blit(self.next_turn_image, self.next_rect)

    def draw_zone(self, screen, rect, colour, label, text_colour=(255, 255, 255)):
        pygame.draw.rect(screen, colour, rect)
        text = self.font.render(label, True, text_colour)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)
