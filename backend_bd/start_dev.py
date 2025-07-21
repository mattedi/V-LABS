# start_dev.py

import sys
import os
from fastapi import FastAPI

# === CONFIGURAÇÃO DO PYTHONPATH ===
# Garante que o diretório 'backend' esteja no sys.path
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "backend"))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# === IMPORTAÇÃO DOS ROUTERS ===
from backend.app.routers import usuarios, avaliacoes, logs, embeddings, perguntas, respostas
from backend.app.routers.listar_perguntas import router as listar_perguntas_router


# === INSTÂNCIA DA APLICAÇÃO ===
app = FastAPI(
    title="Vibe Learning API",
    description="API para sistema de aprendizagem com embeddings e MongoDB",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# === REGISTRO DOS ROUTERS ===
app.include_router(usuarios.router, prefix="/api", tags=["usuarios"])
app.include_router(avaliacoes.router, prefix="/api", tags=["avaliacoes"])
app.include_router(logs.router, prefix="/api", tags=["logs"])
app.include_router(embeddings.router, prefix="/api", tags=["embeddings"])
app.include_router(perguntas.router, prefix="/api", tags=["perguntas"])
app.include_router(respostas.router, prefix="/api", tags=["respostas"])
app.include_router(listar_perguntas_router, prefix="/api", tags=["perguntas-lista"])

# === ENDPOINTS AUXILIARES ===
@app.get("/")
def root():
    return {
        "message": "Vibe Learning API - Rodando",
        "version": "1.0.0",
        "docs": "http://127.0.0.1:8000/docs"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "database": "MongoDB conectado",
        "services": [
            "embeddings", "perguntas", "respostas",
            "usuarios", "avaliacoes", "logs"
        ]
    }

@app.get("/debug/paths")
def debug_paths():
    return {
        "backend_path": backend_path,
        "sys_path_preview": sys.path[:3]
    }
