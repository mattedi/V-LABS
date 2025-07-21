# app/routers/embeddings.py
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List

router = APIRouter()

class Embedding(BaseModel):
    id: Optional[int]
    vetor: List[float]
    origem: Optional[str] = None

embeddings_db: List[Embedding] = []

@router.get("/embeddings/ping")
def ping():
    return {"mensagem": "Ping Embeddings"}

@router.get("/embeddings")
def listar():
    return embeddings_db

@router.post("/embeddings")
def criar(embedding: Embedding):
    embeddings_db.append(embedding)
    return embedding

@router.put("/embeddings/{embedding_id}")
def atualizar(embedding_id: int, embedding: Embedding):
    for i, e in enumerate(embeddings_db):
        if e.id == embedding_id:
            embeddings_db[i] = embedding
            return embedding
    return {"erro": "Embedding não encontrado"}

@router.delete("/embeddings/{embedding_id}")
def deletar(embedding_id: int):
    for i, e in enumerate(embeddings_db):
        if e.id == embedding_id:
            del embeddings_db[i]
            return {"mensagem": "Embedding deletado"}
    return {"erro": "Embedding não encontrado"}
