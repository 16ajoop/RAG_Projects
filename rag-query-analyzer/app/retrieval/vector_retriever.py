from vectorstore.chroma_store import load_vectorstore


def retrieve(query: str, k: int = 3):
    """Retrieve the most relevant chunks for a query."""

    vectorstore = load_vectorstore()

    results = vectorstore.similarity_search(
        query,
        k=k
    )

    return results