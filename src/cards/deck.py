import random


class Deck:
    def __init__(self, cards=None):
        self.cards = list(cards or [])

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self, amount=1):
        drawn_cards = []

        for _ in range(amount):
            if len(self.cards) == 0:
                break

            drawn_cards.append(self.cards.pop(0))

        return drawn_cards
