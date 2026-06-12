from pdf_parser import extract_text
from chunker import create_chunks
from retriever import create_embeddings, build_index, retrieve 
def main():
    text=extract_text("sample.pdf")
    chunks=create_chunks(text)
    model,embeddings=create_embeddings(chunks)
    index=build_index(embeddings)
    query=input("Ask a question: ")
    results=retrieve(query,model,index,chunks,3)
    for result in results:
        print(result)
        print("\n"+"="*80+"\n")
if __name__=="__main__":
    main()