# data_loader.py
# Handles loading, splitting, and vectorizing documents for the agentic_rag project.

from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from .config import URLS, CHUNK_SIZE, CHUNK_OVERLAP


def load_documents():
    """Fetch documents from the URLs specified in config.py."""
    docs = [WebBaseLoader(url).load() for url in URLS]
    docs_list = [item for sublist in docs for item in sublist]
    return docs_list


def split_documents(docs_list):
    """Split documents into chunks using tiktoken encoder."""
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )
    return text_splitter.split_documents(docs_list)


def create_vectorstore(doc_splits):
    """Create an in-memory vector store from document splits using OpenAI embeddings."""
    return InMemoryVectorStore.from_documents(
        documents=doc_splits, embedding=OpenAIEmbeddings()
    ) 