from app.retrieval.retriever import retrieve_documents
from app.generation.prompt import create_prompt
from app.generation.generator import generate_answer


def ask_question(query, top_k=3):

    # Step 1: Retrieve relevant documents
    results = retrieve_documents(
        query,
        top_k=top_k
    )

    # Step 2: Get retrieved text
    retrieved_documents = results["documents"][0]

    # Step 3: Create augmented prompt
    prompt = create_prompt(
        query,
        retrieved_documents
    )

    # Step 4: Generate answer
    answer = generate_answer(prompt)

    return answer