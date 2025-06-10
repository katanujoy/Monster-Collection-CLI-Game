import random
from db.models import MonsterSpecies, Monster

# Type effectiveness (for later battle logic)
TYPE_EFFECTIVENESS = {
    "Fire": ["Grass", "Ice"],
    "Water": ["Fire", "Rock"],
    "Grass": ["Water", "Rock"],
    "Electric": ["Water"],
    "Rock": ["Fire", "Electric"],
    "Ice": ["Grass"],
    "Dark": ["Mystic"],
    "Mystic": ["Electric"]
}

# Catch chance by rarity
RARITY_CATCH_CHANCE = {
    "Common": 0.8,
    "Rare": 0.5,
    "Epic": 0.3,
    "Legendary": 0.1
}

# Adjust catch rate based on player level
def calculate_catch_rate(species_rarity, player_level):
    base_chance = RARITY_CATCH_CHANCE.get(species_rarity, 0.1)
    bonus = min(0.05 * (player_level - 1), 0.15)  # Max bonus is 15%
    return min(base_chance + bonus, 0.95)  # Cap at 95%

# Catching logic
def catch_monster(session, player_id, species_id, player_level):
    species = session.query(MonsterSpecies).filter_by(id=species_id).first()
    if not species:
        return False

    chance = calculate_catch_rate(species.rarity, player_level)
    if random.random() < chance:
        new_monster = Monster(player_id=player_id, species_id=species.id, level=1)
        session.add(new_monster)
        session.commit()
        return True
    return False

# Get all monsters owned by a player
def get_player_collection(session, player_id):
    return session.query(Monster).filter_by(player_id=player_id).all()

# Level-up a specific monster
def level_up_monster(session, monster_id):
    monster = session.query(Monster).filter_by(id=monster_id).first()
    if not monster:
        return None
    monster.level += 1
    session.commit()
    return {
        "name": monster.species.name,
        "level": monster.level
    }
