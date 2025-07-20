from fastapi import APIRouter
import aiomysql
import modules

router = APIRouter(
    prefix="/db",
    tags=["testing db functions"]
)

@router.get("/insert/{query}")
async def read_item(query: str):
    conn = await modules.get_connection()

    async with conn.cursor(aiomysql.DictCursor) as cur:
        await cur.execute(query)
        results = await cur.fetchall()

    return {"query": query, "result" : results}