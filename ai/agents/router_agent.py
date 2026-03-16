def router_agent(state):

    question = state["messages"][-1].content.lower()

    if "price" in question or "market price" in question:
        return {"route": "market_price"}

    elif "news" in question or "why" in question:
        return {"route": "market_news"}

    elif "sell" in question or "best market" in question:
        return {"route": "market_finder"}

    else:
        return {"route": "crop_advisory"}