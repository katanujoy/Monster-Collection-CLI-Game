from sqlalchemy.exc import SQLAlchemyError
from db.models import Trade, Player, Monster
from db.session import session


def propose_trade(from_player_id, to_player_id, from_monster_id, to_monster_id):
    """
    Propose a trade between two players involving their monsters.
    """
    try:
        # Fetch monsters
        from_monster = session.query(Monster).filter_by(id=from_monster_id).first()
        to_monster = session.query(Monster).filter_by(id=to_monster_id).first()

        # Validate monster existence
        if not from_monster or not to_monster:
            return {"success": False, "message": "One or both monsters do not exist."}

        # Validate ownership
        if from_monster.player_id != from_player_id:
            return {"success": False, "message": "You do not own the monster you're offering."}
        if to_monster.player_id != to_player_id:
            return {"success": False, "message": "The requested monster is not owned by the recipient."}

        # Create and save trade
        trade = Trade(
            from_player_id=from_player_id,
            to_player_id=to_player_id,
            from_monster_id=from_monster_id,
            to_monster_id=to_monster_id,
            status="pending"
        )
        session.add(trade)
        session.commit()

        return {"success": True, "message": "Trade proposed successfully.", "trade_id": trade.id}

    except SQLAlchemyError as e:
        session.rollback()
        return {"success": False, "message": f"Database error: {str(e)}"}


def respond_to_trade(trade_id, accept: bool):
    """
    Accept or decline a trade.
    """
    try:
        trade = session.query(Trade).filter_by(id=trade_id).first()
        if not trade or trade.status != "pending":
            return {"success": False, "message": "Invalid or already processed trade."}

        # Fetch monsters
        from_monster = session.query(Monster).filter_by(id=trade.from_monster_id).first()
        to_monster = session.query(Monster).filter_by(id=trade.to_monster_id).first()

        if not from_monster or not to_monster:
            return {"success": False, "message": "One or both monsters no longer exist."}

        if accept:
            # Swap monster ownership
            from_monster.player_id, to_monster.player_id = to_monster.player_id, from_monster.player_id
            trade.status = "accepted"
            session.commit()
            return {"success": True, "message": "Trade accepted and completed."}
        else:
            trade.status = "declined"
            session.commit()
            return {"success": True, "message": "Trade declined."}

    except SQLAlchemyError as e:
        session.rollback()
        return {"success": False, "message": f"Database error: {str(e)}"}


def list_pending_trades_for_player(player_id):
    """
    List all pending trades for a specific player.
    """
    try:
        return session.query(Trade).filter_by(to_player_id=player_id, status="pending").all()
    except SQLAlchemyError as e:
        print(f"[Error] Couldn't fetch trades: {e}")
        return []
