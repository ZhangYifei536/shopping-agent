from langgraph.graph import StateGraph, START, END

from backend.app.agent.state import ShoppingState
from backend.app.agent.nodes import (
    create_parse_request_node,
    query_products_node,
    calculate_budget_node,
    create_generate_response_node
)


def build_graph(llm):
    graph = StateGraph(ShoppingState)

    # 注册节点
    graph.add_node(
        "parse_request",
        create_parse_request_node(llm)
    )

    graph.add_node(
        "query_products",
        query_products_node
    )

    graph.add_node(
        "calculate_budget",
        calculate_budget_node
    )

    graph.add_node(
        "generate_response",
        create_generate_response_node(llm)
    )
    # 定义流程
    graph.add_edge(
        START,
        "parse_request"
    )

    graph.add_edge(
        "parse_request",
        "query_products"
    )

    graph.add_edge(
        "query_products",
        "calculate_budget"
    )

    graph.add_edge(
        "calculate_budget",
        "generate_response"
    )

    graph.add_edge(
        "generate_response",
        END
    )

    return graph.compile()