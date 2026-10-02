from typing import Literal
from pydantic import BaseModel, Field

class QueryAnalysis(BaseModel):
    """Structured analysis of a user query for RAG retrieval."""

    original_query: str = Field(
        description="The exact query provided by the user."
    )

    intent: Literal[
        "factual",
        "explanation",
        "comparison",
        "research",
        "summarization",
        "procedural",
        "unknown",
    ] = Field(
        description="The primary intent of the user's query."
    )

    complexity: Literal[
        "simple",
        "moderate",
        "complex",
    ] = Field(
        description="The complexity of the query."
    )

    entities: list[str] = Field(
        default_factory=list,
        description="Important concepts, technologies, people, papers, "
                    "organizations, or topics in the query."
    )

    needs_expansion: bool = Field(
        description="Whether the query should be expanded."
    )

    needs_decomposition: bool = Field(
        description="Whether the query should be decomposed into sub-queries."
    )

    needs_metadata_filter: bool = Field(
        description="Whether metadata filtering is required."
    )

    metadata_filters: dict[str, str] = Field(
        default_factory=dict,
        description="Metadata constraints extracted from the query."
    )

    retrieval_strategy: list[
        Literal["bm25", "vector", "graph"]
    ] = Field(
        description="Retrieval methods recommended for this query."
    )

    expanded_queries: list[str] = Field(
        default_factory=list,
        description="Alternative queries for retrieval."
    )

    sub_queries: list[str] = Field(
        default_factory=list,
        description="Decomposed sub-queries."
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Number of documents to retrieve."
    )