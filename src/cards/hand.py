class Hand:
    def __init__(self, cards=None, max_size=7):
        self.max_size = max_size
        self.cards = list(cards or [])

    def add_cards(self, cards):
        self.cards.extend(cards)
        return self.discard_excess()

    def discard_excess(self):
        if len(self.cards) <= self.max_size:
            return []

        excess_cards = self.cards[self.max_size:]
        del self.cards[self.max_size:]
        return excess_cards

    def remove(self, card):
        if card not in self.cards:
            return False

        self.cards.remove(card)
        return True

    def is_full(self):
        return len(self.cards) >= self.max_size

    def __len__(self):
        return len(self.cards)
