from src.cards.ability import Ability
from src.cards.buff import Buff
from src.cards.card import Card


def create_hero_cards():
    shadow_bolt = Ability(name="Shadow Bolt", attack_damage=8, mana_cost=3)
    dark_inferno = Ability(name="Dark Inferno", attack_damage=15, mana_cost=6)
    burning = Buff(name="Burning", description="Deals 2 damage per turn")

    voldemort = Card(name="Voldemort", hero_type="Dark", hit_points=30)
    voldemort.abilities.append(shadow_bolt)
    voldemort.evolution_abilities.append(dark_inferno)
    voldemort.buffs.append(burning)

    return [
        voldemort,
        Card("Knight", "Neutral", 20),
        Card("Elf", "Nature", 20),
        Card("Wizard", "Tech", 100),
        Card("Troll", "Dark", 80),
        Card("Ishani", "Nature", 80),
        Card("Voltis", "Tech", 80),
        Card("Sentinel", "Neutral", 100),
        Card("Morvane", "Dark", 75),
        Card("Thornroot", "Nature", 100),
    ]


def create_demo_deck(commander, target_size=30):
    deck = []

    while len(deck) < target_size:
        for card in create_hero_cards():
            if card.name == commander.name:
                continue

            deck.append(card)

            if len(deck) == target_size:
                break

    return deck
