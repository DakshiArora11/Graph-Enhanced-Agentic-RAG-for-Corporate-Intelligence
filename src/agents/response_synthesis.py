from config.settings import settings

def synthesize_response(user_query: str, vector_result: list = None, graph_result: list = None) -> str:
    # Prepare vector text
    vector_text = "\n".join(vector_result) if vector_result and vector_result else "No relevant documents found."

    # Prepare graph text
    graph_text = "\n".join(graph_result) if graph_result and graph_result else "No graph facts found."

    # Construct a simple response based on available data
    response = f"""
Based on the available information:

User Query: {user_query}

Vector Search Results:
{vector_text}

Graph Facts:
{graph_text}

This is a temporary response as the AI model is not available. Please check back later for enhanced responses.
"""
    return response.strip()