from dotenv import load_dotenv
import asyncio, aiomysql, os

from modules.schema import DB_TABLE_SETUP_QUERY

load_dotenv()

async def get_db_connection():
    conn = await aiomysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PW"),
        db=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT")),
        autocommit=True
    )
    return conn

async def insert_data_to_db():

    conn = await get_db_connection()

    async with conn.cursor(aiomysql.DictCursor) as cur:

        await cur.execute(DB_TABLE_SETUP_QUERY)

        results = await cur.fetchall()

    conn.close()

# 실행
asyncio.run(insert_data_to_db())
