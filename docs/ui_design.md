# UI Design Document

## Main Battle Screen

The main screen is divided into the following sections:

---

## 1. Opponent Area

Displays:
- Opponent Hero
- Opponent HP
- Number of cards in opponent hand

Notes:
- Opponent hand is not visible
- Keep this area simple

---

## 2. Enemy Battlefield

Displays:
- Up to 3 enemy hero cards

Each card shows:
- Attack
- Health
- Type
- Active effects (later)

Notes:
- Cards are placed in fixed slots

---

## 3. Player Battlefield

Displays:
- Up to 3 player hero cards

Each card shows:
- Attack
- Health
- Type
- Active effects (later)

Notes:
- Same structure as enemy battlefield

---

## 4. Player Area

Displays:
- Player Hero
- Player HP
- Mana (current / max)

Notes:
- Always visible

---

## 5. Player Hand

Displays:
- Cards currently in hand (max 7)

Behaviour:
- Cards are arranged in a fan
- Cards can be clicked and dragged
- Selected/dragged card is highlighted (https://johnscolaro.xyz/blog/pygame-cards) 

---

## 6. Controls

Displays:
- End Turn button

Notes:
- Used to finish the player’s turn

---

## Interaction Summary

- Click and drag a card from the hand
- Drag the card over a battlefield slot
- Release to place the card
- If released outside a valid slot, the card returns to the hand

---

## Future Features (Not required yet)

- Attack interactions
- Skill targeting
- Buff/debuff icons
- Animations