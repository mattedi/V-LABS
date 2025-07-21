import os
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct
from qdrant_client.http.exceptions import UnexpectedResponse
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)
load_dotenv()

# Validar variáveis obrigatórias
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

if not QDRANT_URL or not QDRANT_API_KEY:
    raise ValueError("QDRANT_URL e QDRANT_API_KEY são obrigatórias")

try:
    qdrant = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    logger.info("Cliente Qdrant inicializado com sucesso")
except Exception as e:
    logger.error(f"Erro ao conectar com Qdrant: {e}")
    raise

def indexar_documento(collection_name: str, doc_id: str, vetor: list[float], payload: dict):
    """Função unificada para indexar documentos no Qdrant"""
    try:
        qdrant.upsert(
            collection_name=collection_name,
            points=[PointStruct(id=str(doc_id), vector=vetor, payload=payload)]
        )
        logger.info(f"Documento {doc_id} indexado na coleção {collection_name}")
    except UnexpectedResponse as e:
        logger.error(f"Erro ao indexar documento {doc_id}: {e}")
        raise
    except Exception as e:
        logger.error(f"Erro inesperado ao indexar: {e}")
        raise

def buscar_por_texto(collection_name: str, vetor: list[float], limit: int = 5):
    """Busca por similaridade usando vetor já processado"""
    try:
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
    except Exception as e:
        logger.error(f"Erro na busca por similaridade: {e}")
        return []