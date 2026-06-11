
class Player:
    def __init__(self):
        self.hero = None

        self.max_hp = 0
        self.current_hp = 0

        self.max_mana = 0
        self.current_mana = 0
    
    def set_hero(self, card):
        self.hero = card

        self.max_hp = card.hit_points
        self.current_hp = self.max_hp

        self.max_mana = 0
        self.current_mana = 0


