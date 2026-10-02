from pydantic import BaseModel, Field


class QueryDecomposition(BaseModel):
    """Structured output for query decomposition."""

    original_query: str = Field(
        description="The original query provided by the user."
    )

    sub_queries: list[str] = Field(
        description="Smaller independent queries derived from the original query."
    )