
from falkordb import FalkorDB
from langchain_ollama import OllamaEmbeddings


def main():
    embeddings = OllamaEmbeddings(
        model="nomic-embed-text:latest",
        base_url="http://localhost:11434",
    )

    question = "Which technologies does GraphMind use?"
    query_vector = embeddings.embed_query(question)

    db = FalkorDB(host="localhost", port=6379)
    graph = db.select_graph("aitch_graph")

    query = """
    CALL db.idx.vector.queryNodes(
        'DocumentChunk',
        'embedding',
        3,
        vecf32($embedding)
    )
    YIELD node, score
    RETURN node.chunk_number, node.text, score
    ORDER BY score DESC
    """

    result = graph.query(query, {"embedding": query_vector})

    print(f"\nQuestion: {question}")
    print("\nTop matching chunks:")

    for number, text, score in result.result_set:
        print(f"\nChunk {number} | Similarity: {score:.4f}")
        print(text[:400])

    db.close()


if __name__ == "__main__":
    main()