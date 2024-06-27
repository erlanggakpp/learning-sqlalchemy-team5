from models.base import Base
from db import db
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, DateTime
from datetime import datetime, timedelta

# Function to get current GMT+7 time
def gmt_plus_7_now():
    return datetime.utcnow() + timedelta(hours=7)

class TeamModel(db.Model):
    __tablename__ = "teams"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(255), unique=True)
    city = mapped_column(String(255))
    arena = mapped_column(String(255))
    owner = mapped_column(String(255))
    players = relationship("PlayerModel", back_populates='team')
    created_at = mapped_column(DateTime, default=gmt_plus_7_now)
    updated_at = mapped_column(DateTime, default=gmt_plus_7_now, onupdate=gmt_plus_7_now)


    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'players': [player.to_dict() for player in self.players]
        }