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
    assert skill_cards[0].mana_cost == 1


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


def test_only_one_mana_card_can_be_played_each_turn():
    commander = Card("Commander", "Dark", 30)
    first_mana = Card("Mana 1", "Neutral", 0, card_type="Mana", mana_value=1)
    second_mana = Card("Mana 2", "Neutral", 0, card_type="Mana", mana_value=1)
    battle_state = BattleState(
        commander,
        [first_mana, second_mana],
        starting_hand_size=2,
    )

    first_result = battle_state.play_mana_card(first_mana)
    second_result = battle_state.play_mana_card(second_mana)

    assert first_result.success
    assert not second_result.success
    assert second_result.message == "You can only play one mana card per turn"
    assert battle_state.player.max_mana == 1
    assert second_mana in battle_state.player_hand.cards


def test_start_phase_resets_mana_play_limit():
    commander = Card("Commander", "Dark", 30)
    first_mana = Card("Mana 1", "Neutral", 0, card_type="Mana", mana_value=1)
    second_mana = Card("Mana 2", "Neutral", 0, card_type="Mana", mana_value=1)
    battle_state = BattleState(
        commander,
        [first_mana, second_mana],
        starting_hand_size=2,
    )
    battle_state.play_mana_card(first_mana)

    battle_state.advance_phase()
    battle_state.advance_phase()
    battle_state.advance_phase()
    battle_state.advance_phase()
    battle_state.advance_phase()
    result = battle_state.play_mana_card(second_mana)

    assert result.success
    assert battle_state.player.max_mana == 2


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
        mana_cost=1,
    )
    battle_state = BattleState(
        commander,
        [hero, skill_card],
        starting_hand_size=2,
    )
    battle_state.player.current_mana = 1
    battle_state.player_board.add_hero(hero)

    result = battle_state.play_skill_card(skill_card, hero)

    assert result.success
    assert hero.attack == 3
    assert battle_state.player.current_mana == 0
    assert skill_card not in battle_state.player_hand.cards
    assert skill_card in battle_state.player_discard_pile


def test_skill_card_requires_enough_mana():
    commander = Card("Commander", "Dark", 30)
    hero = Card("Hero", "Nature", 20, attack=2)
    skill_card = Card(
        "Training",
        "Neutral",
        0,
        card_type="Skill",
        effect="buff_attack",
        attack_bonus=1,
        mana_cost=1,
    )
    battle_state = BattleState(
        commander,
        [hero, skill_card],
        starting_hand_size=2,
    )
    battle_state.player_board.add_hero(hero)

    result = battle_state.play_skill_card(skill_card, hero)

    assert not result.success
    assert result.message == "Not enough mana"
    assert hero.attack == 2
    assert skill_card in battle_state.player_hand.cards


def test_only_one_hero_or_skill_card_can_be_played_each_turn():
    commander = Card("Commander", "Dark", 30)
    first_hero = Card("Hero 1", "Nature", 20, attack=2)
    second_hero = Card("Hero 2", "Tech", 20, attack=2)
    battle_state = BattleState(
        commander,
        [first_hero, second_hero],
        starting_hand_size=2,
    )

    first_result = battle_state.play_card_to_player_battlefield(first_hero)
    second_result = battle_state.play_card_to_player_battlefield(second_hero)

    assert first_result.success
    assert not second_result.success
    assert second_result.message == "You can only play one hero or skill card per turn"
    assert second_hero in battle_state.player_hand.cards


def test_skill_card_uses_main_card_play_for_turn():
    commander = Card("Commander", "Dark", 30)
    hero = Card("Hero", "Nature", 20, attack=2)
    skill_card = Card(
        "Training",
        "Neutral",
        0,
        card_type="Skill",
        effect="buff_attack",
        attack_bonus=1,
        mana_cost=1,
    )
    second_hero = Card("Hero 2", "Tech", 20, attack=2)
    battle_state = BattleState(
        commander,
        [hero, skill_card, second_hero],
        starting_hand_size=3,
    )
    battle_state.player.current_mana = 1
    battle_state.player_board.add_hero(hero)

    skill_result = battle_state.play_skill_card(skill_card, hero)
    hero_result = battle_state.play_card_to_player_battlefield(second_hero)

    assert skill_result.success
    assert not hero_result.success
    assert hero_result.message == "You can only play one hero or skill card per turn"
    assert second_hero in battle_state.player_hand.cards


def test_start_phase_resets_main_card_play_limit():
    commander = Card("Commander", "Dark", 30)
    first_hero = Card("Hero 1", "Nature", 20, attack=2)
    second_hero = Card("Hero 2", "Tech", 20, attack=2)
    battle_state = BattleState(
        commander,
        [first_hero, second_hero],
        starting_hand_size=2,
    )
    battle_state.play_card_to_player_battlefield(first_hero)

    battle_state.advance_phase()
    battle_state.advance_phase()
    battle_state.advance_phase()
    battle_state.advance_phase()
    battle_state.advance_phase()
    result = battle_state.play_card_to_player_battlefield(second_hero)

    assert result.success
    assert second_hero in battle_state.player_board.active_heroes


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
