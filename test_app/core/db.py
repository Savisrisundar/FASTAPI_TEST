from sys import modules
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from test_app import settings

Base=declarative_base()

db_connection_str= settings.db_async_connection_str
if "pytest" in modules:
    db_connection_str= settings.db_async_test_connection_str
    
async_engine=create_async_engine(db_connection_str, echo=True, future=True)

async def get_async_session()-> AsyncSession:
    async_session=sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
            