from typing import Optional

from pydantic import BaseModel, Field

from backend.app.agent.state import ShoppingState
from backend.app.tools.product_tools import query_products
from backend.app.tools.recommend_tools import calculate_budget

class ShoppingRequest(BaseModel):
    budget: Optional[float] = Field(
        default=None,
        description="用户总预算，单位为元"
    )

    count: int = Field(
        default=5,
        description="用户希望购买的商品种类数量"
    )

    keyword: Optional[str] = Field(
        default=None,
        description="商品名称关键词，例如牛奶、鸡胸肉"
    )

    category: Optional[str] = Field(
        default=None,
        description="商品类别，例如乳制品、肉类、零食、主食"
    )

    min_price: Optional[float] = None
    max_price: Optional[float] = None

    min_protein: Optional[float] = Field(
        default=None,
        description="单件商品最低总蛋白质"
    )

    max_fat: Optional[float] = Field(
        default=None,
        description="单件商品最高总脂肪"
    )

    max_carbohydrate: Optional[float] = Field(
        default=None,
        description="单件商品最高总碳水"
    )

    max_calories: Optional[float] = Field(
        default=None,
        description="单件商品最高总热量"
    )

    strategy: str = Field(
        default="protein_value",
        description="购物组合排序策略"
    )

def create_parse_request_node(llm):

    structured_llm = llm.with_structured_output(
        ShoppingRequest
    )

    def parse_request(state: ShoppingState):

        user_query = state["user_query"]

        prompt = f"""
        你是智能购物系统中的需求解析模块。

        你的任务是把用户自然语言需求解析成结构化购物条件。

        用户需求：
        {user_query}

        请严格遵守以下规则：

        1. budget
        表示用户的总购物预算。
        例如：
        “我有50元” -> budget=50

        2. count
        表示用户希望最终购买多少种商品。
        例如：
        “买5种” -> count=5

        3. keyword
        只有用户明确提到具体商品名称时才填写。
        例如：
        “牛奶” -> keyword="牛奶"
        “鸡胸肉” -> keyword="鸡胸肉"

        “高蛋白食品”“低脂食品”“健康食品”等不是商品名称，
        不能放入 keyword。

        4. category
        只有用户明确指定商品类别时才填写。

        允许的商品类别只能来自：
        乳制品、肉类、零食、主食、杂粮干货

        例如：
        “推荐乳制品” -> category="乳制品"
        “想买肉类” -> category="肉类"

        注意：
        “高蛋白食品”“低脂食品”“低热量食品”“健康食品”
        都是营养偏好，不是 category。
        遇到这些描述时 category 必须为空。

        5. min_price / max_price
        只有用户明确给出价格限制时才填写。

        例如：
        “20元以内” -> max_price=20
        “10元以上” -> min_price=10

        6. min_protein
        只有用户明确说出具体蛋白质数值时才填写。

        例如：
        “蛋白质至少20g” -> min_protein=20

        如果用户只是说“高蛋白”，不要自行猜测具体数值，
        min_protein 保持为空。

        7. max_fat
        只有用户明确说出具体脂肪数值时填写。

        例如：
        “脂肪不超过10g” -> max_fat=10

        如果只是说“低脂”，不要自行猜测具体数值。

        8. strategy

        如果用户说：
        “高蛋白”“蛋白质性价比高”
        -> strategy="protein_value"

        如果用户强调：
        “蛋白质最高”
        -> strategy="protein"

        如果用户强调：
        “便宜”“价格低”“省钱”
        -> strategy="price"

        如果没有明确偏好：
        -> strategy="protein_value"

        9. 不允许自行创造用户没有提供的数值。

        10. 未提供的字符串字段必须返回 null，而不是空字符串 ""。
        """

        result = structured_llm.invoke(prompt)

        filters = {
            "keyword": result.keyword,
            "category": result.category,
            "min_price": result.min_price,
            "max_price": result.max_price,
            "min_protein": result.min_protein,
            "max_fat": result.max_fat,
            "max_carbohydrate": result.max_carbohydrate,
            "max_calories": result.max_calories
        }

        # 删除值为 None 的字段
        filters = {
            key: value
            for key, value in filters.items()
            if value is not None and value != ""
        }

        return {
            "budget": result.budget,
            "count": result.count,
            "filters": filters,
            "strategy": result.strategy
        }

    return parse_request

def query_products_node(state: ShoppingState):

    filters = state.get("filters", {})

    candidates = query_products(
        **filters,
        limit=100
    )

    return {
        "candidates": candidates
    }

def calculate_budget_node(state: ShoppingState):

    candidates = state.get("candidates", [])

    budget = state.get("budget")

    count = state.get("count", 5)

    strategy = state.get(
        "strategy",
        "protein_value"
    )

    # 用户没有预算时，不做预算组合
    if budget is None:
        return {
            "shopping_plan": {
                "products": candidates[:count],
                "product_count": min(
                    len(candidates),
                    count
                ),
                "budget": None
            }
        }

    plan = calculate_budget(
        products=candidates,
        budget=budget,
        count=count,
        strategy=strategy
    )

    return {
        "shopping_plan": plan
    }

def create_generate_response_node(llm):
    def generate_response(state: ShoppingState):
        plan = state.get("shopping_plan", {})
        user_query = state.get("user_query", "")

        prompt = f"""
你是智能购物推荐助手。

用户原始需求：
{user_query}

系统已经计算出的购物方案：
{plan}

请根据购物方案生成简洁、清晰的中文推荐结果。

要求：
1. 不要修改商品名称、价格和营养数据。
2. 列出推荐商品。
3. 给出总价格和剩余预算。
4. 简要说明推荐理由。
5. 如果没有符合条件的商品，要明确说明。
"""

        response = llm.invoke(prompt)

        return {
            "messages": [response]
        }

    return generate_response