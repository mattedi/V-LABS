from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct
import os

qdrant = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

def indexar_pergunta(id: str, vetor: list[float], payload: dict):
    qdrant.upsert(
        collection_name="perguntas",
        points=[PointStruct(id=str(id), vector=vetor, payload=payload)]
    )

def indexar_resposta(id: str, vetor: list[float], payload: dict):
    qdrant.upsert(
        collection_name="respostas",
        points=[PointStruct(id=str(id), vector=vetor, payload=payload)]
    )

def buscar_por_texto(collection_name: str, texto: str, limit: int = 5):
    from app.services.embedding_service import gerar_vetor
    vetor = gerar_vetor(texto)
    resultados = qdrant.search(
        collection_name=collection_name,
        query_vector=vetor,
        limit=limit,
        with_payload=True
    )
    return [
        {
            "id": r.id,
            "score": r.score,
            "texto": r.payload.get("texto"),
            "categoria": r.payload.get("categoria")
        }
        for r in resultados
    ]
