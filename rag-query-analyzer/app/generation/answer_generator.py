from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama


llm = ChatOllama(
    model="llama3.2",
    temperature=0,
)


ANSWER_PROMPT = """
You are a helpful assistant in a Retrieval-Augmented Generation (RAG) system.

Answer the user's question using the provided context.

Rules:

1. Use the provided context as the primary source of information.
2. Do not invent facts that are not supported by the context.
3. If the context does not contain enough information to answer,
   clearly say that the available context is insufficient.
4. Give a clear and concise answer.
5. When comparing multiple approaches, organize the answer clearly.

User question:
{query}

Retrieved context:
{context}

Answer:
"""


prompt = ChatPromptTemplate.from_template(ANSWER_PROMPT)


answer_generator = prompt | llm