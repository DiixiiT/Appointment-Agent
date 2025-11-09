import os

from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

from rag.embeddings import get_embedding_model

PERSIST_DIR = "./insurance_db"


def build_vector_store(data_dir: str = "./data"):
    """
    Builds and persists the Chroma vector store from text files in the data directory.
    Run this once to create/update the insurance FAQ database.
    """
    embeddings = get_embedding_model()
    docs = []

    for filename in os.listdir(data_dir):
        if filename.endswith(".txt"):
            path = os.path.join(data_dir, filename)
            loader = TextLoader(path)
            docs.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    vectordb = Chroma.from_documents(
        documents=chunks, embedding=embeddings, persist_directory=PERSIST_DIR
    )
    vectordb.persist()
    print(f"✅ Vector store created successfully at {PERSIST_DIR}")


def load_vector_store():
    """
    Loads the persisted Chroma vector store for querying.
    """
    embeddings = get_embedding_model()
    vectordb = Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)
    return vectordb


if __name__ == "__main__":
    build_vector_store()
