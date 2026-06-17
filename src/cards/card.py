

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
        self.current_hit_points = hit_points
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

    def copy(self):
        card = Card(
            name=self.name,
            hero_type=self.hero_type,
            hit_points=self.hit_points,
            card_type=self.card_type,
            attack=self.attack,
            mana_value=self.mana_value,
            mana_cost=self.mana_cost,
            effect=self.effect,
            attack_bonus=self.attack_bonus,
        )
        card.current_hit_points = self.current_hit_points
        card.image = self.image
        card.buffs = list(self.buffs)
        card.abilities = list(self.abilities)
        card.evolution_abilities = list(self.evolution_abilities)
        return card
        
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

