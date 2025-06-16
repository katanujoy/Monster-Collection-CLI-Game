# game/player_logic.py
from db.session import session
from db.models import Player
from sqlalchemy.orm import Session

def get_or_create_player(username: str):
    try:
        player = session.query(Player).filter_by(username=username).first()
        if player:
            print(f"Welcome back, {username}!")
        else:
            player = Player(username=username)
            session.add(player)
            session.commit()
            print(f"New player created: {username}")
        return player
    except Exception as e:
        session.rollback()
        print(f"[Error] Failed to get or create player: {e}")
        return None

def gain_xp(session: Session, player: Player, xp_amount: int):
    if not player:
        print("[Error] No valid player provided.")
        return

    if xp_amount <= 0:
        print("Can't add zero or negative XP!")
        return

    try:
        player.experience += xp_amount
        print(f"{player.username} got {xp_amount} XP points!")
        
        # XP required to level up
        xp_needed = player.level * 100
        while player.experience >= xp_needed:
            player.experience -= xp_needed
            player.level += 1
            player.money += 50
            print(f"Awesome! {player.username} reached level {player.level}!")
            xp_needed = player.level * 100

        session.commit()
    except Exception as e:
        session.rollback()
        print(f"[Error] Couldn't save XP changes: {e}")

def show_player_stats(player: Player):
    if not player:
        print("[Error] No valid player provided.")
        return

    print("\n=== PLAYER STATS ===")
    print(f"Name: {player.username}")
    print(f"Level: {player.level}")
    print(f"XP: {player.experience} (needs {player.level * 100} for next level)")
    print(f"Coins: {player.money}")
    print(f"Badges: {player.achievements if player.achievements else 'No badges yet'}")
    print("====================")

def view_profile(session: Session, player_id: int):
    try:
        player = session.query(Player).filter_by(id=player_id).first()
        if not player:
            raise ValueError("Player not found.")

        collection_size = len(player.monsters) if hasattr(player, 'monsters') else 0

        return {
            "username": player.username,
            "level": player.level,
            "experience": player.experience,
            "money": player.money,
            "achievements": player.achievements or "No badges yet",
            "collection_size": collection_size
        }
    except Exception as e:
        print(f"[Error] Couldn't load profile: {e}")
        raise
