# Core Game Design Document

## Game Rules

---

## Deck
- 20-30 cards per deck
- No duplicate limit (for now)
- Deck contains cards used during the match, excluding the chosen player hero

---

## Starting The Game
- Choose Player Hero before the match starts
- Player Hero is selected from available hero cards, not drawn randomly
- Player Hero starts on battlefield
- Shuffle Deck
- Draw starting hand

---

## Player Health
- Player HP is equal to the selected Player Hero's HP
- If the Player Hero reaches 0 HP, that player loses

---

## Turn Structure

### Start of Turn
- Refresh mana
- Resolve ongoing effects

### Draw Phase
- Draw 1 card

### Main Phase
- Play 1 Mana card (optional)
- Play 1 Hero card OR skill card

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
- Starting hand size is still undecided
- Starting hand can be higher than 7 if testing shows the game needs it
- Players draw 1 card per turn
- Maximum hand size is 7
- If a player draws above 7 cards, excess cards are discarded

---

## Mana System
- Mana cards increase max mana
- Mana refills each turn
- Current mana cannot exceed max mana
- Playing mana cards is required to increase max mana

---

## Combat
- Heroes attack:
    - Enemy Heroes
    - Enemy Player Hero
- Damage is simultaneous

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
