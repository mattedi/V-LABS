"""
Aplicação principal do backend_com.

Configura e inicializa o servidor FastAPI com todos os
roteadores, middlewares e configurações necessárias.
"""

import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from .config import get_settings, get_cors_config
from .routers import health_router, auth_router, users_router, educational_router
from .utils.logging import setup_logger, configure_structured_logging


# Configura logging estruturado
configure_structured_logging()
logger = setup_logger("main")

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
    
    settings = get_settings()
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
    settings = get_settings()
    
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
        
        ### Arquitetura:
        Este serviço atua como camada de comunicação entre o frontend e o backend_bd,
        orquestrando fluxos complexos e fornecendo uma API REST unificada.
        
        ### Autenticação:
        Utilize o endpoint `/auth/login` para obter um token Bearer que deve ser
        incluído no header `Authorization: Bearer <token>` nas requisições protegidas.
        """,
        contact={
            "name": "V-LABS Team",
            "email": "support@v-labs.edu.br",
        },
        license_info={
            "name": "MIT License",
            "url": "https://opensource.org/licenses/MIT",
        },
        lifespan=lifespan,
        # Configurações de documentação
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
    """
    Configura middlewares da aplicação.
    
    Args:
        app: Instância do FastAPI
    """
    settings = get_settings()
    
    # CORS Middleware
    cors_config = get_cors_config()
    app.add_middleware(
        CORSMiddleware,
        **cors_config
    )
    
    # Trusted Host Middleware (segurança)
    if not settings.debug:
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=["*.v-labs.edu.br", "localhost", "127.0.0.1"]
        )
    
    # Middleware de request logging
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        """Middleware para logging de requisições."""
        start_time = time.time()
        
        # Log da requisição
        logger.info(
            f"HTTP {request.method} {request.url.path}",
            extra={
                "method": request.method,
                "path": request.url.path,
                "query_params": str(request.query_params),
                "client_ip": request.client.host,
                "user_agent": request.headers.get("user-agent", ""),
                "content_length": request.headers.get("content-length", 0)
            }
        )
        
        # Processa requisição
        try:
            response = await call_next(request)
            duration_ms = (time.time() - start_time) * 1000
            
            # Log da resposta
            logger.info(
                f"HTTP {request.method} {request.url.path} -> {response.status_code}",
                extra={
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                    "duration_ms": round(duration_ms, 2),
                    "client_ip": request.client.host
                }
            )
            
            # Adiciona headers de performance
            response.headers["X-Process-Time"] = str(round(duration_ms, 2))
            response.headers["X-Request-ID"] = str(id(request))
            
            return response
            
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            
            logger.error(
                f"HTTP {request.method} {request.url.path} -> ERROR",
                extra={
                    "method": request.method,
                    "path": request.url.path,
                    "duration_ms": round(duration_ms, 2),
                    "error": str(e),
                    "client_ip": request.client.host
                },
                exc_info=e
            )
            
            raise


def setup_routers(app: FastAPI) -> None:
    """
    Configura e inclui todos os roteadores da aplicação.
    
    Args:
        app: Instância do FastAPI
    """
    # Health check (sem autenticação)
    app.include_router(health_router)
    
    # Autenticação (endpoints públicos e protegidos)
    app.include_router(auth_router)
    
    # Usuários (protegido)
    app.include_router(users_router)
    
    # Educacional (protegido)
    app.include_router(educational_router)
    
    logger.info("All routers configured successfully")


def setup_exception_handlers(app: FastAPI) -> None:
    """
    Configura handlers customizados para exceções.
    
    Args:
        app: Instância do FastAPI
    """
    
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """Handler para HTTPException."""
        logger.warning(
            f"HTTP exception: {exc.status_code} - {exc.detail}",
            extra={
                "status_code": exc.status_code,
                "detail": exc.detail,
                "path": request.url.path,
                "method": request.method
            }
        )
        
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": True,
                "message": exc.detail,
                "status_code": exc.status_code,
                "timestamp": time.time()
            }
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handler para erros de validação."""
        errors = []
        for error in exc.errors():
            errors.append({
                "field": " -> ".join(str(loc) for loc in error["loc"]),
                "message": error["msg"],
                "type": error["type"]
            })
        
        logger.warning(
            f"Validation error: {len(errors)} errors",
            extra={
                "errors": errors,
                "path": request.url.path,
                "method": request.method
            }
        )
        
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": True,
                "message": "Validation error",
                "errors": errors,
                "status_code": 422,
                "timestamp": time.time()
            }
        )
    
    @app.exception_handler(500)
    async def internal_server_error_handler(request: Request, exc: Exception):
        """Handler para erros internos."""
        logger.error(
            f"Internal server error: {str(exc)}",
            extra={
                "path": request.url.path,
                "method": request.method,
                "error_type": type(exc).__name__
            },
            exc_info=exc
        )
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": True,
                "message": "Internal server error",
                "status_code": 500,
                "timestamp": time.time()
            }
        )


# Cria instância da aplicação
app = create_app()


# Endpoint raiz
@app.get(
    "/",
    summary="API Root",
    description="Informações básicas da API",
    tags=["Root"]
)
async def root():
    """
    Endpoint raiz da API.
    
    Retorna informações básicas sobre a API e links úteis.
    
    Returns:
        dict: Informações da API
    """
    settings = get_settings()
    uptime_seconds = time.time() - app_start_time
    
    return {
        "service": settings.app_name,
        "version": settings.app_version,
        "status": "operational",
        "uptime_seconds": round(uptime_seconds, 2),
        "environment": settings.environment,
        "timestamp": time.time(),
        "endpoints": {
            "health": "/health",
            "docs": "/docs" if settings.debug else None,
            "auth": "/auth",
            "users": "/users",
            "educational": "/educational"
        },
        "support": {
            "email": "support@v-labs.edu.br",
            "documentation": "/docs" if settings.debug else None
        }
    }


# Endpoint para informações da aplicação
@app.get(
    "/info",
    summary="Application Info",
    description="Informações detalhadas da aplicação",
    tags=["Info"]
)
async def app_info():
    """
    Informações detalhadas da aplicação.
    
    Returns:
        dict: Informações técnicas da aplicação
    """
    settings = get_settings()
    
    return {
        "application": {
            "name": settings.app_name,
            "version": settings.app_version,
            "environment": settings.environment,
            "debug": settings.debug
        },
        "runtime": {
            "uptime_seconds": round(time.time() - app_start_time, 2),
            "start_time": app_start_time,
            "current_time": time.time()
        },
        "configuration": {
            "backend_bd_url": settings.backend_bd_url,
            "backend_bd_timeout": settings.backend_bd_timeout,
            "cors_origins": settings.cors_origins,
            "log_level": settings.log_level
        },
        "features": {
            "authentication": True,
            "user_management": True,
            "educational_content": True,
            "semantic_search": True,
            "health_monitoring": True
        }
    }


# Middleware para adicionar headers de segurança
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """Adiciona headers de segurança às respostas."""
    response = await call_next(request)
    
    # Headers de segurança básicos
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    
    # Content Security Policy básico
    if not get_settings().debug:
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' https:; "
            "connect-src 'self' https:; "
            "frame-ancestors 'none'"
        )
    
    return response


if __name__ == "__main__":
    """
    Execução direta da aplicação (desenvolvimento).
    """
    import uvicorn
    
    settings = get_settings()
    
    logger.info(
        f"Starting {settings.app_name} in development mode",
        extra={
            "host": settings.host,
            "port": settings.port,
            "debug": settings.debug,
            "environment": settings.environment
        }
    )
    
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
        access_log=True,
        server_header=False,  # Remove header Server por segurança
        date_header=False     # Remove header Date por performance
    )