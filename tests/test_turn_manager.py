from src.cards.card import Card
from src.gameplay.battle_state import BattleState
from src.gameplay.turn_manager import TurnManager


def test_turn_manager_starts_at_start_phase():
    turn_manager = TurnManager()

    assert turn_manager.current_phase == "start"
    assert turn_manager.turn_number == 1


def test_turn_manager_advances_through_phase_order():
    turn_manager = TurnManager()

    assert turn_manager.advance_phase() == "draw"
    assert turn_manager.advance_phase() == "main"
    assert turn_manager.advance_phase() == "action"
    assert turn_manager.advance_phase() == "end"
    assert turn_manager.advance_phase() == "start"
    assert turn_manager.turn_number == 2


def test_start_phase_refills_player_mana():
    commander = Card("Commander", "Dark", 30)
    battle_state = BattleState(commander, [], starting_hand_size=0)
    battle_state.player.max_mana = 3
    battle_state.player.current_mana = 0

    battle_state.resolve_current_phase()

    assert battle_state.player.current_mana == 3


def test_draw_phase_draws_one_card_once():
    commander = Card("Commander", "Dark", 30)
    deck_card = Card("Deck Card", "Nature", 10)
    battle_state = BattleState(commander, [deck_card], starting_hand_size=0)

    battle_state.advance_phase()

    assert battle_state.turn_manager.current_phase == "draw"
    assert deck_card in battle_state.player_hand.cards
    assert len(battle_state.player_deck) == 0

    battle_state.resolve_current_phase()

    assert battle_state.player_hand.cards.count(deck_card) == 1


def test_advancing_from_end_starts_next_turn_and_refills_mana():
    commander = Card("Commander", "Dark", 30)
    battle_state = BattleState(commander, [], starting_hand_size=0)
    battle_state.player.max_mana = 2
    battle_state.player.current_mana = 0

    battle_state.advance_phase()
    battle_state.advance_phase()
    battle_state.advance_phase()
    battle_state.advance_phase()
    battle_state.advance_phase()

    assert battle_state.turn_manager.current_phase == "start"
    assert battle_state.turn_manager.turn_number == 2
    assert battle_state.player.current_mana == 2
