from pdf_parser import extract_text
from chunker import create_chunks
from retriever import create_embeddings, build_index, retrieve 
from llm import generate_answer
def main():
    text=extract_text("sample.pdf")
    chunks=create_chunks(text)
    embeddings=create_embeddings(chunks)
    index=build_index(embeddings)
    query=input("Ask a question: ")
    retrieved_chunks=retrieve(query,index,chunks,6)
    retrieved_chunks=[chunks[0]]+retrieved_chunks
    answer=generate_answer(query,retrieved_chunks)
    print("\nAnswer: ")
    print(answer)
    # print("\nRetrieved Chunks:\n")
    # for i, chunk in enumerate(retrieved_chunks):
    #     print(f"\n--- Chunk {i+1} ---")
    #     print(chunk[:500])
if __name__=="__main__":
    main()