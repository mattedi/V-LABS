"""
Aplicação principal do backend_com - VERSÃO REFATORADA E COMPLETA

Configura e inicializa o servidor FastAPI com todos os
roteadores, middlewares e configurações necessárias.

Inclui integração com backend_bd e monitoramento completo do sistema.
"""

import time
import sys
import os
from contextlib import asynccontextmanager
from typing import Dict, Any, Optional

# FastAPI imports
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from config import settings


# HTTP client for backend_bd integration
import httpx

# Adiciona o diretório atual ao Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Imports absolutos - SEM pontos
import config
import routers
from utils import setup_logger, configure_structured_logging

# ===============================================
# CONFIGURAÇÃO GLOBAL
# ===============================================

# Configura logging estruturado
configure_structured_logging()
logger = setup_logger("main")

# Tempo de inicialização para cálculo de uptime
app_start_time = time.time()

# Cliente HTTP global para comunicação com backend_bd
http_client = httpx.AsyncClient()


# =============================================== 
# CICLO DE VIDA DA APLICAÇÃO
# ===============================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia ciclo de vida da aplicação.
    
    Executa operações de inicialização e limpeza.
    """
    # === STARTUP ===
    logger.info("🚀 Starting V-LABS Backend Communication service...")
    
    settings = config.get_settings()
    logger.info(
        f"✅ Application initialized: {settings.app_name} v{settings.app_version}",
        extra={
            "environment": settings.environment,
            "debug": settings.debug,
            "backend_bd_url": settings.backend_bd_url,
            "host": settings.host,
            "port": settings.port
        }
    )
    
    # Testa conectividade com backend_bd
    await test_backend_bd_connectivity()
    
    yield
    
    # === SHUTDOWN ===
    logger.info("🛑 Shutting down V-LABS Backend Communication service...")
    
    # Fecha cliente HTTP
    await http_client.aclose()


async def test_backend_bd_connectivity():
    """Testa conectividade inicial com backend_bd."""
    settings = config.get_settings()
    
    try:
        response = await http_client.get(
            f"{settings.backend_bd_url}/health",
            timeout=5.0
        )
        
        if response.status_code == 200:
            logger.info("✅ Backend_BD connectivity: OK")
        else:
            logger.warning(f"⚠️ Backend_BD returned status: {response.status_code}")
            
    except Exception as e:
        logger.error(f"❌ Backend_BD connectivity failed: {str(e)}")


# ===============================================
# FACTORY FUNCTION DA APLICAÇÃO
# ===============================================

def create_app() -> FastAPI:
    """
    Factory function para criar e configurar a aplicação FastAPI.
    
    Returns:
        FastAPI: Aplicação configurada
    """
    settings = config.get_settings()
    
    # Cria aplicação FastAPI
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="""
        ## 🎓 V-LABS Backend Communication API
        
        **Camada de comunicação do sistema educacional V-LABS.**
        
        ### 🏗️ Arquitetura:
        ```
        Frontend ↔️ Backend_COM ↔️ Backend_BD ↔️ Database
        ```
        
        ### 🚀 Funcionalidades Principais:
        - **🔐 Autenticação**: Login, registro e gerenciamento de sessões
        - **👥 Usuários**: CRUD de usuários e configurações de perfil  
        - **📚 Educacional**: Perguntas, respostas, avaliações e busca semântica
        - **🏥 Health Check**: Monitoramento de saúde do sistema
        - **🔗 Integração**: Orquestração com backend_bd
        
        ### 🔑 Autenticação:
        Utilize o endpoint `/auth/login` para obter um token Bearer que deve ser
        incluído no header `Authorization: Bearer <token>` nas requisições protegidas.
        
        ### 📊 Monitoramento:
        - `/health`: Status básico do serviço
        - `/system/status`: Status completo do sistema
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
    
    # Configura componentes da aplicação
    setup_middlewares(app)
    setup_routers(app)
    setup_exception_handlers(app)
    
    logger.info("🔧 FastAPI application configured successfully")
    
    return app


# ===============================================
# CONFIGURAÇÃO DE MIDDLEWARES
# ===============================================

def setup_middlewares(app: FastAPI) -> None:
    """Configura middlewares da aplicação."""
    settings = config.get_settings()
    cors_config = config.get_cors_config()
    
    # CORS Middleware
    app.add_middleware(CORSMiddleware, **cors_config)
    logger.info("✅ CORS middleware configured")
    
    # Trusted Host Middleware (apenas em produção)
    if not settings.debug:
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=["*.v-labs.edu.br", "localhost", "127.0.0.1"]
        )
        logger.info("✅ TrustedHost middleware configured")
    
    # Request logging middleware
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        """Middleware para logging detalhado de requisições."""
        start_time = time.time()
        
        # Log da requisição
        logger.info(
            f"🌐 {request.method} {request.url.path}",
            extra={
                "method": request.method,
                "path": request.url.path,
                "query_params": str(request.query_params) if request.query_params else None,
                "client_ip": getattr(request.client, 'host', 'unknown'),
                "user_agent": request.headers.get("user-agent", "unknown")[:100]  # Limita tamanho
            }
        )
        
        try:
            response = await call_next(request)
            duration_ms = (time.time() - start_time) * 1000
            
            # Log da resposta
            log_level = "info"
            if response.status_code >= 500:
                log_level = "error"
            elif response.status_code >= 400:
                log_level = "warning"
            
            getattr(logger, log_level)(
                f"📤 {request.method} {request.url.path} → {response.status_code} ({duration_ms:.2f}ms)",
                extra={
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                    "duration_ms": round(duration_ms, 2),
                    "client_ip": getattr(request.client, 'host', 'unknown')
                }
            )
            
            # Headers de performance
            response.headers["X-Process-Time"] = str(round(duration_ms, 2))
            response.headers["X-Request-ID"] = str(id(request))
            response.headers["X-Service"] = "V-LABS-Backend-COM" 
            
            return response
            
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            
            logger.error(
                f"💥 {request.method} {request.url.path} → ERROR ({duration_ms:.2f}ms): {str(e)}",
                extra={
                    "method": request.method,
                    "path": request.url.path,
                    "duration_ms": round(duration_ms, 2),
                    "error": str(e),
                    "client_ip": getattr(request.client, 'host', 'unknown')
                },
                exc_info=True
            )
            
            raise


# ===============================================
# CONFIGURAÇÃO DE ROTEADORES
# ===============================================

def setup_routers(app: FastAPI) -> None:
    """Configura e inclui todos os roteadores da aplicação."""
    
    # Inclui roteadores na ordem de importância
    routers_config = [
        (routers.health_router, "Health Check"),
        (routers.auth_router, "Authentication"),
        (routers.users_router, "Users Management"),
        (routers.educational_router, "Educational Content")
    ]
    
    for router, description in routers_config:
        app.include_router(router)
        logger.info(f"✅ {description} router configured")
    
    logger.info("🔗 All routers configured successfully")


# ===============================================
# HANDLERS DE EXCEÇÃO
# ===============================================

def setup_exception_handlers(app: FastAPI) -> None:
    """Configura handlers customizados para exceções."""
    
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """Handler para HTTPException."""
        logger.warning(
            f"🚨 HTTP Exception: {exc.status_code} - {exc.detail}",
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
                "timestamp": time.time(),
                "path": request.url.path
            }
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handler para erros de validação."""
        errors = []
        for error in exc.errors():
            errors.append({
                "field": " → ".join(str(loc) for loc in error["loc"]),
                "message": error["msg"],
                "type": error["type"],
                "input": error.get("input")
            })
        
        logger.warning(
            f"📋 Validation Error: {len(errors)} error(s)",
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
                "timestamp": time.time(),
                "path": request.url.path
            }
        )
    
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        """Handler global para exceções não tratadas."""
        logger.error(
            f"💥 Unhandled Exception: {type(exc).__name__}: {str(exc)}",
            extra={
                "path": request.url.path,
                "method": request.method,
                "error_type": type(exc).__name__,
                "error_message": str(exc)
            },
            exc_info=True
        )
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": True,
                "message": "Internal server error",
                "error_type": type(exc).__name__,
                "status_code": 500,
                "timestamp": time.time(),
                "path": request.url.path
            }
        )
    
    logger.info("⚡ Exception handlers configured")


# ===============================================
# UTILITÁRIOS DE INTEGRAÇÃO
# ===============================================

async def check_backend_bd_health() -> Dict[str, Any]:
    """Verifica saúde do backend_bd."""
    settings = config.get_settings()
    
    try:
        response = await http_client.get(
            f"{settings.backend_bd_url}/health",
            timeout=settings.backend_bd_timeout
        )
        
        if response.status_code == 200:
            return {
                "status": "healthy",
                "response_time_ms": response.elapsed.total_seconds() * 1000,
                "data": response.json()
            }
        else:
            return {
                "status": "unhealthy",
                "status_code": response.status_code,
                "message": f"Backend_BD returned {response.status_code}"
            }
            
    except httpx.TimeoutException:
        return {
            "status": "timeout",
            "message": f"Backend_BD timeout after {settings.backend_bd_timeout}s"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Backend_BD connection failed: {str(e)}"
        }


# ===============================================
# INSTÂNCIA DA APLICAÇÃO
# ===============================================

# Cria instância da aplicação
app = create_app()


# ===============================================
# ENDPOINTS PRINCIPAIS
# ===============================================

@app.get(
    "/",
    summary="🏠 API Root",
    description="Informações básicas da API e pontos de entrada",
    tags=["Root"]
)
async def root():
    """
    Endpoint raiz da API V-LABS Backend Communication.
    
    Retorna informações básicas sobre a API, status e links úteis.
    """
    settings = config.get_settings()
    uptime_seconds = time.time() - app_start_time
    
    return {
        "service": settings.app_name,
        "version": settings.app_version,
        "status": "operational",
        "uptime_seconds": round(uptime_seconds, 2),
        "environment": settings.environment,
        "timestamp": time.time(),
        "description": "V-LABS Backend Communication - Camada de orquestração do sistema educacional",
        "endpoints": {
            "health": "/health - Health check básico",
            "system_status": "/system/status - Status completo do sistema",
            "docs": "/docs - Documentação interativa" if settings.debug else None,
            "auth": "/auth - Endpoints de autenticação",
            "users": "/users - Gerenciamento de usuários",
            "educational": "/educational - Conteúdo educacional"
        },
        "support": {
            "email": "support@v-labs.edu.br",
            "documentation": "/docs" if settings.debug else None
        },
        "architecture": {
            "layer": "Communication Layer",
            "integrates_with": ["Frontend", "Backend_BD"],
            "database_direct": False
        }
    }


@app.get(
    "/system/status",
    summary="🔍 System Status",
    description="Status completo do sistema V-LABS com teste de integração",
    tags=["System"]
)
async def system_status():
    """
    Status completo do sistema V-LABS.
    
    Verifica conectividade e saúde de todos os componentes:
    - Backend_COM (este serviço)
    - Backend_BD (persistência)
    - Frontend (quando disponível)
    
    Returns:
        dict: Status detalhado de todos os componentes
    """
    settings = config.get_settings()
    current_time = time.time()
    uptime = round(current_time - app_start_time, 2)
    
    # Testa backend_bd
    bd_health = await check_backend_bd_health()
    
    # Determina status geral do sistema
    system_healthy = bd_health.get("status") == "healthy"
    
    return {
        "system": "V-LABS Educational Platform",
        "timestamp": current_time,
        "overall_status": "healthy" if system_healthy else "degraded",
        "uptime_seconds": uptime,
        "components": {
            "backend_com": {
                "name": "Backend Communication",
                "status": "healthy",
                "url": f"http://127.0.0.1:{settings.port}",
                "uptime_seconds": uptime,
                "version": settings.app_version,
                "environment": settings.environment,
                "features": [
                    "API Gateway",
                    "Request Orchestration", 
                    "Authentication Layer",
                    "Business Logic"
                ]
            },
            "backend_bd": {
                "name": "Backend Database",
                "status": bd_health.get("status", "unknown"),
                "url": settings.backend_bd_url,
                "response_time_ms": bd_health.get("response_time_ms"),
                "details": bd_health.get("data", {}),
                "error": bd_health.get("message") if bd_health.get("status") != "healthy" else None
            },
            "frontend": {
                "name": "Frontend Application",
                "status": "unknown",
                "note": "Status não verificado - implementar health check do frontend"
            }
        },
        "integration_tests": {
            "backend_com_to_bd": {
                "status": "passed" if bd_health.get("status") == "healthy" else "failed",
                "tested_at": current_time,
                "details": bd_health
            }
        },
        "monitoring": {
            "logs_active": True,
            "metrics_collected": True,
            "health_checks": True
        }
    }


@app.get(
    "/info",
    summary="ℹ️ Application Info",
    description="Informações técnicas detalhadas da aplicação",
    tags=["Info"]
)
async def app_info():
    """
    Informações técnicas detalhadas da aplicação.
    
    Returns:
        dict: Configurações, runtime info e capacidades
    """
    settings = config.get_settings()
    
    return {
        "application": {
            "name": settings.app_name,
            "version": settings.app_version,
            "environment": settings.environment,
            "debug_mode": settings.debug,
            "description": "Camada de comunicação e orquestração do V-LABS"
        },
        "runtime": {
            "uptime_seconds": round(time.time() - app_start_time, 2),
            "start_time": app_start_time,
            "current_time": time.time(),
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "platform": sys.platform
        },
        "configuration": {
            "host": settings.host,
            "port": settings.port,
            "backend_bd_url": settings.backend_bd_url,
            "backend_bd_timeout": settings.backend_bd_timeout,
            "cors_origins": settings.cors_origins,
            "log_level": settings.log_level
        },
        "features": {
            "authentication": "JWT + Session support",
            "user_management": "Full CRUD operations",
            "educational_content": "Q&A + Semantic search",
            "semantic_search": "Vector-based content search",
            "health_monitoring": "Multi-layer health checks",
            "request_orchestration": "Backend_BD integration"
        },
        "api": {
            "docs_url": "/docs" if settings.debug else None,
            "openapi_url": "/openapi.json" if settings.debug else None,
            "total_endpoints": len([route for route in app.routes if hasattr(route, 'methods')]),
        }
    }


# ===============================================
# EXECUÇÃO DIRETA
# ===============================================

if __name__ == "__main__":
    """
    Execução direta da aplicação (desenvolvimento).
    """
    import uvicorn
    
    settings = config.get_settings()
    
    logger.info(f"🚀 Starting {settings.app_name} in development mode")
    logger.info(f"🌍 Environment: {settings.environment}")
    logger.info(f"🔧 Debug mode: {settings.debug}")
    logger.info(f"📍 Server: http://{settings.host}:{settings.port}")
    logger.info(f"📚 Docs: http://{settings.host}:{settings.port}/docs")
    logger.info(f"🔗 Backend_BD: {settings.backend_bd_url}")
    
    try:
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
    except KeyboardInterrupt:
        logger.info("🛑 Application stopped by user")
    except Exception as e:
        logger.error(f"💥 Failed to start application: {str(e)}")
        sys.exit(1)