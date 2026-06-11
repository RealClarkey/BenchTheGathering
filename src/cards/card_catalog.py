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
        Card("Knight", "Neutral", 20, attack=2),
        Card("Elf", "Nature", 20, attack=2),
        Card("Wizard", "Tech", 100, attack=1),
        Card("Troll", "Dark", 80, attack=3),
        Card("Ishani", "Nature", 80, attack=1),
        Card("Voltis", "Tech", 80, attack=2),
        Card("Sentinel", "Neutral", 100, attack=1),
        Card("Morvane", "Dark", 75, attack=2),
        Card("Thornroot", "Nature", 100, attack=1),
    ]


def create_mana_cards():
    return [
        Card(
            name="Mana Crystal",
            hero_type="Neutral",
            hit_points=0,
            card_type="Mana",
            mana_value=1,
        )
    ]


def create_skill_cards():
    return [
        Card(
            name="Battle Training",
            hero_type="Neutral",
            hit_points=0,
            card_type="Skill",
            effect="buff_attack",
            attack_bonus=1,
        )
    ]


def create_demo_card_pool(commander):
    cards = []

    for card in create_hero_cards():
        if card.name != commander.name:
            cards.append(card)

    cards.extend(create_mana_cards())
    cards.extend(create_skill_cards())

    return cards


def add_repeated_cards(deck, source_cards, amount):
    while len(deck) < amount:
        for card in source_cards:
            deck.append(card)

            if len(deck) == amount:
                break


def create_demo_deck(commander, target_size=30):
    hero_count = 12
    mana_count = 10
    skill_count = 8

    if target_size != 30:
        hero_count = target_size
        mana_count = 0
        skill_count = 0

    deck = []
    hero_cards = [
        card
        for card in create_hero_cards()
        if card.name != commander.name
    ]

    add_repeated_cards(deck, hero_cards, hero_count)
    add_repeated_cards(deck, create_mana_cards(), hero_count + mana_count)
    add_repeated_cards(deck, create_skill_cards(), hero_count + mana_count + skill_count)

    return deck
