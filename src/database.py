from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

DATABASE_URL = "sqlite+aiosqlite:///./src/recipe.db"

engine = create_async_engine(DATABASE_URL, connect_args={"check_same_thread": False})
async_session = async_sessionmaker(engine, expire_on_commit=False)
Base = declarative_base()
