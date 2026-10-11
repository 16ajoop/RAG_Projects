
from falkordb import FalkorDB
from langchain_ollama import OllamaEmbeddings, ChatOllama


def main():
    question = "Which technologies does GraphMind use?"
    project_name = "GraphMind"

    embeddings = OllamaEmbeddings(
        model="nomic-embed-text:latest",
        base_url="http://localhost:11434",
    )

    llm = ChatOllama(
        model="llama3.2:latest",
        base_url="http://localhost:11434",
        temperature=0,
        num_ctx=2048,
        num_predict=128
    )

    query_vector = embeddings.embed_query(question)

    db = FalkorDB(host="localhost", port=6379)
    graph = db.select_graph("aitch_graph")

    try:
        # Retrieve relevant document chunks
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

        # Retrieve facts directly connected to GraphMind
        graph_query = """
        MATCH (p:PROJECT {name: $project_name})-[r]-(related)
        RETURN type(r), related.name, labels(related)
        """

        graph_result = graph.query(
            graph_query,
            {"project_name": project_name},
        )

        context_parts = []

        for number, text, score in vector_result.result_set:
            context_parts.append(
                f"Document chunk {number}:\n{text}"
            )

        for relationship, entity, labels in graph_result.result_set:
            context_parts.append(
                f"Graph fact: GraphMind -{relationship}-> {entity} "
                f"(type: {', '.join(labels)})"
            )

        context = "\n\n".join(context_parts)

        prompt = f"""
You are an assistant answering questions about AITech Solutions.

Answer the user's question using only the context below.
If the context does not contain the answer, say so.
Be concise and do not invent facts.
List technologies separately from departments and people.

Context:
{context}

Question:
{question}

Answer:
"""

        response = llm.invoke(prompt)

        print(f"\nQuestion: {question}")
        print("\n--- GENERATED ANSWER ---")
        print(response.content)

    finally:
        db.close()


if __name__ == "__main__":
    main()