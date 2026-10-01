# Naive RAG 




| Component            | Technology                     | Purpose                             |
| -------------------- | ------------------------------ | ----------------------------------- |
| Programming Language | Python                         | Main development language           |
| Document Format      | PDF                            | Enterprise knowledge source         |
| PDF Processing       | PyMuPDF                        | Extract text from PDFs              |
| Text Processing      | Python                         | Clean extracted text                |
| Chunking             | LangChain                      | Split documents into chunks         |
| Chunking Strategy    | RecursiveCharacterTextSplitter | Create meaningful chunks            |
| Embedding Model      | `nomic-embed-text`             | Convert text into vectors           |
| Model Runtime        | Ollama                         | Run embedding model and LLM locally |
| Vector Database      | ChromaDB                       | Store and search embeddings         |
| Retrieval            | ChromaDB similarity search     | Retrieve relevant chunks            |
| Augmentation         | Python Prompt Template         | Combine question and context        |
| LLM                  | Llama 3.2                      | Generate the final answer           |
| Backend API          | FastAPI                        | Expose the RAG pipeline as an API   |
| Frontend             | Streamlit                      | Build the enterprise user interface |
| Environment          | Python `venv`                  | Isolate project dependencies        |
| Development          | VS Code                        | Project development                 |
| Version Control      | Git + GitHub                   | Source-code management              |

## 🔍 Why These Technologies?
### Python

Python is used for the complete RAG pipeline because it provides libraries for document processing, embeddings, vector databases, LLMs, APIs, and application development.

### PyMuPDF

PyMuPDF is used to extract text from PDF documents.
It also allows us to preserve useful document information such as page numbers.
      
      PDF
       ↓
      PyMuPDF
       ↓
      Extracted Text



### LangChain

LangChain is used mainly for:

- Document chunking
- Embedding integration
- Vector database integration
- LLM integration

The project will not hide the entire RAG pipeline behind a single LangChain chain.

The individual RAG stages will remain visible and understandable.

### RecursiveCharacterTextSplitter

Documents are divided into smaller chunks before embedding.

Initial configuration:

    chunk_size = 500
    chunk_overlap = 50

These values can be changed later during experimentation.

### nomic-embed-text

nomic-embed-text is used to convert:

    Document chunks → Vectors

and:

    User queries → Vectors

The same embedding model is used for both documents and queries.

### Ollama

Ollama is used as the local model runtime.

It will run:

    nomic-embed-text

for embeddings and:

    Llama 3.2

for answer generation.

This allows the project to run locally without depending on an external LLM API.

### ChromaDB

ChromaDB is used as the vector database.

It stores:

- Document chunks
- Embeddings
- Metadata

and performs similarity search when a user asks a question.

### Llama 3.2

Llama 3.2 is responsible for generating the final response.

It receives:

    User Question
    +
    Retrieved Context
    +
    Instructions

and generates the answer.

The LLM does not perform vector retrieval.

### FastAPI

FastAPI will expose the RAG pipeline as an API.

Example:

    POST /ask

The API receives a question and returns the generated response.

### Streamlit

Streamlit provides the user interface for interacting with the RAG application.

The user can:

1. Enter a question
2. Submit the question
3. View the generated answer
4. View retrieved source information
