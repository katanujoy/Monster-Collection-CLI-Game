import random
from sqlalchemy.orm import joinedload
from db.models import MonsterSpecies, Monster

# Type effectiveness (future use)
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

# Catch chances by rarity
RARITY_CATCH_CHANCE = {
    "Common": 0.8,
    "Rare": 0.5,
    "Epic": 0.3,
    "Legendary": 0.1
}

def calculate_catch_rate(species_rarity, player_level):
    try:
        base_chance = RARITY_CATCH_CHANCE.get(species_rarity, 0.1)
        bonus = min(0.05 * (player_level - 1), 0.15)  # max +15%
        return min(base_chance + bonus, 0.95)
    except Exception as e:
        print(f"[Error] Failed to calculate catch rate: {e}")
        return 0.0

def catch_monster(session, player_id, species_id, player_level):
    try:
        species = session.query(MonsterSpecies).filter_by(id=species_id).first()
        if not species:
            return {"success": False, "message": "❌ Monster species not found."}

        chance = calculate_catch_rate(species.rarity, player_level)
        if random.random() < chance:
            new_monster = Monster(
                player_id=player_id,
                species_id=species.id,
                level=1,
                nickname=species.name  # Default nickname
            )
            session.add(new_monster)
            session.commit()
            return {
                "success": True,
                "message": f"✅ Successfully caught {species.name}!",
                "monster": new_monster
            }
        else:
            return {"success": False, "message": "❌ The monster escaped!"}
    except Exception as e:
        session.rollback()
        print(f"[Error] Failed to catch monster: {e}")
        return {"success": False, "message": "❌ An error occurred while catching the monster."}

def get_player_collection(session, player_id):
    try:
        collection = session.query(Monster).options(joinedload(Monster.species)).filter_by(player_id=player_id).all()
        return collection  # Now returns list directly
    except Exception as e:
        print(f"[Error] Failed to retrieve player collection: {e}")
        return []  # Return empty list on failure

def level_up_monster(session, monster_id):
    try:
        monster = session.query(Monster).options(joinedload(Monster.species)).filter_by(id=monster_id).first()
        if not monster:
            return {"success": False, "message": "❌ Monster not found."}

        monster.level += 1
        session.commit()
        return {
            "success": True,
            "message": f"🎉 {monster.nickname} leveled up to {monster.level}!",
            "monster": {
                "name": monster.species.name,
                "level": monster.level,
                "nickname": monster.nickname
            }
        }
    except Exception as e:
        session.rollback()
        print(f"[Error] Failed to level up monster: {e}")
        return {"success": False, "message": "❌ An error occurred while leveling up the monster."}
