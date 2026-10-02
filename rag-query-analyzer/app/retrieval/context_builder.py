def build_context(documents: list) -> str:
    """Combine retrieved documents into a single context string."""

    context_parts = []

    for i, document in enumerate(documents, start=1):
        context_parts.append(
            f"[Document {i}]\n{document.page_content}"
        )

    return "\n\n".join(context_parts)