from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

from app.settings import DATABASE_URL, ASYNC_DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def init_db():
    with engine.connect() as connection:
        connection.execute(text("CREATE SCHEMA IF NOT EXISTS"))
        connection.commit()
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)


# @asynccontextmanager
async def get_async_session():
    async with async_session() as session:
        yield session