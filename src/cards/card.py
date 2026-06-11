

class Card:
    def __init__(
        self,
        name,
        hero_type,
        hit_points,
        card_type="Hero",
        attack=0,
        mana_value=0,
        mana_cost=0,
        effect=None,
        attack_bonus=0,
    ):
        self.name = name
        self.card_type = card_type
        self.hero_type = hero_type
        self.hit_points = hit_points
        self.attack = attack
        self.mana_value = mana_value
        self.mana_cost = mana_cost
        self.effect = effect
        self.attack_bonus = attack_bonus

        # Optional / to be added later
        self.image = None
        self.buffs = []
        self.abilities = []
        self.evolution_abilities = []
        
'''
## Hero Card:
- Name
- Card Type (Hero)
- Hero Type (Dark, Nature, Tech, Neutral)
- Hit Points
- Pic (Image)
- Buffs (Icons)
- Abilities (description, attack damage, mana value)
- Evolution Abilities
'''

