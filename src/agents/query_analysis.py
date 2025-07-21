# src/agents/query_analysis.py
from typing import Literal

QueryType = Literal["graph", "vector", "hybrid"]

def classify_query_type(query: str) -> QueryType:
    """
    Simple rule-based classifier for deciding the query route.
    """
    query = query.lower()

    graph_keywords = [
        "who", "when", "where", "how many", "relationship",
        "filed by", "managed by", "based in", "define", "registered"
    ]

    vector_keywords = [
        "explain", "describe", "summarize", "what is", "give an overview",
        "insight", "details", "products", "sell", "overview"
    ]

    if any(k in query for k in graph_keywords):
        return "graph"
    elif any(k in query for k in vector_keywords):
        return "vector"
    else:
        return "hybrid"