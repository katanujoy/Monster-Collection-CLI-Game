# db/models.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)

    monsters = relationship("Monster", back_populates="player")

class MonsterSpecies(Base):
    __tablename__ = 'monster_species'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)

    monsters = relationship("Monster", back_populates="species")

class Monster(Base):
    __tablename__ = 'monsters'

    id = Column(Integer, primary_key=True)
    nickname = Column(String)
    level = Column(Integer, default=1)

    player_id = Column(Integer, ForeignKey('players.id'))
    species_id = Column(Integer, ForeignKey('monster_species.id'))

    player = relationship("Player", back_populates="monsters")
    species = relationship("MonsterSpecies", back_populates="monsters")

class Battle(Base):
    __tablename__='battles'
    
    
    id = Column(Integer,primary_key=True)
    opponent_type = Column(string)
    result = Column(String)
    reward_money = Column(Integer)
    reward_xp = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)

    player = relationship("Player", back_populates="battles")
    