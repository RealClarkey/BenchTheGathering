from src.cards.card import Card
from src.gameplay.battle_state import BattleState


def advance_to_action_phase(battle_state):
    battle_state.advance_phase()
    battle_state.advance_phase()
    battle_state.advance_phase()


def test_type_advantage_damage_modifiers():
    battle_state = BattleState(Card("Player Hero", "Dark", 30), [], starting_hand_size=0)

    assert battle_state.calculate_damage(Card("Dark", "Dark", 10, attack=4), Card("Nature", "Nature", 10)) == 5
    assert battle_state.calculate_damage(Card("Nature", "Nature", 10, attack=4), Card("Dark", "Dark", 10)) == 3
    assert battle_state.calculate_damage(Card("Neutral", "Neutral", 10, attack=4), Card("Dark", "Dark", 10)) == 4


def test_attack_damages_enemy_battlefield_hero():
    attacker = Card("Attacker", "Dark", 10, attack=4)
    target = Card("Target", "Nature", 10)
    battle_state = BattleState(Card("Player Hero", "Dark", 30), [], starting_hand_size=0)
    battle_state.player_board.add_hero(attacker)
    battle_state.enemy_board.add_hero(target)
    advance_to_action_phase(battle_state)

    result = battle_state.attack(attacker, target)

    assert result.success
    assert result.damage == 5
    assert target.current_hit_points == 5
    assert battle_state.player.current_mana == 0


def test_attack_requires_one_mana():
    attacker = Card("Attacker", "Dark", 10, attack=4)
    target = Card("Target", "Nature", 10)
    battle_state = BattleState(Card("Player Hero", "Dark", 30), [], starting_hand_size=0)
    battle_state.player.current_mana = 0
    battle_state.player_board.add_hero(attacker)
    battle_state.enemy_board.add_hero(target)
    advance_to_action_phase(battle_state)

    result = battle_state.attack(attacker, target)

    assert not result.success
    assert result.message == "Not enough mana to attack"
    assert target.current_hit_points == 10


def test_attack_does_not_spend_mana_when_not_action_phase():
    attacker = Card("Attacker", "Dark", 10, attack=4)
    target = Card("Target", "Nature", 10)
    battle_state = BattleState(Card("Player Hero", "Dark", 30), [], starting_hand_size=0)
    battle_state.player.current_mana = 1
    battle_state.player_board.add_hero(attacker)
    battle_state.enemy_board.add_hero(target)

    result = battle_state.attack(attacker, target)

    assert not result.success
    assert battle_state.player.current_mana == 1


def test_attack_removes_defeated_enemy_battlefield_hero():
    attacker = Card("Attacker", "Dark", 10, attack=4)
    target = Card("Target", "Nature", 5)
    battle_state = BattleState(Card("Player Hero", "Dark", 30), [], starting_hand_size=0)
    battle_state.player_board.add_hero(attacker)
    battle_state.enemy_board.add_hero(target)
    advance_to_action_phase(battle_state)

    result = battle_state.attack(attacker, target)

    assert result.success
    assert target not in battle_state.enemy_board.active_heroes


def test_attack_can_target_enemy_player_hero():
    attacker = Card("Attacker", "Tech", 10, attack=4)
    enemy_player_hero = Card("Enemy Player Hero", "Dark", 20)
    battle_state = BattleState(
        Card("Player Hero", "Dark", 30),
        [],
        starting_hand_size=0,
        enemy_hero=enemy_player_hero,
    )
    battle_state.player_board.add_hero(attacker)
    advance_to_action_phase(battle_state)

    result = battle_state.attack(attacker, enemy_player_hero)

    assert result.success
    assert enemy_player_hero.current_hit_points == 15


def test_enemy_player_hero_cannot_be_attacked_while_enemy_heroes_are_active():
    attacker = Card("Attacker", "Tech", 10, attack=4)
    enemy_player_hero = Card("Enemy Player Hero", "Dark", 20)
    enemy_guard = Card("Enemy Guard", "Nature", 10)
    battle_state = BattleState(
        Card("Player Hero", "Dark", 30),
        [],
        starting_hand_size=0,
        enemy_hero=enemy_player_hero,
        enemy_board_cards=[enemy_guard],
    )
    battle_state.player_board.add_hero(attacker)
    advance_to_action_phase(battle_state)

    result = battle_state.attack(attacker, enemy_player_hero)

    assert not result.success
    assert result.message == "Enemy battlefield heroes must be defeated first"
    assert enemy_player_hero.current_hit_points == 20
    assert battle_state.player.current_mana == 1


def test_reducing_enemy_player_hero_to_zero_ends_game():
    attacker = Card("Attacker", "Tech", 10, attack=4)
    enemy_player_hero = Card("Enemy Player Hero", "Dark", 5)
    battle_state = BattleState(
        Card("Player Hero", "Dark", 30),
        [],
        starting_hand_size=0,
        enemy_hero=enemy_player_hero,
    )
    battle_state.player_board.add_hero(attacker)
    advance_to_action_phase(battle_state)

    result = battle_state.attack(attacker, enemy_player_hero)

    assert result.success
    assert result.game_over
    assert battle_state.game_over
    assert battle_state.winner == "player"


def test_game_over_blocks_further_attacks():
    attacker = Card("Attacker", "Tech", 10, attack=4)
    enemy_player_hero = Card("Enemy Player Hero", "Dark", 5)
    battle_state = BattleState(
        Card("Player Hero", "Dark", 30),
        [],
        starting_hand_size=0,
        enemy_hero=enemy_player_hero,
    )
    battle_state.player.max_mana = 2
    battle_state.player.current_mana = 2
    battle_state.player_board.add_hero(attacker)
    advance_to_action_phase(battle_state)
    battle_state.attack(attacker, enemy_player_hero)

    result = battle_state.attack(attacker, enemy_player_hero)

    assert not result.success
    assert result.message == "Game is already over"


def test_attack_only_allowed_in_action_phase():
    attacker = Card("Attacker", "Dark", 10, attack=4)
    target = Card("Target", "Nature", 10)
    battle_state = BattleState(Card("Player Hero", "Dark", 30), [], starting_hand_size=0)
    battle_state.player_board.add_hero(attacker)
    battle_state.enemy_board.add_hero(target)

    result = battle_state.attack(attacker, target)

    assert not result.success
    assert result.message == "You can only attack during the action phase"
    assert target.current_hit_points == 10


def test_attacker_can_only_attack_once_per_turn():
    attacker = Card("Attacker", "Dark", 10, attack=4)
    first_target = Card("First Target", "Nature", 10)
    second_target = Card("Second Target", "Nature", 10)
    battle_state = BattleState(Card("Player Hero", "Dark", 30), [], starting_hand_size=0)
    battle_state.player_board.add_hero(attacker)
    battle_state.enemy_board.add_hero(first_target)
    battle_state.enemy_board.add_hero(second_target)
    advance_to_action_phase(battle_state)

    first_result = battle_state.attack(attacker, first_target)
    second_result = battle_state.attack(attacker, second_target)

    assert first_result.success
    assert not second_result.success
    assert second_result.message == "This hero has already attacked this turn"
    assert second_target.current_hit_points == 10


def test_same_named_attacker_cards_act_independently():
    first_attacker = Card("Moldrax", "Dark", 10, attack=4)
    second_attacker = Card("Moldrax", "Dark", 10, attack=4)
    first_target = Card("First Target", "Nature", 10)
    second_target = Card("Second Target", "Nature", 10)
    battle_state = BattleState(Card("Player Hero", "Dark", 30), [], starting_hand_size=0)
    battle_state.player.max_mana = 2
    battle_state.player.current_mana = 2
    battle_state.player_board.add_hero(first_attacker)
    battle_state.player_board.add_hero(second_attacker)
    battle_state.enemy_board.add_hero(first_target)
    battle_state.enemy_board.add_hero(second_target)
    advance_to_action_phase(battle_state)
    battle_state.player.current_mana = 2

    first_result = battle_state.attack(first_attacker, first_target)
    second_result = battle_state.attack(second_attacker, second_target)

    assert first_attacker is not second_attacker
    assert first_result.success
    assert second_result.success
    assert first_target.current_hit_points == 5
    assert second_target.current_hit_points == 5
