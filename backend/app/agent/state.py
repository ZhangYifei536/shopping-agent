from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages


class ShoppingState(TypedDict, total=False):
    # 对话消息
    messages: Annotated[list, add_messages]

    # 用户原始需求
    user_query: str

    # 预算
    budget: float

    # 最多购买商品数量
    count: int

    # 商品筛选条件
    filters: dict

    # query_products 返回的候选商品
    candidates: list[dict]

    # 最终购物方案
    shopping_plan: dict

    strategy: str