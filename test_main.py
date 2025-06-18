from fastapi.testclient import TestClient
from main import app  

client = TestClient(app)

def test_ping():
    """Test if the /ping endpoint is working."""
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong"}

def test_ask_returns_answer():
    """Test the /ask endpoint with a basic question."""
    query = {"query": "What is Retrieval-Augmented Generation?"}
    response = client.post("/ask", json=query)
    assert response.status_code == 200
    assert "answer" in response.json()
    answer = response.json()["answer"].lower()
    assert "context" in answer or "retrieval" in answer
