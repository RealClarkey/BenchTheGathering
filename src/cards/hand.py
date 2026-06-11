class Hand:
    def __init__(self, cards=None):
        self.cards = list(cards or [])

    def remove(self, card):
        if card not in self.cards:
            return False

        self.cards.remove(card)
        return True

    def __len__(self):
        return len(self.cards)
