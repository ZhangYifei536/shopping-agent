import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from backend.app.agent.graph import build_graph

load_dotenv()

llm = ChatOpenAI(
    model="qwen3.8-max",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
)

graph = build_graph(llm)

result = graph.invoke(
    {
        "user_query": "我有50元预算，想买5种20元以内的高蛋白食品"
    }
)

print("===== 解析结果 =====")
print("预算：", result.get("budget"))
print("数量：", result.get("count"))
print("筛选条件：", result.get("filters"))


print("\n===== 候选商品 =====")

for product in result.get("candidates", [])[:10]:
    print(product)


print("\n===== 最终购物方案 =====")

plan = result.get("shopping_plan", {})

for product in plan.get("products", []):
    print(product)

print("总价格：", plan.get("total_price"))
print("剩余预算：", plan.get("remaining_budget"))

print("\n===== Agent最终回答 =====")

messages = result.get("messages", [])

if messages:
    print(messages[-1].content)
else:
    print("没有生成最终回答")