from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase


engine = create_async_engine("sqlite+aiosqlite:///my_base.db")

session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass



async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)



async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)