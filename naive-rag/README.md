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



### Commands to run the project 
Terminal 1:

      venv\Scripts\activate
      python -m uvicorn api.main:app --reload

Terminal 2:

      venv\Scripts\activate
      python -m streamlit run frontend/app.py

## List of Questions
1. What are the company's working hours?
2. How many annual leave days do employees get?
3. How many paid sick leave days do employees get?
4. How much is the annual learning allowance?
5.  Within how many days must travel expense claims be submitted?
   
### working hours
6. What days do employees work?
7. What time does the workday start?
8. What time does the workday end?
9. How long is the lunch break?
10. When is the lunch break?

### Leave
11. How many days of sick leave are provided?
12. How many annual leave days are provided per year?
13. How many paid leaves do employees receive?
14. What is the company's maternity leave policy?

### Learning & benefits
15. What is the employee learning allowance?
16. What can the learning allowance be used for?
17. Who is eligible for the learning allowance?
18. How much does the company provide for learning and development?

### Travel & expenses
19. How long do employees have to submit travel expense claims?
20. When should travel expense claims be submitted?
21. What is the deadline for submitting business travel expenses?
22. How many calendar days are allowed for travel claims?

### Remote work
23. What is the company's remote work policy?
24. Are employees allowed to work remotely?
25. What are the rules for remote work?

### Security
26. What are the company's security policies?
27. What security practices are employees expected to follow?
28. What should employees do to protect company information?

### Code of conduct
29. What is the company's code of conduct?
30. What behavior is expected from employees?
31. What are the workplace conduct guidelines?
