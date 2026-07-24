# Research PDF Chatbot

A conversational AI assistant for research papers built with LangChain, FastAPI, Streamlit, ChromaDB, HuggingFace Embeddings, and Groq Llama 3.3.

## Features

- Upload multiple PDF research papers
- Semantic search using ChromaDB
- Question answering with Groq Llama 3.3
- Conversation memory
- FastAPI backend
- Streamlit frontend
- Source-aware retrieval
- Multi-document support

## Tech Stack

- Python
- FastAPI
- Streamlit
- LangChain
- ChromaDB
- HuggingFace Embeddings
- Groq API
- Sentence Transformers

## Project Structure

backend/
frontend/

## Installation

```bash
git clone https://github.com/yourusername/Research-PDF-Chatbot.git

cd Research-PDF-Chatbot
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a .env file

```
GROQ_API_KEY=YOUR_API_KEY
```

Run backend

```bash
uvicorn app:app --reload
```

Run frontend

```bash
streamlit run pdfchat.py
```


## Future Improvements

- Hybrid Retrieval
- Cross-paper comparison
- Research paper summarization
- Citation generation
- GraphRAG
- Multi-agent workflow
