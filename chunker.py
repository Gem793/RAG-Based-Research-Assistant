from  langchain_text_splitters import RecursiveCharacterTextSplitter
def create_chunks(text):
    splitter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, separators=["\n\n","\n",". "," ",""])
    chunks=splitter.split_text(text)
    chunks=[chunk.strip() for chunk in chunks]
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