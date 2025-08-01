# backend/app/services/embedding_service.py

# app/services/embedding_service.py

from sentence_transformers import SentenceTransformer

modelo = SentenceTransformer("all-MiniLM-L6-v2")

def gerar_vetor(texto: str) -> list[float]:
    vetor = modelo.encode(texto)
    return vetor.tolist()
