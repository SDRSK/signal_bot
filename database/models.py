from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import declarative_base, relationship
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    settings = relationship("UserSettings", back_populates="user")
    pairs = relationship("UserPair", back_populates="user")

class UserPair(Base):
    __tablename__ = "user_pairs"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    symbol = Column(String)
    market_type = Column(String)
    user = relationship("User", back_populates="pairs")

class Signal(Base):
    __tablename__ = "signals"
    id = Column(Integer, primary_key=True)
    symbol = Column(String)
    strategy = Column(String)
    price = Column(String)
    signal = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class UserSettings(Base):
    __tablename__ = "user_settings"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    auto_signals = Column(Boolean, default=False)
    interval = Column(Integer, default=60)
    strategies = Column(JSON)
    user = relationship("User", back_populates="settings")