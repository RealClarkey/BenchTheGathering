# A file structure to help me visualise the app

BenchTheGathering/
├─ main.py                  ← Entry point (runs the game)
├─ requirements.txt
├─ README.md
├─ .gitignore
│
├─ src/
│  ├─ __init__.py
│  │
│  ├─ game.py              ← Game loop, screen switching
│  │
│  ├─ screens/
│  │  ├─ __init__.py
│  │  ├─ menu.py           ← Menu screen
│  │  └─ battle.py         ← Main gameplay screen (uses everything below)
│  │
│  ├─ cards/
│  │  ├─ __init__.py
│  │  ├─ card.py           ← Card DATA only (name, cost, etc.)
│  │  ├─ deck.py           ← (later)
│  │  └─ hand.py           ← (later - logical hand, not visual)
│  │
│  ├─ gameplay/
│  │  ├─ __init__.py
│  │  ├─ player.py         ← Player data (hp, mana, etc.)
│  │  ├─ board.py          ← Board state
│  │  └─ turn_manager.py   ← Turns, phases
│  │
│  ├─ ui/
│  │  ├─ __init__.py
│  │  ├─ hand_view.py      ← Card fan effect (hover, drag, layout)
│  │  ├─ card_view.py      ← (optional later: drawing single cards)
│  │  └─ button.py         ← UI buttons (next turn etc.)
│
├─ assets/
│  ├─ images/
│  ├─ sounds/
│  └─ fonts/
│
├─ tests/
│
└─ prototypes/
   └─ hand_fan_test/
      └─ main.py           ← Original card fan prototype (now deprecated)