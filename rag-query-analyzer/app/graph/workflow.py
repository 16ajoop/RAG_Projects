from langgraph.graph import StateGraph, START, END

from graph.state import RAGState

from graph.nodes import (
    analyze_query,
    expand_query,
    decompose_query,
    retrieve_documents,
    rerank_documents,
    build_retrieval_context,
    generate_answer,
)

# 1. Create the graph
builder = StateGraph(RAGState)



# 2. Add  nodes
builder.add_node("analyze", analyze_query)
builder.add_node("expand", expand_query)
builder.add_node("decompose", decompose_query)
builder.add_node("retrieve", retrieve_documents)
builder.add_node("rerank", rerank_documents)
builder.add_node("context", build_retrieval_context)
builder.add_node("generate", generate_answer)



# 3. Connect START to analyzer
builder.add_edge(START, "analyze")



def route_after_analysis(state: RAGState) -> str:
    analysis = state["analysis"]

    if analysis is None:
        return "retrieve"

    if analysis.needs_expansion:
        return "expand"

    if analysis.needs_decomposition:
        return "decompose"

    return "retrieve"



builder.add_conditional_edges(
    "analyze",
    route_after_analysis,
    {
        "expand": "expand",
        "decompose": "decompose",
        "retrieve": "retrieve",
    },
)



# 6. Decide what to do after expansion
def route_after_expansion(state: RAGState) -> str:

    analysis = state["analysis"]

    if analysis is not None and analysis.needs_decomposition:
        return "decompose"
    
    return "retrieve"



builder.add_conditional_edges(
    "expand",
    route_after_expansion,
    {
        "decompose": "decompose",
        "retrieve": "retrieve",
    },
)


builder.add_edge("decompose", "retrieve")
builder.add_edge("retrieve", "rerank")
builder.add_edge("rerank", "context")
builder.add_edge("context", "generate")
builder.add_edge("generate", END)


# 9. Compile the graph
workflow = builder.compile()



