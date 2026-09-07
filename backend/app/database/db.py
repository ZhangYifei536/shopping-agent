import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

#返回数据库连接对象
def get_connection():
    return pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password=os.getenv("DB_PASSWORD"),
        database="shopping_agent",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )