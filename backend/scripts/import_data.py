import csv
import re
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

# 读取商品数据CSV文件
csv_path = "../../data/foods.csv"

#解析商品规格
def parse_specification(specification):
    """
    示例：
    250ml/盒 -> 250
    950ml/盒 -> 950
    500g/袋 -> 500
    """

    pattern = r"(\d+(?:\.\d+)?)\s*(ml|mL|ML|g|G)"

    match = re.search(pattern, specification)

    if not match:
        return None, None

    quantity = float(match.group(1))
    unit = match.group(2).lower()

    return quantity, unit


nutrition_sql = """
INSERT INTO nutrition
(
    total_calories,
    total_protein,
    total_fat,
    total_carbohydrate
)
VALUES (%s, %s, %s, %s)
"""

product_sql = """
INSERT INTO product
(
    name,
    category,
    specification,
    price,
    nutrition_id
)
VALUES (%s, %s, %s, %s, %s)
"""

try:
    with open(csv_path, "r", encoding="utf-8-sig") as file:

        reader = csv.reader(file)

        # 跳过表头
        next(reader)

        count = 0
        failed_count = 0

        for row in reader:

            if not row:
                continue

            if len(row) != 8:
                print("格式错误，跳过：", row)
                failed_count += 1
                continue

            try:
                # CSV 原始数据

                name = row[0].strip()
                category = row[1].strip()
                specification = row[2].strip()

                price = float(row[3])

                calories_per_100 = float(row[4])
                protein_per_100 = float(row[5])
                fat_per_100 = float(row[6])
                carbohydrate_per_100 = float(row[7])

                # 解析规格

                quantity, unit = parse_specification(specification)

                if quantity is None:
                    print(
                        f"无法解析规格，跳过："
                        f"{name} | {specification}"
                    )

                    failed_count += 1
                    continue

                # 计算整件商品总营养

                multiplier = quantity / 100

                total_calories = calories_per_100 * multiplier
                total_protein = protein_per_100 * multiplier
                total_fat = fat_per_100 * multiplier
                total_carbohydrate = carbohydrate_per_100 * multiplier

                # 保留两位小数
                total_calories = round(total_calories, 2)
                total_protein = round(total_protein, 2)
                total_fat = round(total_fat, 2)
                total_carbohydrate = round(
                    total_carbohydrate,
                    2
                )

                # 插入 nutrition

                cursor.execute(
                    nutrition_sql,
                    (
                        total_calories,
                        total_protein,
                        total_fat,
                        total_carbohydrate
                    )
                )

                # 获取刚插入的 nutrition.id
                nutrition_id = cursor.lastrowid

                # 插入 product

                cursor.execute(
                    product_sql,
                    (
                        name,
                        category,
                        specification,
                        price,
                        nutrition_id
                    )
                )

                count += 1

            except Exception as e:

                print(
                    f"处理商品失败：{row}"
                )

                print(
                    "错误信息：",
                    e
                )

                failed_count += 1

        # 所有数据成功处理后统一提交
        conn.commit()

        print("==============================")
        print(f"数据导入完成")
        print(f"成功：{count} 条")
        print(f"失败：{failed_count} 条")
        print("==============================")


except Exception as e:

    conn.rollback()

    print(
        "数据导入失败：",
        e
    )


finally:

    cursor.close()
    conn.close()