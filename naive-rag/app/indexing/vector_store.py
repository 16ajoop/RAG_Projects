import chromadb


client = chromadb.PersistentClient(
    path="vectorstore"
)


collection = client.get_or_create_collection(
    name="enterprise_documents"
)


def add_document(
    document_id,
    text,
    embedding,
    metadata
):
    collection.add(
        ids=[document_id],
        documents=[text],
        embeddings=[embedding],
        metadatas=[metadata]
    )