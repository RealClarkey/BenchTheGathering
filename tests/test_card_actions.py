from src.cards.card import Card
from src.cards.card_catalog import create_demo_deck, create_mana_cards, create_skill_cards
from src.gameplay.battle_state import BattleState


def test_catalog_includes_mana_and_skill_cards():
    mana_cards = create_mana_cards()
    skill_cards = create_skill_cards()

    assert mana_cards[0].card_type == "Mana"
    assert mana_cards[0].mana_value == 1
    assert skill_cards[0].card_type == "Skill"
    assert skill_cards[0].effect == "buff_attack"
    assert skill_cards[0].attack_bonus == 1


def test_demo_deck_includes_hero_mana_and_skill_cards():
    commander = Card("Commander", "Dark", 30)

    deck = create_demo_deck(commander, target_size=30)
    card_types = {card.card_type for card in deck}

    assert {"Hero", "Mana", "Skill"}.issubset(card_types)


def test_demo_deck_uses_prototype_card_type_ratio():
    commander = Card("Ishani", "Nature", 80)

    deck = create_demo_deck(commander, target_size=30)
    card_type_counts = {
        "Hero": len([card for card in deck if card.card_type == "Hero"]),
        "Mana": len([card for card in deck if card.card_type == "Mana"]),
        "Skill": len([card for card in deck if card.card_type == "Skill"]),
    }

    assert card_type_counts == {
        "Hero": 12,
        "Mana": 10,
        "Skill": 8,
    }


def test_playing_mana_card_increases_player_mana():
    commander = Card("Commander", "Dark", 30)
    mana_card = Card("Mana", "Neutral", 0, card_type="Mana", mana_value=1)
    battle_state = BattleState(commander, [mana_card], starting_hand_size=1)

    result = battle_state.play_mana_card(mana_card)

    assert result.success
    assert battle_state.player.max_mana == 1
    assert battle_state.player.current_mana == 1
    assert mana_card not in battle_state.player_hand.cards
    assert mana_card in battle_state.player_discard_pile


def test_attack_buff_skill_increases_battlefield_hero_attack():
    commander = Card("Commander", "Dark", 30)
    hero = Card("Hero", "Nature", 20, attack=2)
    skill_card = Card(
        "Training",
        "Neutral",
        0,
        card_type="Skill",
        effect="buff_attack",
        attack_bonus=1,
    )
    battle_state = BattleState(
        commander,
        [hero, skill_card],
        starting_hand_size=2,
    )
    battle_state.play_card_to_player_battlefield(hero)

    result = battle_state.play_skill_card(skill_card, hero)

    assert result.success
    assert hero.attack == 3
    assert skill_card not in battle_state.player_hand.cards
    assert skill_card in battle_state.player_discard_pile


def test_attack_buff_skill_requires_battlefield_hero_target():
    commander = Card("Commander", "Dark", 30)
    hero = Card("Hero", "Nature", 20, attack=2)
    skill_card = Card(
        "Training",
        "Neutral",
        0,
        card_type="Skill",
        effect="buff_attack",
        attack_bonus=1,
    )
    battle_state = BattleState(
        commander,
        [hero, skill_card],
        starting_hand_size=2,
    )

    result = battle_state.play_skill_card(skill_card, hero)

    assert not result.success
    assert result.message == "Skill target must be a hero on your battlefield"
    assert hero.attack == 2
    assert skill_card in battle_state.player_hand.cards
