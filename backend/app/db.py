import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from .models import Base

def build_db_url():
    user = os.environ["DATABASE_USER"]
    password = os.environ["DATABASE_PASSWORD"]
    host = os.environ["DATABASE_HOST"]
    port = os.environ.get("DATABASE_PORT", "5432")
    name = os.environ["DATABASE_NAME"]
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"

def get_engine():
    return create_engine(build_db_url(), pool_pre_ping=True)

def get_session_factory(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(bind=engine, autoflush=False, autocommit=False)

def create_tables(engine: Engine):
    Base.metadata.create_all(bind=engine)

def db_ping(engine: Engine):
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))

def get_db_session() -> Generator[Session, None, None]:
    engine = get_engine()
    SessionLocal = get_session_factory(engine)
    with SessionLocal() as session:
        yield session