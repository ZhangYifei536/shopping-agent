import csv
from os import getenv

import pymysql
from dotenv import load_dotenv
load_dotenv()

conn = pymysql.connect(
    host="localhost",
    port=3306,
    user="root",
    password=getenv("DB_PASSWORD"),
    database="shopping_agent",
    charset="utf8mb4"
)

cursor = conn.cursor()

csv_path = "../../data/foods.csv"

sql = """
INSERT INTO product
(name, category, specification, price, calories, protein, fat, carbohydrate)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

try:
    with open(csv_path,"r",encoding="utf-8-sig") as f:
        reader = csv.reader(f)

        count = 0

        for row in reader:
            if not row:
                continue

            if len(row) != 8:
                print("跳过格式错误的数据：", row)
                continue

            name = row[0]
            category = row[1]
            specification = row[2]

            price = float(row[3])
            calories = float(row[4])
            protein = float(row[5])
            fat = float(row[6])
            carbohydrate = float(row[7])

            cursor.execute(
                sql,
                (
                    name,
                    category,
                    specification,
                    price,
                    calories,
                    protein,
                    fat,
                    carbohydrate
                )
            )

            count += 1

    conn.commit()

    print(f"数据导入成功，共导入 {count} 条商品数据")

except Exception as e:
    conn.rollback()
    print("数据导入失败：", e)

finally:
    cursor.close()
    conn.close()