# RAG Based Research Assistant

A Retrieval-Augmented Generation (RAG) system that allows users to ask questions based on research paper, Web-Based Indoor Navigation System (Accepted and presented at IEEE CSR 2026 (publication pending)). The system retrieves relevant sections from the paper and uses the Gemini API to generate context-aware answers.

Live App: https://rag-based-research-assistant.streamlit.app/

---

## Features

- Ask questions about the authored research paper  
- Semantic search over paper content using embeddings  
- Context-aware answers using Gemini LLM  
- Streamlit-based interactive Q&A interface  
- Retrieval-Augmented Generation (RAG) for grounded responses  

---

## How it works

Research Paper → Chunking → Embeddings → Vector Search → Relevant Sections → Gemini API → Final Answer  

---

## Tech Stack

- Streamlit  
- Python  
- Sentence Transformers 
- FAISS  
- Google Gemini API  

---

## Use Case
- Research paper analysis
- Academic study assistant
- Document Q&A system
- Knowledge base chatbot

## Run Locally

```bash
git clone https://github.com/Gem793/RAG-Based-Research-Assistant.git
cd RAG-Based-Research-Assistant
pip install -r requirements.txt
streamlit run app.py
