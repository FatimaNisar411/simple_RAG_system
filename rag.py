from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from transformers import pipeline
import os

# Initialize embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Setup ChromaDB
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(
    name="rag_docs",
    embedding_function=SentenceTransformerEmbeddingFunction("all-MiniLM-L6-v2")
)

# Load HF model (use a small CPU-friendly model like flan-t5-base or tiny-gpt2)
generator = pipeline("text2text-generation", model="google/flan-t5-base")

# Flag to prevent loading again
_loaded = False

def load_documents():
    global _loaded
    if _loaded:
        return
    path = os.path.join("data", "context.txt")
    if not os.path.exists(path):
        print("⚠️ context.txt not found!")
        return
    with open(path, "r", encoding="utf-8") as f:
        content = f.read().split("\n\n")
    for i, chunk in enumerate(content):
        collection.add(documents=[chunk], ids=[f"doc_{i}"])
    _loaded = True

def answer_question(query: str) -> str:
    results = collection.query(query_texts=[query], n_results=2)
    retrieved_docs = "\n".join(results["documents"][0])

    # Construct the prompt
    prompt = f"Context:\n{retrieved_docs}\n\nQuestion: {query}\nAnswer:"

    # Use Hugging Face model to generate the answer
    response = generator(prompt, max_length=200, do_sample=True)[0]['generated_text']

    return f"📚 Based on context:\n{retrieved_docs}\n\n❓Answer: {response}"
