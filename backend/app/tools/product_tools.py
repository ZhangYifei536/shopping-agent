from backend.app.database.db import get_connection

# 综合商品查询工具
def query_products(
    keyword: str = None,
    category: str = None,
    min_price: float = None,
    max_price: float = None,
    min_protein: float = None,
    max_fat: float = None,
    max_carbohydrate: float = None,
    max_calories: float = None,
    sort_by: str = "price",
    descending: bool = False,
    limit: int = 20
):
    """
    综合商品查询工具。
    - 商品名称模糊搜索
    - 类别筛选
    - 价格区间筛选
    - 营养条件筛选
    - 按价格/蛋白质/脂肪/碳水/热量排序
    """

    allowed_sort_fields = {
        "price": "p.price",
        "protein": "n.total_protein",
        "fat": "n.total_fat",
        "carbohydrate": "n.total_carbohydrate",
        "calories": "n.total_calories"
    }

    if sort_by not in allowed_sort_fields:
        raise ValueError(f"不支持的排序字段: {sort_by}")

    if limit <= 0:
        limit = 20

    # 防止一次查询过多数据
    limit = min(limit, 100)

    conn = get_connection()

    try:
        with conn.cursor() as cursor:

            sql = """
            SELECT
                p.id,
                p.name,
                p.category,
                p.specification,
                p.price,

                n.total_calories,
                n.total_protein,
                n.total_fat,
                n.total_carbohydrate

            FROM product p

            JOIN nutrition n
                ON p.nutrition_id = n.id

            WHERE 1 = 1
            """

            params = []

            # 商品名称
            if keyword:
                sql += " AND p.name LIKE %s"
                params.append(f"%{keyword}%")

            # 商品类别
            if category:
                sql += " AND p.category = %s"
                params.append(category)

            # 最低价格
            if min_price is not None:
                sql += " AND p.price >= %s"
                params.append(min_price)

            # 最高价格
            if max_price is not None:
                sql += " AND p.price <= %s"
                params.append(max_price)

            # 最低蛋白质
            if min_protein is not None:
                sql += " AND n.total_protein >= %s"
                params.append(min_protein)

            # 最大脂肪
            if max_fat is not None:
                sql += " AND n.total_fat <= %s"
                params.append(max_fat)

            # 最大碳水
            if max_carbohydrate is not None:
                sql += " AND n.total_carbohydrate <= %s"
                params.append(max_carbohydrate)

            # 最大热量
            if max_calories is not None:
                sql += " AND n.total_calories <= %s"
                params.append(max_calories)

            order = "DESC" if descending else "ASC"

            sql += f"""
            ORDER BY {allowed_sort_fields[sort_by]} {order}
            LIMIT %s
            """

            params.append(limit)

            cursor.execute(sql, params)

            products = cursor.fetchall()

            # Decimal 转 float
            for product in products:
                product["price"] = float(product["price"])
                product["total_calories"] = float(
                    product["total_calories"]
                )
                product["total_protein"] = float(
                    product["total_protein"]
                )
                product["total_fat"] = float(
                    product["total_fat"]
                )
                product["total_carbohydrate"] = float(
                    product["total_carbohydrate"]
                )

            return products

    finally:
        conn.close()

if __name__ == "__main__":

    print("===== 综合查询测试 =====")

    result = query_products(
        category="乳制品",
        max_price=10,
        min_protein=5,
        max_fat=15,
        sort_by="protein",
        descending=True,
        limit=5
    )

    for item in result:
        print(item)