# game/battle_logic.py

import random
from db.models import Battle, Player
from db.session import session
from game.player_logic import gain_xp

def simulate_pve_battle(player: Player):
    print(f"{player.username} is fighting a wild monster...")

    win = random.choice([True, False])
    xp_reward = random.randint(20, 50)
    money_reward = random.randint(10, 30)

    if win:
        print("🎉 You won the battle!")
        gain_xp(session, player, xp_reward)
        player.money += money_reward
        result = "win"
    else:
        print("😞 You lost the battle.")
        result = "lose"
        xp_reward = 0
        money_reward = 0

    # Save the battle result
    battle = Battle(
        player_id=player.id,
        opponent_type="wild",
        result=result,
        reward_money=money_reward,
        reward_xp=xp_reward
    )

    session.add(battle)
    session.commit()
    print(f"📝 Battle result saved: {result.upper()}")

def initiate_battle_with_ai(session, player_id):
    try:
        player = session.query(Player).filter_by(id=player_id).first()
        if not player:
            return {"message": "Player not found."}

        simulate_pve_battle(player)
        return {"message": "Battle complete!"}
    except Exception as e:
        session.rollback()
        return {"message": f"Error during battle: {e}"}
