import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_answer(question,embedded_chunks):
    context="\n\n".join(embedded_chunks)
    prompt=f"""
You are a research assistant.

Answer the user's question using ONLY the given context.

- Extract answers directly from the context.
- You may use reasoning to interpret structure in the text (e.g., name lists for authors, or sentences expressing gratitude for acknowledgements).
- Do NOT use external knowledge.
- If a group of personal names appears in the same context as institutional affiliation, emails, or academic header information, treat them as authors.
Do not infer authorship from isolated or unrelated names.
- If the answer is not supported by the context, say:
"I couldn't find that in the provided document."

Context:
{context}
Question:
{question}
Answer:
"""
    response=client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )
    return response.text