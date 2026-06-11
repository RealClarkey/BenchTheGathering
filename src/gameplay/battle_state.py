from src.cards.deck import Deck
from src.cards.hand import Hand
from src.gameplay.board import Board
from src.gameplay.player import Player
from src.gameplay.turn_manager import TurnManager


class PlayResult:
    def __init__(self, success, message=""):
        self.success = success
        self.message = message


class DrawResult:
    def __init__(self, drawn_cards=None, discarded_cards=None):
        self.drawn_cards = list(drawn_cards or [])
        self.discarded_cards = list(discarded_cards or [])

    @property
    def success(self):
        return len(self.drawn_cards) > 0


class BattleState:
    def __init__(
        self,
        player_hero,
        deck_cards,
        starting_hand_size=7,
        max_hand_size=7,
        shuffle_deck=True,
    ):
        self.player = Player()
        self.player.set_hero(player_hero)

        self.player_deck = Deck(deck_cards)
        if shuffle_deck:
            self.player_deck.shuffle()

        self.player_hand = Hand(max_size=max_hand_size)
        self.player_discard_pile = []
        self.player_board = Board()
        self.turn_manager = TurnManager()
        self.resolved_phase_key = None
        self.has_played_mana_this_turn = False
        self.has_played_main_card_this_turn = False
        self.starting_hand_size = starting_hand_size
        self.shuffle_deck = shuffle_deck
        self.has_used_mulligan = False

        self.draw_starting_hand(starting_hand_size)

    def current_phase_key(self):
        return (self.turn_manager.turn_number, self.turn_manager.current_phase)

    def resolve_current_phase(self):
        phase_key = self.current_phase_key()

        if self.resolved_phase_key == phase_key:
            return None

        if self.turn_manager.current_phase == "start":
            self.player.refresh_mana()
            self.has_played_mana_this_turn = False
            self.has_played_main_card_this_turn = False

        if self.turn_manager.current_phase == "draw":
            result = self.draw_cards(1)
            self.resolved_phase_key = phase_key
            return result

        self.resolved_phase_key = phase_key
        return None

    def advance_phase(self):
        self.turn_manager.advance_phase()
        return self.resolve_current_phase()

    def mulligan(self):
        if self.has_used_mulligan:
            return PlayResult(False, "Mulligan already used")

        if self.turn_manager.turn_number != 1 or self.turn_manager.current_phase != "start":
            return PlayResult(False, "Mulligan only available at game start")

        self.player_deck.cards.extend(self.player_hand.cards)
        self.player_hand.cards.clear()

        if self.shuffle_deck:
            self.player_deck.shuffle()
        else:
            self.player_deck.cards.reverse()

        self.draw_starting_hand(self.starting_hand_size)
        self.has_used_mulligan = True

        return PlayResult(True, "Mulligan used")

    def draw_starting_hand(self, amount):
        result = self.draw_cards(amount)
        self.ensure_starting_hand_has_hero()
        return result

    def ensure_starting_hand_has_hero(self):
        if len(self.player_hand) == 0:
            return

        if any(card.card_type == "Hero" for card in self.player_hand.cards):
            return

        for deck_index, card in enumerate(self.player_deck.cards):
            if card.card_type != "Hero":
                continue

            replaced_card = self.player_hand.cards[0]
            self.player_hand.cards[0] = card
            self.player_deck.cards[deck_index] = replaced_card
            return

    def draw_cards(self, amount=1):
        drawn_cards = self.player_deck.draw(amount)
        discarded_cards = self.player_hand.add_cards(drawn_cards)
        self.player_discard_pile.extend(discarded_cards)

        return DrawResult(drawn_cards, discarded_cards)

    def play_mana_card(self, card):
        if card not in self.player_hand.cards:
            return PlayResult(False, "Card is not in hand")

        if card.card_type != "Mana":
            return PlayResult(False, "Only mana cards can be played as mana")

        if self.has_played_mana_this_turn:
            return PlayResult(False, "You can only play one mana card per turn")

        self.player.max_mana += card.mana_value
        self.player.current_mana += card.mana_value
        self.has_played_mana_this_turn = True
        self.player_hand.remove(card)
        self.player_discard_pile.append(card)

        return PlayResult(True)

    def play_skill_card(self, card, target):
        if card not in self.player_hand.cards:
            return PlayResult(False, "Card is not in hand")

        if card.card_type != "Skill":
            return PlayResult(False, "Only skill cards can be played as skills")

        if self.has_played_main_card_this_turn:
            return PlayResult(False, "You can only play one hero or skill card per turn")

        if target not in self.player_board.active_heroes:
            return PlayResult(False, "Skill target must be a hero on your battlefield")

        if self.player.current_mana < card.mana_cost:
            return PlayResult(False, "Not enough mana")

        self.player.current_mana -= card.mana_cost

        if card.effect == "buff_attack":
            target.attack += card.attack_bonus

        self.player_hand.remove(card)
        self.player_discard_pile.append(card)
        self.has_played_main_card_this_turn = True

        return PlayResult(True)

    def play_card_to_player_battlefield(self, card):
        if card not in self.player_hand.cards:
            return PlayResult(False, "Card is not in hand")

        if card.card_type != "Hero":
            return PlayResult(False, "Only hero cards can be played to the battlefield")

        if self.has_played_main_card_this_turn:
            return PlayResult(False, "You can only play one hero or skill card per turn")

        if not self.player_board.can_add_hero():
            return PlayResult(False, "Battlefield is full")

        self.player_hand.remove(card)
        self.player_board.add_hero(card)
        self.has_played_main_card_this_turn = True
        return PlayResult(True)
