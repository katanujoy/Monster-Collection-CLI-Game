from db.models import MonsterSpecies  # Use correct import path
from db.database import Session       # Get the DB session from your config

def seed_monsters(session):
    monster_data = [
        {"name": "Flametail", "type": "Fire", "base_stats": 50, "rarity": "Common", "abilities": "Blaze, Ember"},
        {"name": "Aqualisk", "type": "Water", "base_stats": 52, "rarity": "Common", "abilities": "Splash, Soak"},
        {"name": "Leafurr", "type": "Grass", "base_stats": 48, "rarity": "Common", "abilities": "Vine Whip, Grow"},
        {"name": "Voltkit", "type": "Electric", "base_stats": 51, "rarity": "Common", "abilities": "Zap, Charge"},
        {"name": "Rockhorn", "type": "Rock", "base_stats": 55, "rarity": "Rare", "abilities": "Bash, Stomp"},
        {"name": "Whispy", "type": "Wind", "base_stats": 49, "rarity": "Rare", "abilities": "Gust, Whisper"},
        {"name": "Nightclaw", "type": "Dark", "base_stats": 60, "rarity": "Rare", "abilities": "Shadow, Sneak"},
        {"name": "Frostbite", "type": "Ice", "base_stats": 62, "rarity": "Epic", "abilities": "Freeze, Chill"},
        {"name": "Pyrosaur", "type": "Fire", "base_stats": 65, "rarity": "Epic", "abilities": "Inferno, Tailwhip"},
        {"name": "Hydrake", "type": "Water", "base_stats": 68, "rarity": "Epic", "abilities": "Wave, Torrent"},
        {"name": "Thundragon", "type": "Electric", "base_stats": 70, "rarity": "Legendary", "abilities": "Storm, Thunderclap"},
        {"name": "Terraptor", "type": "Rock", "base_stats": 72, "rarity": "Legendary", "abilities": "Quake, Smash"},
        {"name": "Mystora", "type": "Mystic", "base_stats": 75, "rarity": "Legendary", "abilities": "Illusion, Blink"},
        {"name": "Solarion", "type": "Fire", "base_stats": 80, "rarity": "Legendary", "abilities": "Solar Beam, Burn"},
        {"name": "Glacifin", "type": "Ice", "base_stats": 77, "rarity": "Epic", "abilities": "Ice Beam, Shiver"}
    ]

    for data in monster_data:
        existing = session.query(MonsterSpecies).filter_by(name=data["name"]).first()
        if not existing:
            monster = MonsterSpecies(**data)
            session.add(monster)

    session.commit()

# Run this file directly to seed (optional)
if __name__ == "__main__":
    session = Session()
    seed_monsters(session)
    print("Monsters seeded.")
