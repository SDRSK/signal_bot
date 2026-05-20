from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    telegram_id = Column(String, unique=True)


class UserPair(Base):

    __tablename__ = "user_pairs"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    symbol = Column(String)