from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()
# Player model to represent players in the game
class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    level = Column(Integer, default=1)
    experience = Column(Integer, default=0)
    money = Column(Integer, default=0)

    monsters = relationship("Monster", back_populates="player")
    battles = relationship("Battle", back_populates="player")
    achievements = relationship("Achievement", back_populates="player") # Relationship to track player achievements

    # Relationships for trades
    sent_trades = relationship("Trade", back_populates="from_player", foreign_keys='Trade.from_player_id')
    received_trades = relationship("Trade", back_populates="to_player", foreign_keys='Trade.to_player_id')

# MonsterSpecies model to represent different species of monsters
class MonsterSpecies(Base):
    __tablename__ = 'monster_species'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    base_stats = Column(Integer)
    rarity = Column(String)
    abilities = Column(String)

    monsters = relationship("Monster", back_populates="species")

# Monster model to represent individual monsters owned by players
class Monster(Base):
    __tablename__ = 'monsters'

    id = Column(Integer, primary_key=True)
    nickname = Column(String)
    level = Column(Integer, default=1)

    player_id = Column(Integer, ForeignKey('players.id'))
    species_id = Column(Integer, ForeignKey('monster_species.id'))

    player = relationship("Player", back_populates="monsters")
    species = relationship("MonsterSpecies", back_populates="monsters")

    offered_trades = relationship("Trade", back_populates="from_monster", foreign_keys="Trade.from_monster_id")
    requested_trades = relationship("Trade", back_populates="to_monster", foreign_keys="Trade.to_monster_id")

# Battle model to track battles between players and AI
class Battle(Base):
    __tablename__ = 'battles'

    id = Column(Integer, primary_key=True)
    opponent_type = Column(String)
    result = Column(String)
    reward_money = Column(Integer)
    reward_xp = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)

    player_id = Column(Integer, ForeignKey('players.id'))
    player = relationship("Player", back_populates="battles")

# Trade model to handle player trades
class Trade(Base):
    __tablename__ = 'trades'

    id = Column(Integer, primary_key=True)
    from_player_id = Column(Integer, ForeignKey('players.id'))
    to_player_id = Column(Integer, ForeignKey('players.id'))
    from_monster_id = Column(Integer, ForeignKey('monsters.id'))
    to_monster_id = Column(Integer, ForeignKey('monsters.id'))
    status = Column(String, default="pending")

    from_player = relationship("Player", back_populates="sent_trades", foreign_keys=[from_player_id])
    to_player = relationship("Player", back_populates="received_trades", foreign_keys=[to_player_id])
    from_monster = relationship("Monster", back_populates="offered_trades", foreign_keys=[from_monster_id])
    to_monster = relationship("Monster", back_populates="requested_trades", foreign_keys=[to_monster_id])


#  Achievement model to track player achievements
class Achievement(Base):
    __tablename__ = 'achievements'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    player_id = Column(Integer, ForeignKey('players.id'))

    player = relationship("Player", back_populates="achievements")
