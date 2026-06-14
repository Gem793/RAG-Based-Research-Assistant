import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def rewrite_query(query):
    prompt = f"""
You are a query rewriting module for a retrieval system.

TASK:
Rewrite the user query to improve clarity for search WITHOUT changing its meaning.

RULES:
- Preserve the original intent exactly
- Do NOT add new concepts
- Do NOT add explanation words like "analysis", "comparison", "performance"
- Expand abbreviations if obvious (e.g., "algo" → "algorithm")
- Convert to a clear search-style question if needed
- Keep it short (max 12–15 words)
- Output ONLY the rewritten query

Examples:
"Which algo" → "Which algorithm"
"what is a* used for" → "What is A* algorithm used for"
"dijkstra vs a*" → "Dijkstra vs A* algorithm"

User Query:
{query}

Rewritten Query:
"""

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )

    return response.text.strip()