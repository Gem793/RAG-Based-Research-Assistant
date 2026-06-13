from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
model=SentenceTransformer("all-MiniLM-L6-v2")
def create_embeddings(chunk_texts):
    embeddings=model.encode(chunk_texts)
    return embeddings 
def build_index(embeddings):
    embeddings=np.array(embeddings).astype("float32")
    index=faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    return index
def retrieve(query,index,chunks,k):
    query_embedding=model.encode([query])
    query_embedding=np.array(query_embedding).astype("float32")
    distances,indices=index.search(query_embedding,k)
    results=[]
    for i in indices[0]:
        results.append({
            "chunk_id":chunks[i]["chunk_id"],
            "page":chunks[i]["page"],
            "text":chunks[i]["text"]
            "distances":float(distances[0][rank])
        })
    return results