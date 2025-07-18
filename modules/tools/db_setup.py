import os
import mysql.connector
import httpx
from dotenv import load_dotenv
import asyncio

load_dotenv()

def get_db_connection():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PW"),
        database=os.getenv("DB_NAME"),
        port=3306
    )
    return conn

async def get_data():
    END_POINT = "http://apis.data.go.kr/B551011/KorService2"
    SERVICE_TYPE = "lclsSystmCode2"
    SERVICE_KEY = "n9U5t0ZqsIP9s2Cp%2FjQusFphNyY00MK4yTI5ZmLGEUyeRGeH8AgeX4%2Fsi%2Ba8zxGLAnannZbWx1li1aV6EoJ0vg%3D%3D"
    NUM_OF_ROWS = 250

    url = f"{END_POINT}/{SERVICE_TYPE}?serviceKey={SERVICE_KEY}&numOfRows={NUM_OF_ROWS}&pageNo=1&MobileOS=ETC&MobileApp=App&_type=json&lclsSystmListYn=Y"
    
    result: list[tuple[str, str, str]] = []
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            data = response.json()
        
        PARENT_CODES: set[str] = set()
        for datas in data["response"]["body"]["items"]["item"]:
            PARENT_CODES.add(datas["lclsSystm2Cd"])
        print(PARENT_CODES)

        for PARENT_CODE in PARENT_CODES:
            for datas in data["response"]["body"]["items"]["item"]:
                if (datas["lclsSystm2Cd"] == PARENT_CODE):
                    code = datas["lclsSystm3Cd"]
                    name = datas["lclsSystm3Nm"]
                    print(code, name)
                    result.append((code, name, PARENT_CODE))
    except httpx.ConnectError as e:
        print("Connection Error:", e)
    
    return result

async def insert_data_to_db():
    rows = await get_data()

    conn = get_db_connection()
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO lclsSystmCode3 (lclsSystm3Cd, lclsSystm3Nm, parent_lclsSystm2Cd)
        VALUES (%s, %s, %s);
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
