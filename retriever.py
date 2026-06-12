from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
def create_embeddings(chunks):
    model=SentenceTransformer("all-MiniLM-L6-v2")
    embeddings=model.encode(chunks)
    return model,embeddings 
def build_index(embeddings):
    embeddings=np.array(embeddings).astype("float32")
    index=faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    return index
def retrieve(query,model,index,chunks,k):
    query_embedding=model.encode([query])
    query_embedding=np.array(query_embedding).astype("float32")
    distances,indices=index.search(query_embedding,k)
    results=[]
    for i in indices[0]:
        results.append(chunks[i])
    return results