from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from dotenv import load_dotenv
import os

load_dotenv()
DB_USER = os.getenv("DB_USER")     # "root"
DB_PW = os.getenv("DB_PW")         # "1234"
DB_HOST = os.getenv("DB_HOST")     # "IP"
DB_PORT = os.getenv("DB_PORT")     # "3306"
DB_NAME = os.getenv("DB_NAME")     # "mydb"

DB_URL = f"mysql+aiomysql://{DB_USER}:{DB_PW}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(DB_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_async_session():
    async with async_session() as session:
        yield session