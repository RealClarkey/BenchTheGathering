class Board:
    def __init__(self, max_active_heroes=3):
        self.max_active_heroes = max_active_heroes
        self.active_heroes = []

    def can_add_hero(self):
        return len(self.active_heroes) < self.max_active_heroes

    def add_hero(self, card):
        if not self.can_add_hero():
            return False

        self.active_heroes.append(card)
        return True

    def remove_hero(self, card):
        if card not in self.active_heroes:
            return False

        self.active_heroes.remove(card)
        return True
