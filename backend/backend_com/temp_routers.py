"""
Aplicação principal do backend_com - VERSÃO CORRIGIDA

Configura e inicializa o servidor FastAPI com todos os
roteadores, middlewares e configurações necessárias.
"""

import time
import sys
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

# Adiciona o diretório atual ao Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Imports absolutos - SEM pontos
import backend_com.config as config
from backend.backend_com import routers
import utils

# Configura logging estruturado
utils.configure_structured_logging()
logger = utils.setup_logger("main")

# Tempo de inicialização para cálculo de uptime
app_start_time = time.time()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia ciclo de vida da aplicação.
    
    Executa operações de inicialização e limpeza.
    """
    # Startup
    logger.info("Starting V-LABS Backend Communication service...")
    
    settings = config.get_settings()
    logger.info(
        f"Application initialized: {settings.app_name} v{settings.app_version}",
        extra={
            "environment": settings.environment,
            "debug": settings.debug,
            "backend_bd_url": settings.backend_bd_url
        }
    )
    
    yield
    
    # Shutdown
    logger.info("Shutting down V-LABS Backend Communication service...")


# Cria aplicação FastAPI
def create_app() -> FastAPI:
    """
    Factory function para criar e configurar a aplicação FastAPI.
    
    Returns:
        FastAPI: Aplicação configurada
    """
    settings = config.get_settings()
    
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="""
        ## V-LABS Backend Communication API
        
        API de comunicação do sistema educacional V-LABS.
        
        ### Funcionalidades Principais:
        - **Autenticação**: Login, registro e gerenciamento de sessões
        - **Usuários**: CRUD de usuários e configurações de perfil
        - **Educacional**: Perguntas, respostas, avaliações e busca semântica
        - **Health Check**: Monitoramento de saúde do sistema
        """,
        lifespan=lifespan,
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
        openapi_url="/openapi.json" if settings.debug else None,
    )
    
    # Adiciona middlewares
    setup_middlewares(app)
    
    # Adiciona roteadores
    setup_routers(app)
    
    # Adiciona handlers de exceção
    setup_exception_handlers(app)
    
    return app


def setup_middlewares(app: FastAPI) -> None:
    """Configura middlewares da aplicação."""
    settings = config.get_settings()
    cors_config = config.get_cors_config()
    
    # CORS Middleware
    app.add_middleware(CORSMiddleware, **cors_config)
    
    # Request logging middleware
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        duration_ms = (time.time() - start_time) * 1000
        
        logger.info(
            f"HTTP {request.method} {request.url.path} -> {response.status_code}",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": round(duration_ms, 2)
            }
        )
        
        response.headers["X-Process-Time"] = str(round(duration_ms, 2))
        return response


def setup_routers(app: FastAPI) -> None:
    """Configura e inclui todos os roteadores da aplicação."""
    app.include_router(routers.health_router)
    app.include_router(routers.auth_router)
    app.include_router(routers.users_router)
    app.include_router(routers.educational_router)
    
    logger.info("All routers configured successfully")


def setup_exception_handlers(app: FastAPI) -> None:
    """Configura handlers customizados para exceções."""
    
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": True,
                "message": exc.detail,
                "status_code": exc.status_code,
                "timestamp": time.time()
            }
        )


# Cria instância da aplicação
app = create_app()


# Endpoint raiz
@app.get("/")
async def root():
    """Endpoint raiz da API."""
    settings = config.get_settings()
    uptime_seconds = time.time() - app_start_time
    
    return {
        "service": settings.app_name,
        "version": settings.app_version,
        "status": "operational",
        "uptime_seconds": round(uptime_seconds, 2),
        "environment": settings.environment,
        "endpoints": {
            "health": "/health",
            "docs": "/docs" if settings.debug else None,
            "auth": "/auth",
            "users": "/users",
            "educational": "/educational"
        }
    }


if __name__ == "__main__":
    import uvicorn
    
    settings = config.get_settings()
    
    logger.info(f"Starting {settings.app_name} in development mode")
    
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )