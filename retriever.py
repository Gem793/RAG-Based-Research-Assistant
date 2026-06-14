from sentence_transformers import SentenceTransformer
from sentence_transformers import CrossEncoder
import numpy as np
import faiss
model=SentenceTransformer("all-MiniLM-L6-v2")
reranker=CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
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
    for rank,i in enumerate(indices[0]):
        results.append({
            "chunk_id":chunks[i]["chunk_id"],
            "page":chunks[i]["page"],
            "text":chunks[i]["text"],
            "distance":float(distances[0][rank])
        })
    return results
def rerank(query,chunks,k):
    pairs=[(query,chunk["text"]) for chunk in chunks]
    scores=reranker.predict(pairs)
    ranked=sorted(zip(chunks,scores),
           key=lambda x:x[1],
           reverse=True)
    reranked=[]
    for chunk,score in ranked[:k]:
        chunk_copy=chunk.copy()
        chunk_copy["relevance_score"]=float(score)
        reranked.append(chunk_copy)
    return reranked
    
