from  langchain_text_splitters import RecursiveCharacterTextSplitter
def create_chunks(pages):
    splitter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, separators=["\n\n","\n",". "," ",""])
    chunks=[]
    chunk_id=0
    for page in pages:
        page_num=page["page"]
        page_chunks=splitter.split_text(page["text"])
        for chunk in page_chunks:
            chunks.append({
                "chunk_id":chunk_id,
                "page":page_num,
                "text":chunk.strip()
            })
            chunk_id+=1
    return chunks
# def create_chunks(text,chunk_size=1000, overlap=200):
#     chunks=[]
#     start=0
#     while(start<len(text)):
#         end=start+chunk_size
#         chunk=text[start:end]
#         chunks.append(chunk)
#         start=end-overlap
#     return chunks