from src.cards.card import Card
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
