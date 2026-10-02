from rank_bm25 import BM25Okapi


def create_bm25_retriever(chunks):
    """Create a BM25 retriever from document chunks."""

    tokenized_documents = [
        chunk.page_content.lower().split()
        for chunk in chunks
    ]

    bm25 = BM25Okapi(tokenized_documents)

    return bm25


def retrieve_bm25(bm25, chunks, query: str, k: int = 3):
    """Retrieve the most relevant chunks using BM25."""

    tokenized_query = query.lower().split()

    results = bm25.get_top_n(
        tokenized_query,
        chunks,
        n=k
    )

    return results