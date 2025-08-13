# Database connections - versão funcional para produção
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# Configurações do MongoDB
MONGO_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGODB_DATABASE", "vlabs_prod")

try:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    
    # Testar conexão
    client.admin.command('ping')
    print(f"✅ MongoDB conectado (produção): {db.name}")
    
    # Coleções principais
    colecao_usuarios = db.usuarios
    colecao_perguntas = db.perguntas
    colecao_respostas = db.respostas
    colecao_avaliacoes = db.avaliacoes
    colecao_logs = db.logs
    colecao_embeddings = db.embeddings
    colecao_interacoes = db.interacoes
    colecao_alunos = db.alunos
    colecao_sessoes = db.sessoes
    colecao_configuracoes = db.configuracoes
    colecao_modos_entrada = db.modos_entrada
    colecao_logs_interacao = db.logs_interacao
    
    # Verificar coleções existentes
    collections = db.list_collection_names()
    print(f"Coleções disponíveis: {collections}")
    
except Exception as e:
    print(f"❌ Erro ao conectar MongoDB (produção): {e}")
    # Fallback - variáveis None para evitar erros
    db = None
    colecao_usuarios = None
    colecao_perguntas = None
    colecao_respostas = None
    colecao_avaliacoes = None
    colecao_logs = None
    colecao_embeddings = None
    colecao_interacoes = None
    colecao_alunos = None
    colecao_sessoes = None
    colecao_configuracoes = None
    colecao_modos_entrada = None
    colecao_logs_interacao = None

# === Compatibilidade com routers ===
from typing import Optional, Dict, Any, List

# Coleção de conversas (segue o padrão das demais coleções no módulo)
try:
    colecao_conversas = db.conversas
except Exception:
    colecao_conversas = None

def salvar_interacao(dados: Dict[str, Any]):
    """
    Insere uma interação na coleção 'interacoes' e retorna o ObjectId inserido.
    """
    if db is None:
        raise RuntimeError("MongoDB não inicializado")
    res = db.interacoes.insert_one(dados)
    return res.inserted_id

def obter_interacoes(filtro: Optional[Dict[str, Any]] = None, limite: int = 100) -> List[Dict[str, Any]]:
    """
    Retorna lista de interações de acordo com o filtro (opcional).
    """
    if db is None:
        raise RuntimeError("MongoDB não inicializado")
    filtro = filtro or {}
    cur = db.interacoes.find(filtro).limit(limite)
    return list(cur)
