from pydantic import BaseModel, Field


class QueryExpansion(BaseModel):
    """Structured output for query expansion."""

    original_query: str = Field(
        description="The original query provided by the user."
    )

    expanded_queries: list[str] = Field(
        description="Alternative versions of the original query for retrieval."
    )