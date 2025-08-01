# backend/app/services/qdrant_service.py

from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance, Payload
from uuid import uuid4

qdrant = QdrantClient(host="localhost", port=6333)  # Ajuste conforme seu ambiente
COLLECTION_NAME = "perguntas_vibe"

def inicializar_colecao():
    if COLLECTION_NAME not in [c.name for c in qdrant.get_collections().collections]:
        qdrant.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )

def salvar_no_qdrant(user_id: str, texto: str, resposta: str, vetor: list[float], timestamp: str):
    ponto = PointStruct(
        id=str(uuid4()),
        vector=vetor,
        payload={
            "user_id": user_id,
            "texto": texto,
            "resposta": resposta,
            "timestamp": timestamp
        }
    )
    qdrant.upsert(collection_name=COLLECTION_NAME, points=[ponto])
