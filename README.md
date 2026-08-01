# Research Paper RAG Assistant

## Overview

A Retrieval-Augmented Generation (RAG) application built using **LangChain, ChromaDB, HuggingFace Embeddings, Groq LLM, FastAPI, and Streamlit**.

The system allows users to upload one or more research papers and ask questions grounded only in the uploaded documents. It retrieves the most relevant sections from the papers and generates accurate, context-aware answers using a Large Language Model.

---

## 🚀 Live Deployment

- **Frontend (Streamlit):**
  *Add your Streamlit URL here*

- **Backend (FastAPI):**
  *Add your Render URL here*

---

## ✨ Features

- Multi-PDF research paper support
- Retrieval-Augmented Generation (RAG)
- Semantic search using ChromaDB
- HuggingFace sentence embeddings
- Short-term conversation memory
- Source-aware retrieval with paper name and page number
- Prompt-based hallucination prevention
- Rejects meaningless or gibberish queries
- FastAPI backend with Streamlit frontend

---

## 🧠 Tech Stack

- Python
- LangChain
- ChromaDB
- HuggingFace Embeddings
- Groq Llama 3.3 70B
- FastAPI
- Streamlit
- PyPDFLoader
- NLTK

---

## 🏗️ System Architecture

```text
               User
                 │
                 ▼
      Streamlit Frontend (pdfchat.py)
                 │
                 ▼
        FastAPI Backend (app.py)
                 │
                 ▼
          Upload Research PDFs
                 │
                 ▼
            PyPDFLoader
                 │
                 ▼
   RecursiveCharacterTextSplitter
                 │
                 ▼
 HuggingFace Embeddings (MiniLM-L6-v2)
                 │
                 ▼
        Chroma Vector Database
                 │
                 ▼
      Top-K Semantic Retrieval
                 │
                 ▼
 ConversationBufferWindowMemory
                 │
                 ▼
        Prompt Construction
                 │
                 ▼
      Groq Llama-3.3-70B Model
                 │
                 ▼
        Context-Aware Response
```

---

## 📁 Project Structure

```text
Research-Paper-RAG/
│
├── agent.py
├── app.py
├── pdfchat.py
├── requirements.txt
├── README.md
├── docs/
├── uploads/
└── screenshots/
```

---

## ⚙️ Installation

```bash
git clone https://github.com/kririntu/-Research-PDF-Chatbot.git

cd Research-PDF-Chatbot

pip install -r requirement.txt
```

---

## 🔐 Environment Variables

Create a `.env` file:

```text
GROQ_API_KEY=your_groq_api_key
```

---

## ▶️ Run Locally

### Start Backend (FastAPI)

```bash
uvicorn app:app --reload
```

Backend runs at:

```
http://127.0.0.1:8000
```

---

### Start Frontend (Streamlit)

```bash
streamlit run pdfchat.py
```

Frontend runs at:

```
http://localhost:8501
```

---

## 🔄 RAG Pipeline

1. Upload one or more research papers.
2. Extract text using **PyPDFLoader**.
3. Split documents into overlapping chunks.
4. Generate embeddings using **sentence-transformers/all-MiniLM-L6-v2**.
5. Store embeddings in **ChromaDB**.
6. Retrieve the Top-4 most relevant document chunks.
7. Load recent conversation history.
8. Construct the prompt.
9. Generate the final response using **Groq Llama-3.3-70B**.

---

## 🛡️ Prompt Guardrails

The assistant follows strict prompt rules to improve response reliability.

- Answers **only** using the retrieved document context.
- Does **not** invent or hallucinate information.
- Rejects meaningless, random, or gibberish inputs.
- Uses recent conversation history for follow-up questions.
- Grounds every response in the uploaded research papers.

---

## 💬 Conversation Memory

The application uses **ConversationBufferWindowMemory** with a window size of **3**, allowing users to ask follow-up questions while maintaining contextual continuity without excessive memory usage.

---

## 📄 Document Processing

Each uploaded research paper is:

- Loaded using **PyPDFLoader**
- Split into chunks of **1000 characters**
- Uses **200-character overlap**
- Tagged with:
  - Paper name
  - Page number

This metadata helps identify the source of retrieved information.

---

## 🧩 Design Decisions

- Retrieval-Augmented Generation for document-grounded responses
- ChromaDB for efficient semantic search
- Lightweight MiniLM embeddings for fast retrieval
- Groq Llama-3.3-70B for high-quality answer generation
- Prompt-based hallucination prevention
- Short-term conversation memory
- Metadata tracking with paper name and page number
- Modular architecture separating retrieval, prompting, memory, API, and UI

---

## 🔮 Future Improvements

- Hybrid Search (BM25 + Vector Search)
- Cross-Encoder Re-ranking
- Persistent Chroma Database
- Citation highlighting in responses
- Multi-agent research assistant
- Research paper summarization
- Figure and table understanding
- OCR support for scanned PDFs
- Long-term conversation memory
- Web search integration for unanswered questions

---

