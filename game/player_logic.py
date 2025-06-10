# game/player_logic.py
from db.session import session
from db.models import Player

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
