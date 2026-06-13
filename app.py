from pdf_parser import extract_text
from chunker import create_chunks
from retriever import create_embeddings, build_index, retrieve 
from llm import generate_answer
def main():
    pages=extract_text("sample.pdf")
    chunks=create_chunks(pages)
    chunk_texts=[chunk["text"] for chunk in chunks]
    embeddings=create_embeddings(chunk_texts)
    index=build_index(embeddings)
    query=input("Ask a question: ")
    retrieved_chunks=retrieve(query,index,chunks,6)
    if "author" in query.lower() or "title" in query.lower():
        retrieved_chunks = [chunks[0]] + retrieved_chunks
    retrieved_texts=[chunk["text"] for chunk in retrieved_chunks]
    answer=generate_answer(query,retrieved_texts)
    print("\nAnswer: ")
    print(answer)
    sources=set(chunk["page"] for chunk in retrieved_chunks[:3])
    print("\nTop Sources: ")
    for page in sorted(sources):
        print(f"\nPage {page}")
    # print("\nRetrieved Chunks: ")
    # for result in retrieved_chunks:
    #     print(f"\n--- Chunk {result['chunk_id']} | Page {result['page']} ---")
    #     print(result["text"][:500])
if __name__=="__main__":
    main()