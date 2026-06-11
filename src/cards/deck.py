import random


class Deck:
    def __init__(self, cards=None):
        self.cards = list(cards or [])

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self, amount=1):
        drawn_cards = []

        for _ in range(max(0, amount)):
            if len(self.cards) == 0:
                break

            drawn_cards.append(self.cards.pop(0))

        return drawn_cards

    def is_empty(self):
        return len(self.cards) == 0

    def __len__(self):
        return len(self.cards)
