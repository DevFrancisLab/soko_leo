from langgraph.graph import StateGraph, START
from state.state import State

from agents.router_agent import router_agent
from agents.market_price_agent import market_price_agent
from agents.market_news_agent import market_news_agent
from agents.crop_advisory_agent import crop_advisory_agent
from agents.market_finder_agent import market_finder_agent


def route(state):
    return state["route"]


def build_graph():

    builder = StateGraph(State)

    builder.add_node("router", router_agent)
    builder.add_node("market_price", market_price_agent)
    builder.add_node("market_news", market_news_agent)
    builder.add_node("crop_advisory", crop_advisory_agent)
    builder.add_node("market_finder", market_finder_agent)

    builder.add_edge(START, "router")

    builder.add_conditional_edges(
        "router",
        route,
        {
            "market_price":"market_price",
            "market_news":"market_news",
            "crop_advisory":"crop_advisory",
            "market_finder":"market_finder"
        }
    )

    return builder.compile()