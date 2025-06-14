# game/player_logic.py
from db.session import session
from db.models import Player
from sqlalchemy.orm import Session

def get_or_create_player(username):
    player = session.query(Player).filter_by(username=username).first()
    if player:
        print(f"Welcome back, {username}!")
    else:
        player = Player(username=username)
        session.add(player)
        session.commit()
        print(f"New player created: {username}")
    return player

def gain_xp(session: Session, player: Player, xp_amount: int):
    if xp_amount <= 0:
        print("Can't add zero or negative XP!")
        return
    
    player.experience += xp_amount
    print(f"{player.username} got {xp_amount} XP points!")
    
    
    xp_needed = player.level * 100
    while player.experience >= xp_needed:
        player.experience -= xp_needed
        player.level += 1
        player.money += 50
        print(f"Awesome! {player.username} reached level {player.level}!")
        xp_needed = player.level * 100  
    
    try:
        session.commit()
    except:
        session.rollback()
        print("Couldn't save XP changes...")

def show_player_stats(player: Player):
    print("\n=== PLAYER STATS ===")
    print(f"Name: {player.username}")
    print(f"Level: {player.level}")
    print(f"XP: {player.experience} (needs {player.level * 100} for next level)")
    print(f"Coins: {player.money}")
    print(f"Badges: {player.achievements if player.achievements else 'No badges yet'}")
    print("====================")