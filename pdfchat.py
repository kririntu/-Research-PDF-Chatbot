# 📚 Multi-Paper Research Assistant

An AI-powered research assistant that allows users to upload multiple research papers (PDFs), ask questions, generate summaries, and understand relationships between papers using Retrieval-Augmented Generation (RAG).

---

## 🚀 Features

- 📄 Upload multiple research papers (PDF)
- 🔍 Semantic search using vector embeddings
- 🤖 Question answering using Llama 3.3 (Groq)
- 📝 Automatic summarization of uploaded papers
- 🔗 Finds relationships and common ideas across papers
- 💬 Maintains short conversation history
- ⚡ FastAPI backend
- 🎨 Streamlit frontend
- 🧠 Retrieval-Augmented Generation (RAG)

---

## 🛠 Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | Streamlit |
| Backend | FastAPI |
| LLM | Groq (Llama-3.3-70B-Versatile) |
| Embeddings | sentence-transformers/all-MiniLM-L6-v2 |
| Vector Database | ChromaDB |
| PDF Loader | LangChain PyPDFLoader |
| Text Splitter | RecursiveCharacterTextSplitter |
| Memory | ConversationBufferWindowMemory |
| Language | Python |

---

# Project Architecture

```
                 User
                  │
                  ▼
           Streamlit Frontend
                  │
                  ▼
            FastAPI Backend
                  │
        Upload Research Papers
                  │
                  ▼
            PyPDFLoader
                  │
                  ▼
      Recursive Text Splitter
                  │
                  ▼
     HuggingFace Embeddings
                  │
                  ▼
              ChromaDB
                  │
        Semantic Retrieval
                  │
                  ▼
       Conversation History
                  │
                  ▼
      Llama-3.3-70B (Groq)
                  │
                  ▼
        Final Research Answer
```

---

# How It Works

### Step 1 — Upload Papers

Users upload **3–4 research papers** in PDF format through the Streamlit interface.

---

### Step 2 — Document Processing

Each paper is

- Loaded using PyPDFLoader
- Split into chunks
- Metadata is attached
  - Paper name
  - Page number

Example metadata:

```
Paper: Paper1.pdf
Page: 5
```

---

### Step 3 — Embedding Generation

Each chunk is converted into embeddings using

```
sentence-transformers/all-MiniLM-L6-v2
```

These embeddings are stored inside **ChromaDB**.

---

### Step 4 — Semantic Retrieval

When a user asks a question,

Example:

> What are the similarities between these papers?

The system retrieves the top 4 most relevant chunks.

---

### Step 5 — Prompt Construction

The retrieved context, conversation history, and user question are combined into a prompt.

```
Conversation History

+

Retrieved Context

+

Current Question
```

---

### Step 6 — LLM Response

The prompt is sent to

```
Llama-3.3-70B-Versatile
```

running on Groq.

The model answers **only using the retrieved context**.

---

## Example Questions

### Paper Summary

- Summarize all uploaded papers.
- Give an overview of the research.
- What is the main contribution of each paper?

---

### Cross-Paper Comparison

- Compare these papers.
- What are the similarities?
- What are the differences?
- Which paper improves previous work?
- What problems are solved by each paper?

---

### Research Understanding

- Explain the proposed methodology.
- What datasets were used?
- What algorithms are proposed?
- What limitations are mentioned?
- What future work is suggested?

---

### General Questions

- Explain Equation (5).
- What is the main conclusion?
- Why did the authors choose this method?

---

# Project Structure

```
Research-Agent/
│
├── app.py                  # FastAPI backend
├── researchagent.py        # Research agent
├── frontend.py             # Streamlit frontend
├── uploads/                # Uploaded PDFs
├── requirements.txt
└── README.md
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/research-agent.git

cd research-agent
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

Linux

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Set Groq API Key

Linux

```bash
export GROQ_API_KEY="YOUR_API_KEY"
```

Windows

```cmd
set GROQ_API_KEY=YOUR_API_KEY
```

---

## Run FastAPI

```bash
uvicorn app:app --reload
```

Runs at

```
http://127.0.0.1:8000
```

---

## Run Streamlit

```bash
streamlit run frontend.py
```

---

# API Endpoints

## Upload PDFs

```
POST /uploadfile/
```

Uploads multiple PDF files and creates the vector database.

---

## Chat

```
POST /chat
```

Request

```json
{
    "question":"Summarize the uploaded papers"
}
```

Response

```json
{
    "answer":"..."
}
```

---

# Current Pipeline

```
Upload PDFs
      │
      ▼
Load Documents
      │
      ▼
Chunk Documents
      │
      ▼
Generate Embeddings
      │
      ▼
Store in ChromaDB
      │
      ▼
Retrieve Relevant Chunks
      │
      ▼
Build Prompt
      │
      ▼
Groq LLM
      │
      ▼
Research Answer
```

---

# Current Limitations

- Designed for a small collection of papers (approximately 3–4 PDFs).
- Uses a fixed retrieval size (`k=4`).
- Conversation memory is limited to the last three exchanges.
- Responses rely entirely on retrieved content and do not incorporate external knowledge.

---

# Future Improvements

- Multi-agent research workflow
- Paper clustering
- Citation-aware responses
- Research timeline generation
- Automatic literature review generation
- Knowledge graph construction
- PDF highlighting with source references
- Support for larger document collections
- Hybrid retrieval (vector + keyword search)

---

