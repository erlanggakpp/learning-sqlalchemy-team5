from models.base import Base
from db import db
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey

class PlayerModel(db.Model):
    __tablename__ = "players"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(255))
    nationality = mapped_column(String(255))
    age = mapped_column(Integer)
    team_id = mapped_column(Integer, ForeignKey("teams.id"), nullable=True)
    team = relationship("TeamModel", back_populates='players')

    def to_dict(self):
        return {    
            'id': self.id,
            'name': self.name,
            'nationality': self.nationality,
            'age': self.age
        }