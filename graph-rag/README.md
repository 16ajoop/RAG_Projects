# GraphRAG: Knowledge Graph and Hybrid Retrieval

A Graph Retrieval-Augmented Generation (GraphRAG) project that combines knowledge graphs and vector-based retrieval to answer questions about enterprise documents. It uses an LLM to extract entities and relationships, stores graph data in FalkorDB, and combines retrieval results to generate context-aware answers.

## Key Features

- PDF loading and text cleaning
- Section-aware document chunking
- LLM-based entity and relationship extraction
- Knowledge graph construction and storage in FalkorDB
- Graph community detection using NetworkX
- Vector embeddings and similarity search using ChromaDB
- Hybrid retrieval experiments combining graph and vector context
- Reciprocal Rank Fusion (RRF) concepts explored in the wider RAG project
- Answer generation using a local Ollama model
- Extraction progress tracking to help resume processing



## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| PyMuPDF | PDF text extraction |
| Ollama — Llama 3.2 | Entity extraction and answer generation |
| Ollama — Nomic Embed Text | Text embeddings |
| FalkorDB | Knowledge graph storage |
| ChromaDB | Vector storage and retrieval |
| NetworkX | Graph analysis and community detection |
| LangChain | LLM and embedding integration |
| RRF | Combining retrieval results |
| Docker | Running FalkorDB |

## Architecture

```text
PDF Documents
     |
     v
Text Extraction and Cleaning
     |
     v
Text Chunking
     |
     v
Entity and Relationship Extraction
     |
     v
Knowledge Graph -----> FalkorDB
     |
     v
Community Detection
     |
     v
Query Analysis
     |
     +----> Graph Retrieval
     |
     +----> Vector Retrieval
                  |
                  v
          Hybrid Retrieval
                  |
                  v
             RRF Fusion
                  |
                  v
          Context and LLM
                  |
                  v
             Final Answer
```

## Prerequisites

- Python 3.12
- Docker Desktop
- Ollama
- Models: `llama3.2:latest` and `nomic-embed-text:latest`

Pull the models only if they are not already installed:

```powershell
ollama pull llama3.2
ollama pull nomic-embed-text
```

## Setup

Run these commands from the `graph-rag` project directory.

Create and activate a virtual environment:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Start FalkorDB

Create the container the first time:

```powershell
docker run -d --name falkordb -p 6379:6379 -p 3000:3000 falkordb/falkordb:latest
```

Start it again after it has been created:

```powershell
docker start falkordb
```

If the container is already running, you do not need to start it again.
Verify that the database is running and reachable on the host and port configured in the application. The current test scripts use localhost:6379

## Run the Project

Ensure Ollama is running and FalkorDB is available before executing the scripts.

Run the pipeline tests:

```powershell
python -m tests.test_pipeline
```

Test vector retrieval:

```powershell
python -m app.graph.test_vector_search
```

Test graph retrieval:

```powershell
python -m app.graph.test_graph_retrieval
```

Test hybrid retrieval:

```powershell
python -m app.graph.test_hybrid_retrieval
```

Test hybrid answer generation:

```powershell
python -m app.graph.test_hybrid_answer
```

Some scripts may depend on generated graph data or a populated database. Run the extraction and loading steps first if required by your implementation.

## Data

The project uses a synthetic enterprise knowledge base for demonstration and testing. Generated graph data is stored in `data/graph_data.json`.

## Example Questions

The synthetic company knowledge base can be used to explore questions such as:
 - Which technologies does GraphMind use?
 - Who works in the AI Research department?
 - Which projects are associated with which technologies?
 - How are employees, departments, and projects connected?
 - Is a particular business fact documented in the available knowledge base?

Answers depend on the information actually present in the source documents and successfully retrieved by the application. Unsupported facts should be reported as unavailable rather than invented.

## Current Implementation Status

The project has working components for document processing, entity and relationship extraction, graph storage, graph retrieval, and hybrid-answer experiments.

The synthetic knowledge base has previously produced an extracted graph containing 55 entities and 80 relationships. This count describes that extraction run and may change if the source documents or extraction logic change.

The hybrid-answer test has successfully generated an answer to a question about the technologies used by GraphMind.

## Future Improvements

- Add a user-friendly interface
- Expose the pipeline through a FastAPI service
- Improve retrieval evaluation and answer-quality metrics
- Add support for additional document formats

## Learning Objectives

This project demonstrates how knowledge graphs can complement vector search, how relationships between entities can support retrieval, and how multiple retrieval strategies can be combined to improve question answering.

## Learning Goals

This project helps explore:
 - Retrieval-Augmented Generation (RAG)
 - Knowledge graphs and entity relationships
 - Vector embeddings and semantic search
 - Graph-based retrieval
 - Hybrid retrieval strategies
 - Local LLM inference with Ollama
 - Practical integration of graph databases and vector databases

## Related Projects

This project belongs to my broader RAG learning repository, which also includes:

 - Naive RAG — a basic document retrieval and answer-generation pipeline.
 - RAG Query Analyzer — query analysis and more advanced retrieval techniques.
 - GraphRAG — knowledge graph construction and graph-plus-vector retrieval experiments.


## Repository

[View the RAG Projects repository on GitHub](https://github.com/16ajoop/RAG_Projects)
