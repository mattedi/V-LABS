import os
import logging
from typing import List, Dict
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv

# =============================================================================
# Configuração e Inicialização
# =============================================================================

load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mongo")

# Variáveis de ambiente obrigatórias
MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "vibe_learning")

if not MONGODB_URI:
    raise ValueError("Variável de ambiente 'MONGODB_URI' não foi definida.")

try:
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    client.admin.command("ping")  # Testar conexão
    db = client[MONGODB_DATABASE]
    logger.info("Conexão com MongoDB estabelecida com sucesso.")
except ConnectionFailure as e:
    logger.error(f"Falha na conexão com o MongoDB: {e}")
    raise
except Exception as e:
    logger.error(f"Erro inesperado ao conectar com MongoDB: {e}")
    raise

# =============================================================================
# Coleções
# =============================================================================

colecao_usuarios: Collection = db["usuarios"]
colecao_perguntas: Collection = db["perguntas"]
colecao_respostas: Collection = db["respostas"]
colecao_avaliacoes: Collection = db["avaliacoes"]
colecao_logs: Collection = db["logs"]
colecao_interacoes: Collection = db["interacoes"]

# =============================================================================
# Funções utilitárias
# =============================================================================

def salvar_interacao(interacao: Dict) -> str:
    """
    Insere uma nova interação na coleção `interacoes`.
    
    :param interacao: Dicionário representando a interação.
    :return: ID da interação inserida como string.
    """
    try:
        result = colecao_interacoes.insert_one(interacao)
        logger.info(f"Interação salva com ID {result.inserted_id}")
        return str(result.inserted_id)
    except Exception as e:
        logger.error(f"Erro ao salvar interação: {e}")
        raise

def buscar_historico_por_usuario(user_id: str) -> List[Dict]:
    """
    Retorna todas as interações de um usuário específico.
    
    :param user_id: ID do usuário
    :return: Lista de dicionários com as interações
    """
    try:
        interacoes = list(colecao_interacoes.find({"user_id": user_id}))
        for item in interacoes:
            item["_id"] = str(item["_id"])
        logger.info(f"{len(interacoes)} interações encontradas para user_id={user_id}")
        return interacoes
    except Exception as e:
        logger.error(f"Erro ao buscar interações do usuário {user_id}: {e}")
        raise
