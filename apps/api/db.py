import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from .config import settings

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set. Create a .env file in the repo root.")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

Base = declarative_base()
# Friendly error if psycopg isn't installed but URL expects it
try:
    engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
except ModuleNotFoundError as e:
    if "psycopg" in str(e):
        raise RuntimeError(
            "Database driver 'psycopg' is missing.\n"
            "Fix:\n"
            "  pip install 'psycopg[binary]'\n"
            "Also ensure DATABASE_URL uses: postgresql+psycopg://...\n"
        ) from e
    raise

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
