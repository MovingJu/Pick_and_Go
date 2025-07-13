from fastapi import APIRouter

import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()

def get_db_connection():
    conn = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DB"),
        port=3306
    )
    return conn

@router.get("/sigungu")
def get_sigungu():
    # conn = get_db_connection()
    # cursor = conn.cursor()
    # cursor.execute("SELECT * FROM sigungu;")
    # result = cursor.fetchall()
    # cursor.close()
    # conn.close()
    return {"sigungu": "ulsan"}
