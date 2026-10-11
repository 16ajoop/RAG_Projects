
from falkordb import FalkorDB
from langchain_ollama import OllamaEmbeddings


def main():
    question = "Which technologies does GraphMind use?"
    project_name = "GraphMind"

    # Step 1: Convert the question into an embedding
    embeddings = OllamaEmbeddings(
        model="nomic-embed-text:latest",
        base_url="http://localhost:11434",
    )
    query_vector = embeddings.embed_query(question)

    # Step 2: Connect to FalkorDB
    db = FalkorDB(host="localhost", port=6379)
    graph = db.select_graph("aitch_graph")

    # Step 3: Retrieve relevant document chunks
    vector_query = """
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

    vector_result = graph.query(
        vector_query,
        {"embedding": query_vector},
    )

    # Step 4: Retrieve connected graph facts
    graph_query = """
    MATCH (p:PROJECT {name: $project_name})-[r]-(related)
    RETURN type(r), related.name, labels(related)
    """

    graph_result = graph.query(
        graph_query,
        {"project_name": project_name},
    )

    # Step 5: Combine both retrieval results
    context_parts = []

    for number, text, score in vector_result.result_set:
        context_parts.append(
            f"[Document chunk {number}]\n{text}"
        )

    for relationship, entity, labels in graph_result.result_set:
        context_parts.append(
            f"[Graph fact] GraphMind -{relationship}-> {entity} "
            f"(type: {', '.join(labels)})"
        )

    combined_context = "\n\n".join(context_parts)

    print(f"\nQuestion: {question}")
    print("\n--- HYBRID RETRIEVAL CONTEXT ---")
    print(combined_context)

    db.close()


if __name__ == "__main__":
    main()