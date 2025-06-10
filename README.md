# Monster-Collection-CLI-Game

A command-line monster catching game with species data, rarity mechanics, and leveling!

## How to Run
1. Install dependencies: `pip install sqlalchemy`
2. Run the game: `python main.py`or `python3 main.py`
3. Optional: seed monster species: `python -c \"from seed import seed_monsters; from db.database import Session; seed_monsters(Session())\"`

## File Structure
```
📁 game/
  ├── player_logic.py       # Player creation, level-up
  ├── monster_logic.py      # Monster management (catching, leveling)
  ├── battle_logic.py       # (Later) Damage calc, effectiveness
  └── trading_logic.py      # (Later) Trade monsters

📁 db/
  ├── models.py             # SQLAlchemy models ✅
  ├── database.py           # DB engine/session setup

📁 tests/
  ├── test_player.py        # Test player logic
  ├── test_monster.py       # Test monster logic
  ├── test_battle.py        # Test type effectiveness, etc.

📄 cli.py                    # Entry CLI commands (future)
📄 seed.py                   # Monster species data ✅
📄 mechanics.py              # Game logic (catching, leveling) ✅
📄 main.py                   # Game runner script ✅
📄 README.md                 # Setup instructions and game summary
```

## Features
- Monster rarity affects catch rate
- Player leveling influences catch success
- View and level up your monsters
