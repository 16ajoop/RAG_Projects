
import hashlib
import json
from pathlib import Path

from falkordb import FalkorDB
from langchain_ollama import OllamaEmbeddings

from app.loaders.pdf_loader import load_pdf
from app.processing.chunker import chunk_text


PDF_PATH = Path("data/documents/company_knowledge_base_graphrag.pdf")
GRAPH_NAME = "aitch_graph"
EMBEDDING_MODEL = "nomic-embed-text:latest"


def main():
    if not PDF_PATH.exists():
        raise FileNotFoundError(f"PDF not found: {PDF_PATH}")

    # 1. Load and chunk the source document using your existing pipeline.
    text = load_pdf(str(PDF_PATH))
    chunks = chunk_text(text)

    print(f"Document chunks: {len(chunks)}")

    # 2. Generate embeddings using the existing local Ollama model.
    embeddings = OllamaEmbeddings(
        model=EMBEDDING_MODEL,
        base_url="http://localhost:11434",
    )

    # 3. Connect to FalkorDB.
    db = FalkorDB(host="localhost", port=6379)
    graph = db.select_graph(GRAPH_NAME)

    # 4. Create the vector index if it doesn't already exist.
    indexes = graph.query("CALL db.indexes()").result_set
    index_exists = any(
        "DocumentChunk" in str(row) and "embedding" in str(row)
        and "VECTOR" in str(row).upper()
        for row in indexes
    )

    if not index_exists:
        graph.query(
            """
            CREATE VECTOR INDEX FOR (d:DocumentChunk) ON (d.embedding)
            OPTIONS {dimension: 768, similarityFunction: 'cosine'}
            """
        )
        print("Created DocumentChunk vector index.")

    # 5. Store each chunk with a stable ID and embedding.
    for number, chunk in enumerate(chunks, start=1):
        chunk_id = hashlib.sha256(
            f"{PDF_PATH.name}:{number}:{chunk}".encode("utf-8")
        ).hexdigest()[:16]

        vector = embeddings.embed_query(chunk)

        graph.query(
            """
            MERGE (d:DocumentChunk {id: $id})
            SET d.chunk_number = $number,
                d.text = $text,
                d.source = $source,
                d.embedding = vecf32($embedding)
            """,
            {
                "id": chunk_id,
                "number": number,
                "text": chunk,
                "source": PDF_PATH.name,
                "embedding": vector,
            },
        )

        print(f"Stored chunk {number}/{len(chunks)}")

    # 6. Report the number of stored chunks.
    result = graph.query(
        "MATCH (d:DocumentChunk) RETURN count(d) AS total"
    ).result_set

    print(f"\nDocument chunks stored in FalkorDB: {result[0][0]}")

    db.close()


if __name__ == "__main__":
    main()