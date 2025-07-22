from fastapi import APIRouter
import aiomysql
import modules

router = APIRouter(
    prefix="/db",
    tags=["testing db functions"]
)

@router.get("/select/{query}")
async def read_item(query: str):
    conn = await modules.get_connection()

    async with conn.cursor(aiomysql.DictCursor) as cur:
        await cur.execute(query)
        results = await cur.fetchall()

    conn.close()

    return {"query": query, "result" : results}

@router.get("/class_test/{table_name}")
async def class_test(table_name: str):
    """이게 db to pd.DataFrame 예제코드입니다. 비동기 함수 안에서 await키워드 도배하면서 써주세요."""
    db = await modules.Manage.create()

    df = await db.read_table(table_name)

    await db.close()

    return {"result": df.to_dict(orient="records")}