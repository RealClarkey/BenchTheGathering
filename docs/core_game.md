# Core Game Design Document

## Game Rules

---

## Deck
- 20-30 cards per deck
- No duplicate limit (for now)
- Deck contains cards used during the match, excluding the chosen player hero
- Current 30-card prototype deck uses 12 Hero cards, 10 Mana cards, and 8 Skill cards

---

## Starting The Game
- Choose Player Hero before the match starts
- Player Hero is selected from available hero cards, not drawn randomly
- Player Hero starts on battlefield
- Shuffle Deck
- Draw 7 cards
- Player may take 1 Mulligan before advancing to the first Draw Phase
- Mulligan shuffles the opening hand back into the deck and draws a new 7-card hand

---

## Player Health
- Player HP is equal to the selected Player Hero's HP
- If the Player Hero reaches 0 HP, that player loses

---

## Turn Structure
- Current prototype advances phases with the Next Phase button

### Start of Turn
- Refresh mana
- Resolve ongoing effects

### Draw Phase
- Draw 1 card

### Main Phase
- Play 1 Mana card (optional)
- Play 1 Hero card OR Skill card

### Action Phase
- Attack with Heroes
- Use abilities

### End Turn
- End effects expire

---

## Battlefield
- Max 3 Heroes active per player

---

## Hand Size
- Players start with 7 cards
- Players draw 1 card per turn
- Maximum hand size is 7
- If a player draws above 7 cards, excess cards are discarded

---

## Mana System
- Players start at 1/1 mana after choosing their Player Hero
- Mana cards increase max mana
- Mana refills each turn
- Current mana cannot exceed max mana
- Playing mana cards is required to increase max mana
- Players can play 1 Mana card per turn
- Current prototype Skill cards cost 1 mana

---

## Combat
- Heroes attack:
    - Enemy Heroes
    - Enemy Player Hero
- Damage is simultaneous
- Current prototype uses a default enemy commander and battlefield before AI exists
- Attacks are only allowed during the Action Phase
- Each hero can attack once per turn
- Defeated enemy battlefield heroes are removed from battle

---

## Type System
- Dark > Nature
- Nature > Tech
- Tech > Dark
- Neutral = no advantage

---

## Buff & Debuff System
- Effects can target:
  - Self
  - Ally
  - Enemy
- Buffs and debuffs shown as icons

---

## Evolution
- Heroes evolve after trigger condition
- Gain stat boosts and/or new abilities

--- 

## Win Condition
- Reduce opponent Hero HP to 0
