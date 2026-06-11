from src.cards.deck import Deck
from src.cards.hand import Hand
from src.gameplay.board import Board
from src.gameplay.player import Player


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
    def __init__(self, player_hero, deck_cards, starting_hand_size=7, max_hand_size=7):
        self.player = Player()
        self.player.set_hero(player_hero)

        self.player_deck = Deck(deck_cards)
        self.player_deck.shuffle()

        self.player_hand = Hand(max_size=max_hand_size)
        self.player_discard_pile = []
        self.player_board = Board()

        self.draw_cards(starting_hand_size)

    def draw_cards(self, amount=1):
        drawn_cards = self.player_deck.draw(amount)
        discarded_cards = self.player_hand.add_cards(drawn_cards)
        self.player_discard_pile.extend(discarded_cards)

        return DrawResult(drawn_cards, discarded_cards)

    def play_card_to_player_battlefield(self, card):
        if card not in self.player_hand.cards:
            return PlayResult(False, "Card is not in hand")

        if not self.player_board.can_add_hero():
            return PlayResult(False, "Battlefield is full")

        self.player_hand.remove(card)
        self.player_board.add_hero(card)
        return PlayResult(True)
