from db.database import engine
from db.models import Base
from db.session import session  # Use the shared session
from game.player_logic import get_or_create_player
from game.monster_logic import catch_monster, get_player_collection, level_up_monster

# Create all tables
Base.metadata.create_all(engine)

# Seed monsters (run once, then comment again)
# from seed import seed_monsters
# seed_monsters(session)

# Create or get existing player
player = get_or_create_player("Ash")

# Try to catch a monster (species_id=1, player's level)
success = catch_monster(session, player.id, species_id=1, player_level=player.level)
print("Caught!" if success else "Failed to catch")

# Show player's monster collection
collection = get_player_collection(session, player.id)
print("\nYour monsters:")
for m in collection:
    print(f"{m.species.name} - Level {m.level} (Nickname: {m.nickname})")

# Level up the first monster in the collection
if collection:
    updated = level_up_monster(session, collection[0].id)
    print("\nLeveled up:", updated)
