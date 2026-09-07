def calculate_budget(
    products: list[dict],
    budget: float,
    count: int = 5,
    strategy: str = "protein_value"
):
    """
    根据候选商品列表、预算和性价比策略生成最终购物组合。

    参数：
    products:
        query_products() 返回的候选商品列表

    budget:
        总预算

    count:
        最多选择的商品数量

    strategy:
        排序策略，目前支持：
        - protein_value：蛋白质性价比 = total_protein / price
        - protein：总蛋白质优先
        - price：价格优先
    """

    if not products:
        return {
            "products": [],
            "product_count": 0,
            "budget": budget,
            "total_price": 0,
            "remaining_budget": budget,
            "total_protein": 0,
            "total_fat": 0,
            "total_carbohydrate": 0,
            "total_calories": 0
        }

    # =========================
    # 1. 复制候选列表
    # 避免直接修改原来的 products
    # =========================

    candidates = [product.copy() for product in products]


    # =========================
    # 2. 计算性价比
    # =========================

    for product in candidates:

        price = float(product["price"])

        product["price"] = price

        if price > 0:
            product["protein_value"] = round(
                float(product["total_protein"]) / price,
                2
            )
        else:
            product["protein_value"] = 0


    # =========================
    # 3. 根据策略排序
    # =========================

    if strategy == "protein_value":

        candidates.sort(
            key=lambda x: x["protein_value"],
            reverse=True
        )

    elif strategy == "protein":

        candidates.sort(
            key=lambda x: float(x["total_protein"]),
            reverse=True
        )

    elif strategy == "price":

        candidates.sort(
            key=lambda x: x["price"]
        )

    else:
        raise ValueError(
            f"不支持的预算策略: {strategy}"
        )


    # =========================
    # 4. 贪心选择商品
    # =========================

    selected_products = []
    total_price = 0.0

    for product in candidates:

        # 已达到商品数量上限
        if len(selected_products) >= count:
            break

        price = product["price"]

        # 加入该商品后不能超过预算
        if total_price + price > budget:
            continue

        selected_products.append(product)

        total_price += price


    # =========================
    # 5. 统计最终购物方案
    # =========================

    total_price = round(total_price, 2)

    total_protein = round(
        sum(
            float(product["total_protein"])
            for product in selected_products
        ),
        2
    )

    total_fat = round(
        sum(
            float(product["total_fat"])
            for product in selected_products
        ),
        2
    )

    total_carbohydrate = round(
        sum(
            float(product["total_carbohydrate"])
            for product in selected_products
        ),
        2
    )

    total_calories = round(
        sum(
            float(product["total_calories"])
            for product in selected_products
        ),
        2
    )


    # =========================
    # 6. 返回结果
    # =========================

    return {
        "products": selected_products,

        "product_count": len(selected_products),

        "budget": budget,

        "total_price": total_price,

        "remaining_budget": round(
            budget - total_price,
            2
        ),

        "total_protein": total_protein,

        "total_fat": total_fat,

        "total_carbohydrate": total_carbohydrate,

        "total_calories": total_calories
    }


# if __name__ == "__main__":
#
#     # 第一步：筛选符合条件的商品
#     candidates = query_products(
#         max_price=20,
#         min_protein=10,
#         max_fat=20,
#         limit=100
#     )
#
#     # 第二步：根据预算生成购物组合
#     result = calculate_budget(
#         products=candidates,
#         budget=50,
#         count=5,
#         strategy="protein_value"
#     )
#
#     print("===== 最终购物方案 =====")
#
#     for product in result["products"]:
#         print(product)
#
#     print("总价格：", result["total_price"])
#     print("剩余预算：", result["remaining_budget"])
#     print("总蛋白质：", result["total_protein"])