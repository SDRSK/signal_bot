from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import asyncio

from config.settings import DATABASE_URL

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

async def init_db():
    from database.models import User
    Base.metadata.create_all(bind=engine)