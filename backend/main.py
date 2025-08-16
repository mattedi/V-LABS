"""backend/main.py – V-LABS Backend Communication (versão 2025-08-16)
================================================================================
Camada de orquestração entre Frontend e Backend_BD. Refatoração completa sem
`sys.path` hacks, com tipagem estática, logging estruturado e ciclo de vida
controlado por `lifespan`.

Requisitos de layout do projeto (todos diretórios devem conter `__init__.py`):

V-LABS/
└── backend/
    ├── __init__.py
    ├── main.py               # ← ESTE ARQUIVO
    └── backend_com/
        ├── __init__.py
        ├── config.py         # get_settings(), get_cors_config(), Settings
        ├── utils.py          # configure_structured_logging(), setup_logger()
        └── routers/
            ├── __init__.py   # define __all__ com referências aos routers
            └── health.py …

Execute em desenvolvimento:
    uvicorn backend.main:app --reload

Execute em produção (exemplo systemd):
    gunicorn -k uvicorn.workers.UvicornWorker backend.main:app
"""
from __future__ import annotations

import sys
import time
from contextlib import asynccontextmanager
from typing import Any, Dict, Iterable

import httpx
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse

# ──────────────────────────────────────────────────────────────────────────────
# Imports locais (absolutos)
# ──────────────────────────────────────────────────────────────────────────────
from backend.backend_com.config import Settings, get_cors_config, get_settings
from backend.backend_com import routers               # routers.__all__ = [...]
from backend.backend_com.utils import (
    configure_structured_logging,
    setup_logger,
)

# ──────────────────────────────────────────────────────────────────────────────
# Logging estruturado
# ──────────────────────────────────────────────────────────────────────────────
configure_structured_logging()
logger = setup_logger("backend.main")

app_start_time = time.time()
http_client: httpx.AsyncClient | None = None

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║ Ciclo de vida (startup / shutdown)                                        ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
@asynccontextmanager
async def lifespan(app: FastAPI):
    global http_client
    s: Settings = get_settings()

    logger.info("🏁 Iniciando %s v%s (%s)", s.app_name, s.app_version, s.environment)
    http_client = httpx.AsyncClient(timeout=s.backend_bd_timeout)

    try:
        yield
    finally:
        logger.info("🔻 Encerrando serviço %s …", s.app_name)
        if http_client:
            await http_client.aclose()

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║ Fábrica da aplicação                                                      ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
def create_app() -> FastAPI:
    s: Settings = get_settings()
    app = FastAPI(
        title=s.app_name,
        version=s.app_version,
        description="Camada de comunicação da plataforma educacional V-LABS.",
        contact={"name": "V-LABS Team", "email": "support@v-labs.edu.br"},
        lifespan=lifespan,
        docs_url="/docs" if s.debug else None,
        redoc_url="/redoc" if s.debug else None,
        openapi_url="/openapi.json" if s.debug else None,
    )

    _setup_middlewares(app)
    _setup_routers(app, routers.__all__)
    _setup_exception_handlers(app)
    logger.info("✅ FastAPI configurado (rotas=%s)", len(app.routes))
    return app

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║ Middlewares                                                               ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
def _setup_middlewares(app: FastAPI) -> None:
    s = get_settings()
    app.add_middleware(CORSMiddleware, **get_cors_config())

    if not s.debug:
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=["*.v-labs.edu.br", "localhost", "127.0.0.1"],
        )

    @app.middleware("http")
    async def _log_requests(request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        duration = (time.perf_counter() - start) * 1000
        level = "info" if response.status_code < 400 else (
            "warning" if response.status_code < 500 else "error"
        )
        getattr(logger, level)(
            "%s %s → %s (%.1f ms)",
            request.method,
            request.url.path,
            response.status_code,
            duration,
        )
        response.headers["X-Process-Time"] = f"{duration:.1f}"
        return response

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║ Routers                                                                   ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
def _setup_routers(app: FastAPI, router_names: Iterable[str]) -> None:
    for name in router_names:
        app.include_router(getattr(routers, name))
        logger.info("Router %s incluído", name)

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║ Exception Handlers                                                        ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
def _setup_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(HTTPException)
    async def _http_exc(request: Request, exc: HTTPException):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    @app.exception_handler(RequestValidationError)
    async def _validation_exc(request: Request, exc: RequestValidationError):
        return JSONResponse(status_code=422, content={"errors": exc.errors()})

    @app.exception_handler(Exception)
    async def _unhandled_exc(request: Request, exc: Exception):
        logger.error("Erro inesperado: %s", exc, exc_info=True)
        return JSONResponse(status_code=500, content={"detail": "Internal server error"})

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║ Instância da aplicação                                                    ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
app = create_app()

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║ Endpoints básicos                                                         ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
@app.get("/", tags=["Root"])
async def root():
    s = get_settings()
    return {
        "service": s.app_name,
        "version": s.app_version,
        "environment": s.environment,
        "uptime_seconds": round(time.time() - app_start_time, 1),
    }

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║ Execução direta                                                           ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
