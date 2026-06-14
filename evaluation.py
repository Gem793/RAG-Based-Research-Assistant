from app import chunks, index
from retriever import retrieve, rerank
from query_rewriter import rewrite_query
from llm import generate_answer


evaluation_set = [
    {
        "question": "Who are the authors?",
        "expected_keywords": ["Akshya"]
    },
    {
        "question": "Whom would the authors like to thank?",
        "expected_keywords": ["Anuradha"]
    },
    {
        "question": "Which algorithm is used?",
        "expected_keywords": ["A*"]
    },
    {
        "question": "Which is more efficient A* or Dijkstra?",
        "expected_keywords": ["A*"]
    },
    {
        "question": "What is computation time of A*?",
        "expected_keywords": ["204"]
    }
    
]
def run_eval():

    passed = 0

    for item in evaluation_set:

        query = item["question"]

        # pipeline
        rewritten = rewrite_query(query)
        retrieved = retrieve(rewritten, index, chunks, 15)
        if "author" in rewritten.lower() or "title" in rewritten.lower():
            first_chunk = chunks[0].copy()
            first_chunk["distance"] = 0.0
            retrieved= [first_chunk] + retrieved
        reranked = rerank(rewritten, retrieved, 10)

        texts = [c["text"] for c in reranked]
        answer = generate_answer(rewritten, texts)

        print("\n====================")
        print("Q:", query)
        print("Rewritten:", rewritten)
        print("A:", answer)

        hit = all(
            kw.lower() in answer.lower()
            for kw in item["expected_keywords"]
        )

        print("RESULT:", "PASS" if hit else "FAIL")

        if hit:
            passed += 1

    print("\n====================")
    print(f"SCORE: {passed}/{len(evaluation_set)}")
if __name__ == "__main__":
    run_eval()