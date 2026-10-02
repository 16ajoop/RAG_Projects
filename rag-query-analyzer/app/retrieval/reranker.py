from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama


llm = ChatOllama(
    model="llama3.2",
    temperature=0,
)


RERANK_PROMPT = """
You are a document relevance evaluator.

Given a user query and a document, determine how relevant the
document is for answering the query.

Return ONLY a number from 0 to 10.

0 = completely irrelevant
10 = extremely relevant

User query:
{query}

Document:
{document}
"""


prompt = ChatPromptTemplate.from_template(RERANK_PROMPT)


def rerank(query: str, documents: list, top_k: int = 3):
    """Rerank retrieved documents using the LLM."""

    scored_documents = []

    for document in documents:

        response = (prompt | llm).invoke({
            "query": query,
            "document": document.page_content,
        })

        try:
            score = float(response.content.strip())
        except ValueError:
            score = 0

        scored_documents.append(
            (score, document)
        )

    scored_documents.sort(
        key=lambda item: item[0],
        reverse=True
    )

    return [
        document
        for score, document in scored_documents[:top_k]
    ]