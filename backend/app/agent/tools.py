from langchain.tools import tool

from backend.app.tools.product_tools import (
    query_products as query_products_service
)

from backend.app.tools.recommend_tools import (
    calculate_budget as calculate_budget_service
)

@tool
def query_products(
    keyword: str | None = None,
    category: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    min_protein: float | None = None,
    max_fat: float | None = None,
    max_carbohydrate: float | None = None,
    max_calories: float | None = None,
    sort_by: str = "price",
    descending: bool = False,
    limit: int = 20
) -> list[dict]:
    """
    根据用户的商品需求查询候选商品。

    支持根据商品名称、类别、价格、蛋白质、脂肪、
    碳水化合物和热量进行筛选，并支持排序。

    当用户需要查找、筛选或比较商品时使用此工具。
    """

    return query_products_service(
        keyword=keyword,
        category=category,
        min_price=min_price,
        max_price=max_price,
        min_protein=min_protein,
        max_fat=max_fat,
        max_carbohydrate=max_carbohydrate,
        max_calories=max_calories,
        sort_by=sort_by,
        descending=descending,
        limit=limit
    )


@tool
def calculate_budget(
    products: list[dict],
    budget: float,
    count: int = 5,
    strategy: str = "protein_value"
) -> dict:
    """
    根据候选商品、用户预算和选择策略生成最终购物组合。

    products 应当来自 query_products 工具返回的候选商品。

    budget 表示用户总预算。

    count 表示最多选择多少种商品。

    strategy 支持：
    - protein_value：优先选择蛋白质性价比高的商品
    - protein：优先选择总蛋白质高的商品
    - price：优先选择价格低的商品

    当已经获得候选商品，需要在预算范围内进一步选择商品时使用。
    """

    return calculate_budget_service(
        products=products,
        budget=budget,
        count=count,
        strategy=strategy
    )

tools = [
    query_products,
    calculate_budget
]

# if __name__ == "__main__":
#
#     print("===== Tool 信息 =====")
#
#     for t in tools:
#         print("Tool名称：", t.name)
#         print("Tool描述：", t.description)
#         print("参数结构：", t.args)
#         print()