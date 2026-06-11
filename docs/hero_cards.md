# Hero Cards

Basic outline of the initial hero cards to get development moving.

## Type Effectiveness

Nature > Tech > Dark > Nature

Neutral has no strengths or weaknesses.

### Damage Modifiers

- Strong Against: +25% damage
- Weak Against: -25% damage
- Neutral Interactions: No modifier

### Examples

- Nature attacking Tech: +25% damage
- Tech attacking Dark: +25% damage
- Dark attacking Nature: +25% damage

- Tech attacking Nature: -25% damage
- Dark attacking Tech: -25% damage
- Nature attacking Dark: -25% damage

- Any type attacking Neutral: No modifier
- Neutral attacking any type: No modifier

---

## Dark Type

### Dreadbone, Undead King
- **HP:** 90
- **Bone Cleaver** *(Basic Attack)* - 2 Mana
- **Raise the Fallen** *(Ability)* - 5 Mana
  - Summons a Skeleton Minion that attacks for 10 damage each turn.
- **Evolution:** Maximum HP increased by 50%. All abilities increase by 50%.

### Morvane, Shadow Warlock
- **HP:** 75
- **Shadow Bolt** *(Basic Attack)* - 2 Mana
- **Soul Drain** *(Ability)* - 4 Mana
  - Deal 20 damage to an enemy and heal for the damage dealt.
- **Evolution:** Maximum HP increased by 50%. All abilities increase by 50%.

### Vexis, Broodmother
- **HP:** 85
- **Venom Bite** *(Basic Attack)* - 2 Mana
- **Paralysing Venom** *(Ability)* - 4 Mana
  - Target enemy cannot use abilities during their next turn.
- **Evolution:** Maximum HP increased by 50%. All abilities increase by 50%.

---

## Nature Type

### Ishani
- **HP:** 80
- **Blossom Attack** *(Basic Attack)* - 2 Mana
- **Verdant Bloom** *(Ability)* - 4 Mana
  - Heal all active heroes for 10% of their maximum HP.
- **Evolution:** Maximum HP increased by 50%. All abilities increase by 50%.

### Thornroot, Ancient Guardian
- **HP:** 100
- **Root Slam** *(Basic Attack)* - 2 Mana
- **Living Bark** *(Ability)* - 4 Mana
  - Reduce all damage taken by 50% for the next 2 turns.
- **Evolution:** Maximum HP increased by 50%. All abilities increase by 50%.

### Sylva, Forest Huntress
- **HP:** 75
- **Vine Whip** *(Basic Attack)* - 2 Mana
- **Nature's Fury** *(Ability)* - 4 Mana
  - Deal 25 damage to a target enemy.
- **Evolution:** Maximum HP increased by 50%. All abilities increase by 50%.

---

## Tech Type

### Sparky-5, Experimental Prototype
- **HP:** 85
- **Misfire Cannon** *(Basic Attack)* - 2 Mana
  - Deals 15 damage to an enemy.
  - Has a 10% chance to hit a random target instead.
- **Random Upgrade** *(Ability)* - 4 Mana
  - Randomly affects an active hero:
    - +25% Damage for 2 turns
    - +25% Maximum HP
    - Heal 20 HP
    - -25% Damage for 2 turns *(Oops!)*
- **Evolution:** Maximum HP increased by 50%. All abilities increase by 50%.

### Voltis, Arc Technician
- **HP:** 80
- **Shock Blast** *(Basic Attack)* - 2 Mana
- **Overload** *(Ability)* - 4 Mana
  - Deal 20 damage and prevent the target from using abilities next turn.
- **Evolution:** Maximum HP increased by 50%. All abilities increase by 50%.

### Ironclad, Siege Automaton
- **HP:** 105
- **Hydraulic Smash** *(Basic Attack)* - 2 Mana
- **Adaptive Shield** *(Ability)* - 5 Mana
  - Reduce all damage taken by 50% for the next 2 turns.
- **Evolution:** Maximum HP increased by 50%. All abilities increase by 50%.

---

## Neutral Type

### Aurelia, Scales of Judgement
- **HP:** 80
- **Balanced Verdict** *(Basic Attack)* - 2 Mana
  - Deals damage equal to 10% of the target's maximum HP.
- **Lady's Decree** *(Ability)* - 4 Mana
  - Removes all attack buffs and debuffs currently active on the battlefield.
- **Evolution:** Maximum HP increased by 50%. All abilities increase by 50%.

### Kael, Wandering Mercenary
- **HP:** 85
- **Sword Slash** *(Basic Attack)* - 2 Mana
- **Execution Strike** *(Ability)* - 4 Mana
  - Deal 30 damage to an enemy below 50% HP.
- **Evolution:** Maximum HP increased by 50%. All abilities increase by 50%.

### Sentinel, Guardian of Order
- **HP:** 100
- **Shield Bash** *(Basic Attack)* - 2 Mana
- **Protective Stance** *(Ability)* - 4 Mana
  - Reduce incoming damage by 25% for all allied heroes for the next 2 turns.
- **Evolution:** Maximum HP increased by 50%. All abilities increase by 50%.

---

# Hero Card Structure

Each hero card contains:

- Name
- Hero Type (Dark, Nature, Tech, Neutral)
- Hit Points (HP)
- Character Image
- Active Buffs/Debuffs (Icons)
- Abilities
  - Name
  - Description
  - Damage/Effect Value
  - Mana Cost
- Evolution Effects

---

# Balance Guidelines

## Hero Archetypes

| Role | HP Range |
|------|----------|
| Damage Dealer | 70-85 |
| Balanced | 80-90 |
| Tank | 95-110 |

## Ability Guidelines

| Ability Type | Typical Value |
|--------------|--------------|
| Basic Attack | 10-15 Damage |
| Single Target Ability | 20-30 Damage |
| AoE Ability | 10-15 Damage |
| Healing Ability | 10-20 HP |
| Buff/Debuff | 2 Turns |