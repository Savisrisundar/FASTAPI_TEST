from sys import modules
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from test_app import settings

Base=declarative_base()