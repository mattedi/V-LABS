# backend_bd/start_dev.py

# backend_bd/start_dev.py

import os
import sys
import logging
from fastapi import FastAPI

# =============================================================================
# CONFIGURAÇÃO DO LOG
# =============================================================================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("startup")

# =============================================================================
# CONFIGURAÇÃO DO PYTHONPATH
# =============================================================================
current_dir = os.path.abspath(os.path.dirname(__file__))
app_path = os.path.join(current_dir, "backend_mq", "app")

if not os.path.isdir(app_path):
    logger.critical(f"Diretório 'app' não encontrado: {app_path}")
    raise FileNotFoundError(f"Caminho inválido para os routers: {app_path}")

if app_path not in sys.path:
    sys.path.insert(0, app_path)
    logger.info(f"'app_path' adicionado ao sys.path: {app_path}")

# =============================================================================
# IMPORTAÇÃO DOS ROUTERS
# =============================================================================
try:
    from router import (
        usuarios,
        avaliacoes,
        logs,
        embeddings,
        perguntas,
        respostas,
        interacoes,
    )
    from routers.listar_perguntas import router as listar_perguntas_router
    logger.info("Todos os routers importados com sucesso.")
except ImportError as e:
    logger.exception("Erro ao importar routers")
    raise ImportError("Falha ao importar os módulos de roteamento.") from e

# =============================================================================
# INSTÂNCIA DA APLICAÇÃO FASTAPI
# =============================================================================
app = FastAPI(
    title="Vibe Learning API",
    description="API para sistema de aprendizagem com MongoDB, Qdrant e FastAPI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# =============================================================================
# REGISTRO DOS ROUTERS
# =============================================================================
router_config = [
    (usuarios.router, "usuarios"),
    (avaliacoes.router, "avaliacoes"),
    (logs.router, "logs"),
    (embeddings.router, "embeddings"),
    (perguntas.router, "perguntas"),
    (respostas.router, "respostas"),
    (interacoes.router, "interacoes"),
    (listar_perguntas_router, "perguntas-lista"),
]

for router, tag in router_config:
    app.include_router(router, prefix="/api", tags=[tag])

# =============================================================================
# ENDPOINTS AUXILIARES
# =============================================================================
@app.get("/")
def root():
    return {
        "message": "Vibe Learning API - Rodando",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "database": "MongoDB conectado",
        "services": [tag for _, tag in router_config]
    }

@app.get("/debug/paths")
def debug_paths():
    return {
        "app_path": app_path,
        "sys_path_preview": sys.path[:3]
    }
