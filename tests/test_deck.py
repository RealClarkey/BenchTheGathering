from src.cards.card import Card
from src.cards.card_catalog import create_demo_deck
from src.cards.deck import Deck
from src.cards.hand import Hand
from src.gameplay.battle_state import BattleState


def test_deck_draw_removes_cards_from_deck():
    deck = Deck(["A", "B", "C"])

    drawn_cards = deck.draw(2)

    assert drawn_cards == ["A", "B"]
    assert deck.cards == ["C"]


def test_deck_draw_stops_when_deck_is_empty():
    deck = Deck(["A"])

    drawn_cards = deck.draw(3)

    assert drawn_cards == ["A"]
    assert deck.is_empty()


def test_hand_discards_excess_cards_over_max_size():
    hand = Hand(["A", "B"], max_size=3)

    discarded_cards = hand.add_cards(["C", "D"])

    assert hand.cards == ["A", "B", "C"]
    assert discarded_cards == ["D"]


def test_hand_keeps_same_card_list_when_discarding_excess():
    hand = Hand(["A", "B"], max_size=3)
    displayed_cards = hand.cards

    discarded_cards = hand.add_cards(["C", "D"])

    assert displayed_cards is hand.cards
    assert displayed_cards == ["A", "B", "C"]
    assert discarded_cards == ["D"]


def test_battle_state_draws_starting_hand_after_hero_selection():
    commander = Card("Commander", "Dark", 30)
    deck_cards = [
        Card("Card 1", "Nature", 10),
        Card("Card 2", "Tech", 10),
        Card("Card 3", "Neutral", 10),
    ]

    battle_state = BattleState(commander, deck_cards, starting_hand_size=2)

    assert battle_state.player.hero == commander
    assert len(battle_state.player_hand) == 2
    assert len(battle_state.player_deck) == 1


def test_battle_state_starting_hand_includes_hero_when_deck_has_one():
    commander = Card("Commander", "Dark", 30)
    mana_card = Card("Mana", "Neutral", 0, card_type="Mana")
    skill_card = Card("Skill", "Neutral", 0, card_type="Skill")
    hero_card = Card("Hero", "Nature", 10)

    battle_state = BattleState(
        commander,
        [mana_card, skill_card, hero_card],
        starting_hand_size=2,
        shuffle_deck=False,
    )

    assert hero_card in battle_state.player_hand.cards
    assert len(battle_state.player_hand) == 2


def test_mulligan_redraws_starting_hand_once_at_game_start():
    commander = Card("Commander", "Dark", 30)
    first_card = Card("First", "Nature", 10)
    second_card = Card("Second", "Tech", 10)
    third_card = Card("Third", "Dark", 10)
    fourth_card = Card("Fourth", "Neutral", 10)
    battle_state = BattleState(
        commander,
        [first_card, second_card, third_card, fourth_card],
        starting_hand_size=2,
        shuffle_deck=False,
    )

    result = battle_state.mulligan()

    assert result.success
    assert battle_state.has_used_mulligan
    assert len(battle_state.player_hand) == 2
    assert battle_state.player_hand.cards != [first_card, second_card]


def test_mulligan_can_only_be_used_once():
    commander = Card("Commander", "Dark", 30)
    deck_cards = [
        Card("First", "Nature", 10),
        Card("Second", "Tech", 10),
        Card("Third", "Dark", 10),
        Card("Fourth", "Neutral", 10),
    ]
    battle_state = BattleState(
        commander,
        deck_cards,
        starting_hand_size=2,
        shuffle_deck=False,
    )

    first_result = battle_state.mulligan()
    second_result = battle_state.mulligan()

    assert first_result.success
    assert not second_result.success
    assert second_result.message == "Mulligan already used"


def test_mulligan_only_allowed_before_first_phase_advance():
    commander = Card("Commander", "Dark", 30)
    deck_cards = [
        Card("First", "Nature", 10),
        Card("Second", "Tech", 10),
        Card("Third", "Dark", 10),
    ]
    battle_state = BattleState(
        commander,
        deck_cards,
        starting_hand_size=2,
        shuffle_deck=False,
    )

    battle_state.advance_phase()
    result = battle_state.mulligan()

    assert not result.success
    assert result.message == "Mulligan only available at game start"


def test_mulligan_keeps_a_hero_in_starting_hand_when_possible():
    commander = Card("Commander", "Dark", 30)
    mana_card = Card("Mana", "Neutral", 0, card_type="Mana")
    skill_card = Card("Skill", "Neutral", 0, card_type="Skill")
    hero_card = Card("Hero", "Nature", 10)
    battle_state = BattleState(
        commander,
        [mana_card, skill_card, hero_card],
        starting_hand_size=2,
        shuffle_deck=False,
    )

    battle_state.mulligan()

    assert any(card.card_type == "Hero" for card in battle_state.player_hand.cards)


def test_battle_state_discards_drawn_cards_when_hand_is_full():
    commander = Card("Commander", "Dark", 30)
    deck_cards = [
        Card("Card 1", "Nature", 10),
        Card("Card 2", "Tech", 10),
        Card("Card 3", "Neutral", 10),
    ]
    battle_state = BattleState(
        commander,
        deck_cards,
        starting_hand_size=2,
        max_hand_size=2,
    )

    result = battle_state.draw_cards(1)

    assert result.success
    assert len(battle_state.player_hand) == 2
    assert len(result.discarded_cards) == 1
    assert battle_state.player_discard_pile == result.discarded_cards


def test_demo_deck_uses_target_size_and_excludes_commander():
    commander = Card("Ishani", "Nature", 80)

    deck = create_demo_deck(commander, target_size=30)

    assert len(deck) == 30
    assert commander.name not in [card.name for card in deck]


def test_cards_can_store_card_type():
    hero = Card("Hero", "Dark", 30, card_type="Hero")
    mana = Card("Mana", "Neutral", 0, card_type="Mana")
    skill = Card("Skill", "Neutral", 0, card_type="Skill")

    assert hero.card_type == "Hero"
    assert mana.card_type == "Mana"
    assert skill.card_type == "Skill"


def test_cards_default_to_hero_type_for_existing_card_data():
    card = Card("Hero", "Dark", 30)

    assert card.card_type == "Hero"


def test_only_hero_cards_can_be_played_to_battlefield():
    commander = Card("Commander", "Dark", 30)
    mana_card = Card("Mana", "Neutral", 0, card_type="Mana")
    battle_state = BattleState(
        commander,
        [mana_card],
        starting_hand_size=1,
    )

    result = battle_state.play_card_to_player_battlefield(mana_card)

    assert not result.success
    assert result.message == "Only hero cards can be played to the battlefield"
    assert mana_card in battle_state.player_hand.cards
    assert mana_card not in battle_state.player_board.active_heroes
