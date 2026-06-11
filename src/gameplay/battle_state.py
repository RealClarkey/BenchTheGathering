from src.cards.deck import Deck
from src.cards.hand import Hand
from src.gameplay.board import Board
from src.gameplay.player import Player


class PlayResult:
    def __init__(self, success, message=""):
        self.success = success
        self.message = message


class BattleState:
    def __init__(self, player_hero, deck_cards, starting_hand_size=7):
        self.player = Player()
        self.player.set_hero(player_hero)

        self.player_deck = Deck(deck_cards)
        self.player_deck.shuffle()

        self.player_hand = Hand(self.player_deck.draw(starting_hand_size))
        self.player_board = Board()

    def play_card_to_player_battlefield(self, card):
        if card not in self.player_hand.cards:
            return PlayResult(False, "Card is not in hand")

        if not self.player_board.can_add_hero():
            return PlayResult(False, "Battlefield is full")

        self.player_hand.remove(card)
        self.player_board.add_hero(card)
        return PlayResult(True)
