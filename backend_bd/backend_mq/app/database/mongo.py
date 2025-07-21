import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Validar variáveis obrigatórias
MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "vibe_learning")

if not MONGODB_URI:
    raise ValueError("MONGODB_URI não encontrada nas variáveis de ambiente")

try:
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    # Testar conexão
    client.admin.command('ping')
    logger.info("Conexão com MongoDB estabelecida com sucesso")
    
    db = client[MONGODB_DATABASE]
    
    # Coleções
    colecao_usuarios = db["usuarios"]
    colecao_perguntas = db["perguntas"]
    colecao_respostas = db["respostas"]
    colecao_avaliacoes = db["avaliacoes"]
    colecao_logs = db["logs"]
    
except ConnectionFailure as e:
    logger.error(f"Falha na conexão com MongoDB: {e}")
    raise
except Exception as e:
    logger.error(f"Erro inesperado na conexão MongoDB: {e}")
    raise