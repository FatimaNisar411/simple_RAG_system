
from fastapi import FastAPI
from pydantic import BaseModel
from rag import answer_question, load_documents
app = FastAPI()

# Load context on startup
@app.on_event("startup")
def startup_event():
    load_documents()

class Question(BaseModel):
    query: str

@app.post("/ask")
def ask(question: Question):
    response = answer_question(question.query)
    return {"answer": response}
