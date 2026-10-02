from langchain_community.document_loaders import TextLoader


def load_documents():
    """Load all text documents from the documents directory."""

    loader = TextLoader(
        "data/documents/rag.txt",
        encoding="utf-8"
    )

    documents = loader.load()

    return documents