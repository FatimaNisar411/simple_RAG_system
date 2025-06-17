
# from fastapi import FastAPI
# from pydantic import BaseModel
# from rag import answer_question, load_documents
# app = FastAPI()

# # Load context on startup
# @app.on_event("startup")
# def startup_event():
#     load_documents()

# class Question(BaseModel):
#     query: str

# @app.post("/ask")
# def ask(question: Question):
#     response = answer_question(question.query)
#     return {"answer": response}

# @app.get("/ping")
# def ping():
#     return {"message": "pong"}
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag import answer_question, load_documents
from prometheus_client import start_http_server, Summary, Counter
import time

app = FastAPI()

# --- Prometheus metrics ---
REQUEST_TIME = Summary("request_processing_seconds", "Time spent processing request")
REQUEST_COUNT = Counter("requests_total", "Total number of /ask requests")
ERROR_COUNT = Counter("model_errors_total", "Total number of model inference errors")

# --- Load context and start Prometheus on startup ---
@app.on_event("startup")
def startup_event():
    load_documents()
    start_http_server(8001)  # Prometheus scrapes this port

class Question(BaseModel):
    query: str

# --- /ask endpoint with metrics ---
@app.post("/ask")
@REQUEST_TIME.time()
def ask(question: Question):
    REQUEST_COUNT.inc()
    try:
        response = answer_question(question.query)
        return {"answer": response}
    except Exception as e:
        ERROR_COUNT.inc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ping")
def ping():
    return {"message": "pong"}
