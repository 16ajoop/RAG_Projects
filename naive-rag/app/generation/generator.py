from langchain_ollama import OllamaLLM


llm = OllamaLLM(
    model="llama3.2"
)


def generate_answer(prompt):
    response = llm.invoke(prompt)

    return response