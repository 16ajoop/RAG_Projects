def create_prompt(query, retrieved_documents):

    context = "\n\n".join(retrieved_documents)

    prompt = f"""
You are an enterprise knowledge assistant.

Answer the user's question using only the provided context.

Context:
{context}

Question:
{query}

Answer:
"""

    return prompt