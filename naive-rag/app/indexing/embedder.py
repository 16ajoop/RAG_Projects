from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(
    model = "nomic-embed-text"
)

def create_embedding(text):
    return embeddings.embed_query(text)