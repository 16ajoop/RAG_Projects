from app.indexing.embedder import create_embedding
from app.indexing.vector_store import collection


def retrieve_documents(query, top_k=3):
    query_embedding = create_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results