from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title="V.A.L.E. Orchestrator",
    description="Local-first AI companion platform — orchestration layer",
    version="0.1.0"
)

@app.get("/")
def root():
    return {
        "status": "online",
        "system": "V.A.L.E. Orchestrator",
        "version": "0.1.0"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "postgres": os.getenv("POSTGRES_URL") is not None,
        "qdrant": os.getenv("QDRANT_URL") is not None
    }
