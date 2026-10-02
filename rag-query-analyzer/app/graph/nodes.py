from chains.query_analyzer_chain import query_analyzer_chain
from chains.query_expansion_chain import query_expansion_chain
from chains.query_decomposition_chain import query_decomposition_chain

from graph.state import RAGState


from ingestion.document_loader import load_documents
from ingestion.document_chunker import chunk_documents

from vectorstore.chroma_store import load_vectorstore

from retrieval.bm25_retriever import (
    create_bm25_retriever,
    retrieve_bm25,
)

from retrieval.rrf import reciprocal_rank_fusion
from retrieval.reranker import rerank
from retrieval.context_builder import build_context
from generation.answer_generator import answer_generator







def analyze_query(state: RAGState) -> dict:
    """Analyze the user's query and update the state."""

    query = state["original_query"]

    analysis = query_analyzer_chain.invoke({
        "query": query
    })

    # Make entity extraction more reliable for known technical terms.
    known_entities = [
        "RAG",
        "retrieval-augmented generation",
        "LLM",
        "LLMs",
        "RLHF",
        "DPO",
        "BM25",
        "vector",
        "graph",
        "knowledge grounding",
    ]

    query_lower = query.lower()

    detected_entities = [
        entity
        for entity in known_entities
        if entity.lower() in query_lower
    ]

    # Use deterministic entities when the LLM misses them.
    if detected_entities:
        analysis.entities = detected_entities

    return {
        "analysis": analysis
    }




def expand_query(state: RAGState) -> dict:
    """Expand the user's query and update the state."""

    expansion = query_expansion_chain.invoke({
        "query": state["original_query"]
    })

    return {
        "expansion": expansion
    }

def decompose_query(state: RAGState) -> dict:
    """Decompose the user's query and update the state."""

    decomposition = query_decomposition_chain.invoke({
        "query": state["original_query"]
    })

    return {
        "decomposition": decomposition
    }


def retrieve_documents(state: RAGState) -> dict:
    """Retrieve documents using vector search and BM25, then fuse results."""

    query = state["original_query"]

    # Load documents and create chunks for BM25
    documents = load_documents()
    chunks = chunk_documents(documents)

    # -------------------------
    # Vector retrieval
    # -------------------------

    vectorstore = load_vectorstore()

    vector_results = vectorstore.similarity_search(
        query,
        k=3,
    )

    # -------------------------
    # BM25 retrieval
    # -------------------------

    bm25 = create_bm25_retriever(chunks)

    bm25_results = retrieve_bm25(
        bm25,
        chunks,
        query,
        k=3,
    )

    # -------------------------
    # Reciprocal Rank Fusion
    # -------------------------

    fused_results = reciprocal_rank_fusion(
        [
            vector_results,
            bm25_results,
        ]
    )

    return {
        "retrieved_documents": fused_results
    }

def rerank_documents(state: RAGState) -> dict:
    """Rerank retrieved documents based on query relevance."""

    query = state["original_query"]
    documents = state["retrieved_documents"]

    if not documents:
        return {
            "reranked_documents": []
        }

    reranked_documents = rerank(
        query,
        documents,
        top_k=3,
    )

    return {
        "reranked_documents": reranked_documents
    }


def build_retrieval_context(state: RAGState) -> dict:
    """Build a clean context string from reranked documents."""

    documents = state["reranked_documents"]

    if not documents:
        return {
            "context": ""
        }

    context = build_context(documents)

    return {
        "context": context
    }



def generate_answer(state: RAGState) -> dict:
    """Generate the final answer using the query and retrieved context."""

    query = state["original_query"]
    context = state["context"]

    response = answer_generator.invoke({
        "query": query,
        "context": context or "",
    })

    return {
        "answer": response.content
    }