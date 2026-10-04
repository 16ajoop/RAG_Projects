# RAG Query Analyzer

An Advanced RAG system that analyzes user queries before retrieval and uses multiple retrieval strategies to improve the quality of generated answers.

## Overview

Traditional RAG systems usually follow a simple pipeline:

```text
User Query
    ↓
Vector Search
    ↓
Retrieved Documents
    ↓
LLM
    ↓
Answer
```

This project improves that approach by analyzing the query before retrieval and combining multiple retrieval techniques.

The system can:

- Analyze the user's query
- Identify query intent and complexity
- Expand queries with additional search terms
- Decompose complex queries into smaller queries
- Perform vector-based retrieval
- Perform BM25 keyword retrieval
- Combine retrieval results using Reciprocal Rank Fusion (RRF)
- erank retrieved documents
- Build the final context
- Generate an answer using an LLM
- Orchestrate the workflow using LangGraph

## Architecture
                    User Query
                         │
                         ▼
                ┌─────────────────┐
                │  Query Analyzer │
                └────────┬────────┘
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
       Query Expansion      Query Decomposition
              │                     │
              └──────────┬──────────┘
                         ▼
                ┌─────────────────┐
                │ Retrieval Layer │
                └────────┬────────┘
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
        Vector Retrieval       BM25 Retrieval
              │                     │
              └──────────┬──────────┘
                         ▼
                 ┌─────────────┐
                 │     RRF     │
                 │  Fusion     │
                 └──────┬──────┘
                        ▼
                  ┌───────────┐
                  │ Reranking │
                  └─────┬─────┘
                        ▼
                ┌──────────────┐
                │Context Builder│
                └──────┬───────┘
                       ▼
                 ┌───────────┐
                 │    LLM    │
                 └─────┬─────┘
                       ▼
                 Final Answer


## Key Features
1. Query Analysis

The system analyzes the incoming query and extracts structured information such as:

Query intent
Query complexity
Entities
Retrieval requirements

The analysis is represented using structured Pydantic models.

2. Query Expansion

The original query can be expanded into additional search queries to improve document retrieval.

3. Query Decomposition

Complex questions can be broken down into smaller sub-queries before retrieval.

4. Hybrid Retrieval

The project combines two retrieval approaches:

Vector Retrieval

Uses semantic similarity between the query and document embeddings.

BM25 Retrieval

Uses keyword-based matching to find documents containing relevant terms.

5. Reciprocal Rank Fusion

Results from vector retrieval and BM25 retrieval are combined using Reciprocal Rank Fusion (RRF).

This allows results from different retrieval methods to be merged into a single ranked list.

6. Reranking

Retrieved documents are reranked before being passed to the generation stage.

7. LangGraph Workflow

LangGraph is used to organize the RAG pipeline into nodes and workflow steps.

This makes the retrieval process more structured and allows conditional processing based on the query.

8. LLM Generation

The final context is passed to an LLM to generate the answer.

## Project Structure

    rag-query-analyzer/
    │
    ├── app/
    │   ├── chains/
    │   │   ├── query_analyzer_chain.py
    │   │   ├── query_decomposition_chain.py
    │   │   └── query_expansion_chain.py
    │   │
    │   ├── embeddings/
    │   │   └── embedding_model.py
    │   │
    │   ├── generation/
    │   │   └── answer_generator.py
    │   │
    │   ├── graph/
    │   │   ├── nodes.py
    │   │   ├── state.py
    │   │   └── workflow.py
    │   │
    │   ├── ingestion/
    │   │   ├── document_chunker.py
    │   │   └── document_loader.py
    │   │
    │   ├── models/
    │   │   ├── query_analysis.py
    │   │   ├── query_decomposition.py
    │   │   └── query_expansion.py
    │   │
    │   ├── prompts/
    │   │   ├── query_analyzer_prompt.py
    │   │   ├── query_decomposition_prompt.py
    │   │   └── query_expansion_prompt.py
    │   │
    │   ├── retrieval/
    │   │   ├── bm25_retriever.py
    │   │   ├── context_builder.py
    │   │   ├── reranker.py
    │   │   ├── rrf.py
    │   │   └── vector_retriever.py
    │   │
    │   └── main.py
    │
    ├── data/
    │   └── documents/
    │       └── rag.txt
    │
    ├── requirements.txt
    ├── .gitignore
    └── README.md


## Technologies Used

| Technology       | Purpose                            |
| ---------------- | ---------------------------------- |
| Python           | Core programming language          |
| LangChain        | RAG components and LLM integration |
| LangGraph        | Workflow orchestration             |
| Ollama           | Local LLM and embedding models     |
| Llama 3.2        | Text generation                    |
| Nomic Embed Text | Document and query embeddings      |
| ChromaDB         | Vector storage and retrieval       |
| BM25             | Keyword-based retrieval            |
| Pydantic         | Structured query analysis          |
| RRF              | Retrieval result fusion            |



## Installation

1. Clone the repository
   
        git clone https://github.com/16ajoop/RAG_Projects.git

Navigate to the project:

        cd RAG_Projects/rag-query-analyzer
    
2. Create a virtual environment
   
        python -m venv .venv

Activate it on Windows:

        .\.venv\Scripts\Activate.ps1
    
3. Install dependencies
 
        pip install -r requirements.txt
   
5. Install Ollama models

Make sure Ollama is installed and running.
Pull the required models:

    ollama pull llama3.2
    ollama pull nomic-embed-text
    Running the Project

Run the application from the project directory:

    python -m app/main.py

The application will process the document and run the RAG workflow.

The exact execution flow may depend on the configuration in app/main.py.

What I Learned

Through this project, I learned how an Advanced RAG system can go beyond simple vector search.

## Project Classification

This project can be considered an Advanced RAG implementation because it extends basic vector retrieval with:

- Query analysis
- Query expansion
- Query decomposition
- Hybrid retrieval
- Reciprocal Rank Fusion
- Reranking
- Workflow orchestration

It is primarily an Advanced RAG pipeline rather than a fully autonomous agent.


### List of Questions:
Simple questions

    1. What is RAG?
    2. What is an LLM?
    3. What is a vector database?
    4. What is LangChain?
    5. What is LangGraph?
    6. What are embeddings?
    7. What is semantic search?
    8. What is hybrid search?

Questions that should trigger richer analysis

    9. How does RAG work?
    10. How does RAG differ from fine-tuning?
    11. What are the advantages of using RAG with LLMs?
    12. What are the limitations of RAG?
    13. How do embeddings help in RAG?
    14. How does a vector database retrieve relevant documents?
    15. How does hybrid search combine keyword and vector search?
    16. How does reranking improve RAG retrieval?

Complex / multi-part questions

    17. Explain how RAG works and compare it with fine-tuning.
    18. What are embeddings, how are they generated, and how are they used in RAG?
    19. Explain the difference between vector search, BM25 search, and hybrid search.
    20. What are the advantages and disadvantages of using RAG for enterprise applications?
    21. Explain how query expansion, query decomposition, retrieval, fusion, and reranking work together in an advanced RAG pipeline.
    22. Compare Naive RAG, Hybrid RAG, Advanced RAG, and Graph RAG.
    23. How does Graph RAG differ from traditional vector-based RAG, and when should I use each?
    24. How can an agent use RAG to retrieve information and make decisions?
    
# Author

Pooja V
GitHub: 16ajoop
