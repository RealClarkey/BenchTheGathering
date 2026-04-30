

class Card:
    def __init__(self, name, hero_type, hit_points):
        self.name = name
        self.hero_type = hero_type
        self.hit_points = hit_points

        # Optional / to be added later
        self.image = None
        self.buffs = []
        self.abilities = []
        self.evolution_abilities = []
        
'''
## Hero Card:
- Name
- Hero Type (Fire, Nature, Tech, Neutral)
- Hit Points
- Pic (Image)
- Buffs (Icons)
- Abilities (description, attack damage, mana value)
- Evolution Abilities
'''

