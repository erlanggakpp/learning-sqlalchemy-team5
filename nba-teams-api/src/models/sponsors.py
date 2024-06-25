from models.base import Base
from db import db
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey

class SponsorModel(db.Model):
    __tablename__ = "sponsors"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(255))
    industry = mapped_column(String(255))
    headquarter_location = mapped_column(String(255))


    # def to_dict(self):
    #     return {
    #         'id': self.id,
    #         'name': self.name,
    #         'city': self.city,
    #         'players': [player.to_dict() for player in self.players]
    #     }