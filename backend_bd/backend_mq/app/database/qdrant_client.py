import os
import logging
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import UnexpectedResponse
from qdrant_client.http.models import PointStruct, VectorParams, Distance

# =============================================================================
# Configuração
# =============================================================================

load_dotenv()

# Logging
logger = logging.getLogger("qdrant")
logging.basicConfig(level=logging.INFO)

# Variáveis de ambiente
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION = "interacoes"
VECTOR_SIZE = 384  # compatível com all-MiniLM-L6-v2

if not QDRANT_URL or not QDRANT_API_KEY:
    raise ValueError("QDRANT_URL e QDRANT_API_KEY são obrigatórias.")

# Inicialização do cliente
try:
    qdrant = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    logger.info("Cliente Qdrant inicializado com sucesso.")
except Exception as e:
    logger.error(f"Erro ao conectar com Qdrant: {e}")
    raise

# =============================================================================
# Verificação da coleção (executar sob demanda no main)
# =============================================================================

def garantir_colecao():
    """
    Garante que a coleção 'interacoes' esteja criada no Qdrant.
    Deve ser chamada no início da aplicação (ex: em main.py).
    """
    try:
        colecoes = qdrant.get_collections().collections
        nomes_colecoes = [c.name for c in colecoes]

        if QDRANT_COLLECTION not in nomes_colecoes:
            qdrant.recreate_collection(
                collection_name=QDRANT_COLLECTION,
                vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE)
            )
            logger.info(f"Coleção '{QDRANT_COLLECTION}' criada.")
        else:
            logger.info(f"Coleção '{QDRANT_COLLECTION}' já existe.")
    except Exception as e:
        logger.error(f"Erro ao verificar/criar coleção '{QDRANT_COLLECTION}': {e}")
        raise

# =============================================================================
# Funções de indexação e busca
# =============================================================================

def indexar_documento(collection_name: str, doc_id: str, vetor: list[float], payload: dict):
    """
    Indexa um documento (ponto) na coleção Qdrant especificada.
    """
    try:
        qdrant.upsert(
            collection_name=collection_name,
            points=[PointStruct(id=doc_id, vector=vetor, payload=payload)]
        )
        logger.info(f"Documento {doc_id} indexado na coleção {collection_name}.")
    except UnexpectedResponse as e:
        logger.error(f"Erro na resposta do Qdrant: {e}")
        raise
    except Exception as e:
        logger.error(f"Erro inesperado ao indexar documento {doc_id}: {e}")
        raise

def buscar_por_texto(collection_name: str, vetor: list[float], limit: int = 5):
    """
    Realiza busca por similaridade com base em vetor na coleção especificada.
    """
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
