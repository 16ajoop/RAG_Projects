from typing import TypedDict

from models.query_analysis import QueryAnalysis
from models.query_expansion import QueryExpansion
from models.query_decomposition import QueryDecomposition


class RAGState(TypedDict):
    original_query: str

    # Query understanding
    analysis: QueryAnalysis | None
    expansion: QueryExpansion | None
    decomposition: QueryDecomposition | None

    # Retrieval
    retrieved_documents: list | None
    reranked_documents: list | None

    # Generation
    context: str | None
    answer: str | None