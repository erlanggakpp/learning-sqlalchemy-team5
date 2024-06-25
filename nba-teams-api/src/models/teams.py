from models.base import Base
from db import db
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey

class TeamModel(db.Model):
    __tablename__ = "teams"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(255), unique=True)
    city = mapped_column(String(255))
    arena = mapped_column(String(255))
    owner = mapped_column(String(255))
    players = relationship("PlayerModel", back_populates='team')


    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'players': [player.to_dict() for player in self.players]
        }