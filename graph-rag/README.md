# GraphRAG: Knowledge Graph and Hybrid Retrieval

A Graph Retrieval-Augmented Generation (GraphRAG) project that combines knowledge graphs and vector-based retrieval to answer questions about enterprise documents. It uses an LLM to extract entities and relationships, stores graph data in FalkorDB, and combines retrieval results to generate context-aware answers.

## Features

- PDF text extraction and cleaning
- Text chunking for document processing
- LLM-based entity and relationship extraction
- Knowledge graph construction and storage with FalkorDB
- Community detection
- Vector retrieval with ChromaDB
- Hybrid retrieval and Reciprocal Rank Fusion (RRF)
- Answer generation using Ollama

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

## Project Status

The PDF processing, graph extraction, graph storage, vector retrieval, graph retrieval, hybrid retrieval, and answer-generation components have been implemented and tested individually.

## Future Improvements

- Add a user-friendly interface
- Expose the pipeline through a FastAPI service
- Improve retrieval evaluation and answer-quality metrics
- Add support for additional document formats

## Learning Objectives

This project demonstrates how knowledge graphs can complement vector search, how relationships between entities can support retrieval, and how multiple retrieval strategies can be combined to improve question answering.
