from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from dotenv import load_dotenv
import os

load_dotenv()
DB_USER = os.getenv("DB_USER")     # "root"
DB_PW = os.getenv("DB_PW")         # "1234"
DB_HOST = os.getenv("DB_HOST")     # "IP"
DB_PORT = os.getenv("DB_PORT")     # "3306"
DB_NAME = os.getenv("DB_NAME")     # "mydb"

DB_URL = f'mysql+pymysql://{DB_USER}:{DB_PW}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8'

engine = create_engine(DB_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False,autoflush=False, bind=engine)
Base = declarative_base()
