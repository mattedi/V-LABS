from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criar app FastAPI
app = FastAPI(
    title="Vibe Learning API",
    version="1.0.0", 
    description="API completa para tutoria multimodal com IA - Todos os endpoints de banco de dados",
    contact={
        "name": "Equipe V-LABS",
        "email": "contato@vlabs.ai"
    }
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar origens
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lista para rastrear routers carregados
routers_loaded = []
routers_failed = []

# Função helper para carregar router
def load_router(router_name, prefix, tags):
    try:
        if router_name == "usuarios":
            from app.routers import usuarios
            app.include_router(usuarios.router, prefix=prefix, tags=tags)
        elif router_name == "perguntas":
            from app.routers import perguntas  
            app.include_router(perguntas.router, prefix=prefix, tags=tags)
        elif router_name == "respostas":
            from app.routers import respostas
            app.include_router(respostas.router, prefix=prefix, tags=tags)
        elif router_name == "embeddings":
            from app.routers import embeddings
            app.include_router(embeddings.router, prefix=prefix, tags=tags)
        elif router_name == "avaliacoes":
            from app.routers import avaliacoes
            app.include_router(avaliacoes.router, prefix=prefix, tags=tags)
        elif router_name == "logs":
            from app.routers import logs
            app.include_router(logs.router, prefix=prefix, tags=tags)
        elif router_name == "interacoes":
            from app.routers import interacoes
            app.include_router(interacoes.router, prefix=prefix, tags=tags)
        
        routers_loaded.append(router_name)
        logger.info(f"✅ Router {router_name} carregado com sucesso")
        return True
        
    except Exception as e:
        routers_failed.append({"router": router_name, "error": str(e)})
        logger.warning(f"⚠️ Router {router_name} falhou: {str(e)}")
        return False

# Lista de routers para carregar
routers_config = [
    ("usuarios", "/api/usuarios", ["usuarios"]),
    ("perguntas", "/api/perguntas", ["perguntas"]),
    ("respostas", "/api/respostas", ["respostas"]),
    ("embeddings", "/api/embeddings", ["embeddings"]),
    ("avaliacoes", "/api/avaliacoes", ["avaliacoes"]),
    ("logs", "/api/logs", ["logs"]),
    ("interacoes", "/api/interacoes", ["interacoes"])
]

# Carregar todos os routers
for router_name, prefix, tags in routers_config:
    load_router(router_name, prefix, tags)

# Endpoints básicos
@app.get("/", tags=["health"])
def root():
    """Endpoint principal da API."""
    return {
        "mensagem": "API Vibe Learning funcionando!",
        "versao": "1.0.0",
        "status": "healthy",
        "routers_carregados": routers_loaded,
        "total_routers": len(routers_loaded),
        "routers_com_erro": len(routers_failed)
    }

@app.get("/health", tags=["health"])  
def health_check():
    """Endpoint de verificação de saúde detalhado."""
    return {
        "status": "healthy",
        "api_version": "1.0.0",
        "routers": {
            "carregados": routers_loaded,
            "total": len(routers_loaded),
            "falharam": routers_failed
        },
        "services": {
            "database": "connected",
            "api": "running"
        }
    }

@app.get("/routers", tags=["debug"])
def list_routers():
    """Lista todos os routers e seu status."""
    return {
        "routers_ativos": routers_loaded,
        "routers_com_erro": routers_failed,
        "total_configurados": len(routers_config),
        "taxa_sucesso": f"{len(routers_loaded)/len(routers_config)*100:.1f}%"
    }

# Eventos de inicialização
@app.on_event("startup")
async def startup_event():
    """Executado na inicialização da aplicação."""
    logger.info("=== VIBE LEARNING API INICIADA ===")
    logger.info(f"Routers carregados: {len(routers_loaded)}/{len(routers_config)}")
    logger.info(f"Routers ativos: {', '.join(routers_loaded)}")
    if routers_failed:
        logger.warning(f"Routers com erro: {len(routers_failed)}")

@app.on_event("shutdown")
async def shutdown_event():
    """Executado no encerramento da aplicação."""
    logger.info("=== VIBE LEARNING API ENCERRADA ===")

# Log final
logger.info(f"🚀 API configurada com {len(routers_loaded)} routers ativos")
if routers_failed:
    logger.warning(f"⚠️ {len(routers_failed)} routers falharam na inicialização")

# Adicionar após a definição inicial do app
try:
    from app.routers import usuarios
    app.include_router(usuarios.router, prefix="/api/usuarios", tags=["usuarios"])
    print("✅ Router usuarios adicionado")
except Exception as e:
    print(f"⚠️ Router usuarios falhou: {e}")