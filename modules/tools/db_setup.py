from dotenv import load_dotenv
import asyncio, aiomysql, os

from crawl_data import get_data

load_dotenv()

async def get_db_connection():
    conn = await aiomysql.connect(
        host=os.getenv("DB_HOST"), # type: ignore
        password=os.getenv("DB_PW"), # type: ignore
        port=int(os.getenv("DB_PORT")), # type: ignore
        user=os.getenv("DB_USER"),
        db=os.getenv("DB_NAME"),
        autocommit=True
    )
    return conn


async def insert_data_to_db():

    DB_QUERY = """
INSERT INTO categoryCode3 (id, code, name, parent_code) VALUES (NULL, %s, %s, %s)
"""

    data = await get_data()

    conn = await get_db_connection()

    async with conn.cursor(aiomysql.DictCursor) as cur:

        await cur.executemany(DB_QUERY, data)

    conn.close()

# 실행
asyncio.run(insert_data_to_db())
