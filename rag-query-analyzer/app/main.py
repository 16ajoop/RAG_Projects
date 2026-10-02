from graph.workflow import workflow


def main():
    query = input("\nEnter your question: ")

    initial_state = {
        "original_query": query,
        "analysis": None,
        "expansion": None,
        "decomposition": None,
        "retrieved_documents": None,
        "reranked_documents": None,
        "context": None,
        "answer": None,
    }

    result = workflow.invoke(initial_state)

    print("\n========== FINAL ANSWER ==========\n")
    print(result["answer"])


if __name__ == "__main__":
    main()