from db.database import Session
from game.player_logic import create_player

session = Session()

def main():
    username = input("Enter your player name: ")
    player = create_player(session, username)
    print(f"Welcome, {player.username}!")

if __name__ == "__main__":
    main()
