from fastapi import FastAPI
from pydantic import BaseModel

from app.rag_pipeline import ask_question


app = FastAPI(
    title="Naive RAG API",
    description="Enterprise document question-answering API",
    version="1.0.0"
)


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return {
        "message": "Naive RAG API is running"
    }


@app.post("/ask")
def ask(request: QuestionRequest):

    answer = ask_question(request.question)

    return {
        "question": request.question,
        "answer": answer
    }