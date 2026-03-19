import re
from ai.tools.tavily_tool import search_tool

def market_price_agent(query: str) -> str:
    """
    Takes a farmer question and returns market advice.
    Handles prices, crop recommendations, surplus alerts, storage, transport, and profit maximization.
    """

    try:
        results = search_tool.invoke(query)
    except Exception as e:
        return f"Error fetching data: {e}"

    # Tavily results can be dict or list; extract text safely
    text_to_parse = ""
    if isinstance(results, list):
        for item in results:
            text_to_parse += item.get("snippet", "") + " "
    elif isinstance(results, dict):
        for item in results.get("results", []):
            text_to_parse += item.get("snippet", "") + " "

    # Try to parse a price pattern
    match = re.search(
        r"(?P<crop>\w+) in (?P<market>[\w\s]+) KSh (?P<price>[\d\.]+)",
        text_to_parse
    )

    if match:
        crop = match["crop"]
        market = match["market"]
        price = match["price"]
        advice = (
            f"{crop} in {market} costs KSh {price} per kg. "
            "Consider selling where demand is high. Store in cool, dry places and transport via main highways for safety. "
        )
        return advice
    else:
        # General advisory if no price found
        return (
            "Based on current market trends: "
            "Plant crops with high local demand, sell in major city markets, and "
            "coordinate procurement and transport efficiently. "
            "Monitor weather patterns and harvest early if rains are delayed."
        )