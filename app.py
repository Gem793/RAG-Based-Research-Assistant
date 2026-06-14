import streamlit as st
import base64
from pdf_parser import extract_text
from chunker import create_chunks
from retriever import create_embeddings, build_index, retrieve, rerank
from query_rewriter import rewrite_query
from llm import generate_answer
@st.cache_resource
def build_pipeline():
    pages = extract_text("sample.pdf")
    chunks = create_chunks(pages)

    chunk_texts = [chunk["text"] for chunk in chunks]
    embeddings = create_embeddings(chunk_texts)
    index = build_index(embeddings)

    return chunks, index



chunks, index = build_pipeline()
def show_pdf(file_path):
    from streamlit.components.v1 import html as st_html
    with open(file_path, "rb") as f:
        pdf_bytes = f.read()

    base64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
    iframe = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800px"></iframe>'

    try:
        st_html(iframe, height=800)
    except Exception:
        st.sidebar.error("Inline PDF blocked by browser/security policy.")
        st.sidebar.download_button("Download PDF", pdf_bytes, file_name="document.pdf", mime="application/pdf")


st.title("RAG Based Research Assistant")

st.markdown("### Research Paper: Web-Based Indoor Navigation System(Accepted and presented at IEEE CSR 2026 (publication pending))")

st.sidebar.title("Document Viewer")
show_pdf("sample.pdf")

query = st.text_input("Ask a question about the document")
if query:
    rewritten_query=rewrite_query(query)
    retrieved_chunks=retrieve(rewritten_query,index,chunks,10)

    if "author" in rewritten_query.lower() or "title" in rewritten_query.lower():
        first_chunk = chunks[0].copy()
        first_chunk["distance"] = 0.0
        retrieved_chunks = [first_chunk] + retrieved_chunks
    reranked_chunks=rerank(rewritten_query,retrieved_chunks,10)
    retrieved_texts=[chunk["text"] for chunk in reranked_chunks]
    answer=generate_answer(rewritten_query,retrieved_texts)
    st.subheader("Answer")
    st.write(answer)

    st.subheader("Rewritten Query")
    st.write(rewritten_query)

    st.subheader("Sources (Pages)")
    pages = sorted(set(c["page"] for c in reranked_chunks))
    st.write(pages)

    with st.expander("Retrieved Chunks"):
        for c in reranked_chunks:
            st.markdown(
                f"""
                **Chunk {c['chunk_id']} | Page {c['page']}**  
                Distance: `{c['distance']:.4f}` | Score: `{c.get('relevance_score', 0):.4f}`
                """
            )
            st.write(c["text"][:500])
            st.markdown("---")
#     print("\nOriginal Query:")
#     print(query)

#     print("\nRewritten Query:")
#     print(rewritten_query)
#     print("\nAnswer: ")
#     print(answer)
#     sources=set(chunk["page"] for chunk in reranked_chunks)
#     print("\nTop Sources: ")
#     for page in sorted(sources):
#         print(f"\nPage {page}")
#     print("\nRetrieved Chunks: ")
#     for result in reranked_chunks:
#         print(
#     f"\n--- Chunk {result['chunk_id']} | "
#     f"Page {result['page']} | "
#     f"Distance {result['distance']:.4f} | "
#     f"Relevance Score {result.get('relevance_score',0):.4f} ---"
# )
#         print(result["text"][:500])
# if __name__=="__main__":
#     main()
  