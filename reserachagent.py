import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_groq import ChatGroq
from langchain_classic.memory import ConversationBufferWindowMemory

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

import re
import nltk
from nltk.corpus import words

class ResearchAgent:

    def __init__(self, pdf_paths):

        if not pdf_paths:
            raise ValueError("Please provide at least one PDF path.")

        self.pdf_paths = pdf_paths

        self.embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0
        )

        self.memory = ConversationBufferWindowMemory(
            k=3,
            return_messages=True
        )

        self.vectordb = None
        self.retriever = None
        self.qa_chain = None

    # -----------------------------------------------------
    # Load PDFs
    # -----------------------------------------------------

    def load_papers(self):

        all_docs = []

        for pdf_path in self.pdf_paths:

            if not os.path.exists(pdf_path):
                raise FileNotFoundError(f"{pdf_path} not found.")

            loader = PyPDFLoader(pdf_path)
            documents = loader.load()

            splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )

            docs = splitter.split_documents(documents)

            for doc in docs:
                doc.metadata["paper_name"] = os.path.basename(pdf_path)

            all_docs.extend(docs)

        return all_docs

    # -----------------------------------------------------
    # Create Vector Database
    # -----------------------------------------------------

    def create_embeddings(self):

        documents = self.load_papers()

        self.vectordb = Chroma.from_documents(
            documents=documents,
            embedding=self.embedding_model,
            
        )

        self.retriever = self.vectordb.as_retriever(
            search_kwargs={"k": 4}
        )

    # -----------------------------------------------------
    # Retrieve Context
    # -----------------------------------------------------

    def retrieve_context(self, question):

        if self.retriever is None:
            raise ValueError("Retriever not initialized. Run create_embeddings().")

        docs = self.retriever.invoke(question)

        context = ""

        for doc in docs:

            paper = doc.metadata.get("paper_name", "Unknown")
            page = doc.metadata.get("page", "Unknown")

            context += (
                f"Paper: {paper}\n"
                f"Page: {page}\n"
                f"{doc.page_content}\n\n"
            )

        return context

    # -----------------------------------------------------
    # Conversation History
    # -----------------------------------------------------

    def get_history(self, _):

        messages = self.memory.load_memory_variables({})["history"]

        history = ""

        for message in messages:
            history += f"{message.type.upper()}: {message.content}\n"

        return history

    # -----------------------------------------------------
    # Prompt
    # -----------------------------------------------------

    def create_prompt(self):

        template = """
You are a helpful research assistant.

Answer ONLY using the supplied context.

Rule:


1. If the user's input is gibberish, random characters, meaningless text, or does not form a valid research question, reply exactly:
   "Please enter a meaningful research question."

2. Do not invent information.

Conversation History:
{history}

Context:
{context}

Question:
{question}

Answer:
"""

        return ChatPromptTemplate.from_template(template)

    # -----------------------------------------------------
    # Build Chain
    # -----------------------------------------------------

    def build_chain(self):

        if self.retriever is None:
            raise ValueError("Run create_embeddings() before build_chain().")

        self.qa_chain = (

            {
                "context": RunnableLambda(self.retrieve_context),
                "question": RunnablePassthrough(),
                "history": RunnableLambda(self.get_history),
            }

            | self.create_prompt()
            | self.llm
            | StrOutputParser()

        )

    # -----------------------------------------------------
    # Ask Question
    # -----------------------------------------------------

    def ask(self, question):

        if self.qa_chain is None:
            raise ValueError("Run build_chain() first.")

        answer = self.qa_chain.invoke(question)

        self.memory.save_context(
            {"input": question},
            {"output": answer}
        )

        return answer
