from src.cards.hand import Hand
from src.gameplay.board import Board
from src.gameplay.player import Player


class PlayResult:
    def __init__(self, success, message=""):
        self.success = success
        self.message = message


class BattleState:
    def __init__(self, starting_hand):
        self.player = Player()
        self.player_hand = Hand(starting_hand)
        self.player_board = Board()

    def choose_player_hero(self, card):
        if self.player.hero is not None:
            return PlayResult(False, "Hero already exists")

        if not self.player_hand.remove(card):
            return PlayResult(False, "Card is not in hand")

        self.player.set_hero(card)
        return PlayResult(True)

    def play_card_to_player_battlefield(self, card):
        if card not in self.player_hand.cards:
            return PlayResult(False, "Card is not in hand")

        if not self.player_board.can_add_hero():
            return PlayResult(False, "Battlefield is full")

        self.player_hand.remove(card)
        self.player_board.add_hero(card)
        return PlayResult(True)
