import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_answer(question,embedded_chunks):
    context="\n\n".join(embedded_chunks)
    prompt=f"""
You are a research assistant
You must answer the user's question based on ONLY the given context.
Do not refer to any external sources of information.
If the answer is not present in the context, say:
"I couldn't find that in the provided document."

Context:
{context}
Question:
{question}
Answer:
"""
    response=client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text