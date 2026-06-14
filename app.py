from pdf_parser import extract_text
from chunker import create_chunks
from retriever import create_embeddings, build_index, retrieve, rerank
from query_rewriter import rewrite_query
from llm import generate_answer
pages=extract_text("sample.pdf")
chunks=create_chunks(pages)
chunk_texts=[chunk["text"] for chunk in chunks]
embeddings=create_embeddings(chunk_texts)
index=build_index(embeddings)
def main():
    query=input("Ask a question: ")
    rewritten_query=rewrite_query(query)
    retrieved_chunks=retrieve(rewritten_query,index,chunks,15)

    if "author" in rewritten_query.lower() or "title" in rewritten_query.lower():
        first_chunk = chunks[0].copy()
        first_chunk["distance"] = 0.0
        retrieved_chunks = [first_chunk] + retrieved_chunks
    reranked_chunks=rerank(rewritten_query,retrieved_chunks,5)
    retrieved_texts=[chunk["text"] for chunk in reranked_chunks]
    answer=generate_answer(rewritten_query,retrieved_texts)
    print("\nOriginal Query:")
    print(query)

    print("\nRewritten Query:")
    print(rewritten_query)
    print("\nAnswer: ")
    print(answer)
    sources=set(chunk["page"] for chunk in reranked_chunks)
    print("\nTop Sources: ")
    for page in sorted(sources):
        print(f"\nPage {page}")
    print("\nRetrieved Chunks: ")
    for result in reranked_chunks:
        print(
    f"\n--- Chunk {result['chunk_id']} | "
    f"Page {result['page']} | "
    f"Distance {result['distance']:.4f} | "
    f"Relevance Score {result.get('relevance_score',0):.4f} ---"
)
        print(result["text"][:500])
if __name__=="__main__":
    main()
    