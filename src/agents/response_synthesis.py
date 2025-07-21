import google.generativeai as genai
from config.settings import settings

# Configure Gemini
try:
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    print("[Gemini Config Error]", str(e))
    model = None

def synthesize_response(user_query: str, vector_result: list = None, graph_result: list = None) -> str:
    if model is None:
        return "[Error: Gemini model not initialized]"

    # Prepare vector text
    vector_text = "\n".join(vector_result) if vector_result and vector_result else "No relevant documents found."

    # Prepare graph text
    graph_text = "\n".join(graph_result) if graph_result and graph_result else "No graph facts found."

    # Construct the prompt
    prompt = f"""
You are an intelligent assistant. A user asked the following question:

"{user_query}"

You are given:
Vector Search Results:
{vector_text}

Graph Facts:
{graph_text}

Based on the information above, generate a helpful and concise answer to the user's question.
"""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"[Error during Gemini response synthesis: {str(e)}]")
        return f"[Error during response synthesis: {str(e)}]"