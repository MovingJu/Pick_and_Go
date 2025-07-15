import os
import mysql.connector
import httpx
from dotenv import load_dotenv
import asyncio

load_dotenv()

def get_db_connection():
    conn = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST_LOCAL"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DB"),
        port=3306
    )
    return conn

async def get_data():
    area_code = 1
    url = f"https://apis.data.go.kr/B551011/KorService2/areaCode2?serviceKey=n9U5t0ZqsIP9s2Cp%2FjQusFphNyY00MK4yTI5ZmLGEUyeRGeH8AgeX4%2Fsi%2Ba8zxGLAnannZbWx1li1aV6EoJ0vg%3D%3D&numOfRows=10&pageNo=1&MobileOS=ETC&MobileApp=AppTest&areaCode={area_code}&_type=json"
    result: list[tuple[int, str]] = []
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            data = response.json()
        for i in data["response"]["body"]["items"]["item"]:
            code = int(i["code"])
            name = i["name"]
            print(code, name)
            result.append((code, name))
    except httpx.ConnectError as e:
        print("Connection Error:", e)
    
    return result

async def insert_data_to_db():
    rows = await get_data()
    conn = get_db_connection()
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO sigungu_sido (city_id, city_name, parent_city_id)
        VALUES (%s, %s);
    """
    try:
        cursor.executemany(insert_query, rows)
        conn.commit()
        print(f"{cursor.rowcount} rows inserted or updated.")
    except mysql.connector.Error as e:
        print("DB Error:", e)
    finally:
        cursor.close()
        conn.close()

# 실행
asyncio.run(insert_data_to_db())
