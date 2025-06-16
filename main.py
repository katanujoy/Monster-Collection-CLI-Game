# Monster CLI Game
from db.database import engine
from db.models import Base
from db.session import session
from game.player_logic import get_or_create_player, view_profile
from game.monster_logic import catch_monster, get_player_collection, level_up_monster
from game.battle_logic import initiate_battle_with_ai
from game.trading_logic import propose_trade, respond_to_trade, list_pending_trades_for_player
from seed import seed_monsters
from colorama import init, Fore, Style

init(autoreset=True)

# Create all tables
Base.metadata.create_all(engine)

# Seed monsters (only run once)
seed_monsters(session)

def trade_menu(player):
    while True:
        print("\n--- Trade Menu ---")
        print("1. View Pending Trades")
        print("2. Accept/Decline Trade")
        print("3. Propose New Trade")
        print("4. Back to Main Menu")

        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            try:
                trades = list_pending_trades_for_player(player.id)
                if not trades:
                    print(Fore.YELLOW + "📭 No pending trades.")
                else:
                    print(Fore.BLUE + "\n📋 Pending Trades:")
                    for t in trades:
                        print(f"Trade ID: {t.id} | From Player ID: {t.from_player_id} | "
                              f"Offers Monster ID: {t.from_monster_id} for your Monster ID: {t.to_monster_id}")
            except Exception as e:
                print(Fore.RED + f"❌ Error retrieving trades: {e}")

        elif choice == "2":
            try:
                trade_id = int(input("Enter Trade ID to respond to: "))
                decision = input("Accept this trade? (yes/no): ").strip().lower()
                accept = decision == "yes"
                result = respond_to_trade(trade_id, accept)
                print(Fore.GREEN + result["message"] if result["success"] else Fore.YELLOW + result["message"])
            except ValueError:
                print(Fore.RED + "⚠️ Enter a valid trade ID.")
            except Exception as e:
                print(Fore.RED + f"❌ Error responding to trade: {e}")

        elif choice == "3":
            try:
                to_player_id = int(input("Enter the recipient player's ID: "))
                from_monster_id = int(input("Enter your monster's ID to offer: "))
                to_monster_id = int(input("Enter the recipient's monster ID you want: "))
                result = propose_trade(player.id, to_player_id, from_monster_id, to_monster_id)
                print(Fore.CYAN + result["message"])
            except ValueError:
                print(Fore.RED + "⚠️ Please enter valid numbers.")
            except Exception as e:
                print(Fore.RED + f"❌ Error proposing trade: {e}")

        elif choice == "4":
            break
        else:
            print(Fore.RED + "⚠️ Invalid option. Choose 1-4.")

def main():
    print(Fore.CYAN + "🧃 Welcome to Monster CLI Game!")
    name = input("Enter your player name: ").strip()

    try:
        player = get_or_create_player(name)
        print(Fore.GREEN + f"Hello, {player.username}!")
    except Exception as e:
        print(Fore.RED + f"❌ Error fetching or creating player: {e}")
        return

    while True:
        print(Style.BRIGHT + "\n--- Main Menu ---")
        print("1. Catch a Monster")
        print("2. View Your Collection")
        print("3. Level Up a Monster")
        print("4. Battle an AI Trainer")
        print("5. Trade Monsters")
        print("6. View Profile")
        print("7. Exit")

        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            try:
                species_id = int(input("Enter species ID to catch (e.g., 1): "))
                result = catch_monster(session, player.id, species_id, player.level)
                print(Fore.YELLOW + result["message"])
            except ValueError:
                print(Fore.RED + "⚠️ Please enter a valid number.")
            except Exception as e:
                print(Fore.RED + f"❌ Error during catch attempt: {e}")

        elif choice == "2":
            try:
                collection = get_player_collection(session, player.id)
                if not collection:
                    print(Fore.YELLOW + "📭 You have no monsters yet.")
                else:
                    print(Fore.BLUE + "\n📜 Your Monsters:")
                    for m in collection:
                        print(f"- {m.species.name} (Level {m.level}) - Nickname: {m.nickname} | ID: {m.id}")
            except Exception as e:
                print(Fore.RED + f"❌ Failed to load collection: {e}")

        elif choice == "3":
            try:
                collection = get_player_collection(session, player.id)
                if not collection:
                    print(Fore.YELLOW + "📭 You have no monsters to level up.")
                    continue

                print("\nSelect a monster to level up:")
                for idx, m in enumerate(collection, start=1):
                    print(f"{idx}. {m.species.name} (Level {m.level}) - Nickname: {m.nickname}")

                selected = int(input("Choose by number: "))
                if 1 <= selected <= len(collection):
                    monster = collection[selected - 1]
                    result = level_up_monster(session, monster.id)
                    if result["success"]:
                        m = result["monster"]
                        print(Fore.GREEN + f"🎉 {m['nickname']} leveled up to {m['level']}!")
                    else:
                        print(Fore.YELLOW + result["message"])
                else:
                    print(Fore.RED + "⚠️ Invalid choice.")
            except ValueError:
                print(Fore.RED + "⚠️ Enter a number.")
            except Exception as e:
                print(Fore.RED + f"❌ Error during leveling up: {e}")

        elif choice == "4":
            try:
                result = initiate_battle_with_ai(session, player.id)
                print(Fore.MAGENTA + result["message"])
            except Exception as e:
                print(Fore.RED + f"❌ Error during battle: {e}")

        elif choice == "5":
            trade_menu(player)

        elif choice == "6":
            try:
                stats = view_profile(session, player.id)
                print(Fore.CYAN + f"\n📊 Profile for {stats['username']}:")
                print(f"Level: {stats['level']} | XP: {stats['experience']}")
                print(f"Money: 💰 {stats['money']} | Achievements: {stats['achievements']}")
                print(f"Total Monsters: {stats['collection_size']}")
            except Exception as e:
                print(Fore.RED + f"❌ Error loading profile: {e}")

        elif choice == "7":
            print(Fore.CYAN + "👋 Goodbye!")
            break

        else:
            print(Fore.RED + "⚠️ Invalid option. Please select 1-7.")

if __name__ == "__main__":
    main()
