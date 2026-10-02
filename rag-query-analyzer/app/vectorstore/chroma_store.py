from langchain_chroma import Chroma

from embeddings.embedding_model import embeddings


def create_vectorstore(chunks):
    """Create the vector store from document chunks."""

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name="rag_documents",
        persist_directory="data/chroma_db",
    )

    return vectorstore


def load_vectorstore():
    """Load the existing vector store."""

    vectorstore = Chroma(
        collection_name="rag_documents",
        embedding_function=embeddings,
        persist_directory="data/chroma_db",
    )

    return vectorstore