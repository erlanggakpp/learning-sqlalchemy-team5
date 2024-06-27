from models.base import Base
from db import db
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Integer, DateTime
from flask_login import UserMixin
from datetime import datetime, timedelta
import bcrypt

def gmt_plus_7_now():
    return datetime.utcnow() + timedelta(hours=7)


class UserModel2(db.Model):
    __tablename__ = "users2"

    id = mapped_column(Integer, primary_key=True)
    email = mapped_column(String(255), unique=True)
    password = mapped_column(String(255))
    role = mapped_column(String(255))
    username = mapped_column(String(255))
    created_at = mapped_column(DateTime, default=gmt_plus_7_now)
    updated_at = mapped_column(DateTime, default=gmt_plus_7_now, onupdate=gmt_plus_7_now)


    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'role': self.role
        }
    
    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))