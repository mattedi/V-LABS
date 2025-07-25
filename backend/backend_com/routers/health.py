"""
Endpoints de health check e status do sistema.

Fornece informações sobre a saúde do backend_com e
serviços dependentes para monitoramento.
"""

import time
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any

from ..models import HealthResponse
from ..gateways import PersistenceGateway
from ..config import get_settings
from ..utils.logging import setup_logger

# Configuração do router
router = APIRouter(
    prefix="/health",
    tags=["Health Check"],
    responses={
        500: {"description": "Internal server error"}
    }
)

# Logger específico para health checks
logger = setup_logger("health_router")

# Tempo de inicialização para calcular uptime
START_TIME = time.time()


@router.get(
    "/",
    response_model=HealthResponse,
    summary="Health Check Básico",
    description="Verifica se o serviço está funcionando corretamente"
)
async def health_check():
    """
    Endpoint básico de health check.
    
    Retorna status básico do serviço sem verificar dependências.
    Usado por load balancers e sistemas de monitoramento simples.
    
    Returns:
        HealthResponse: Status básico do serviço
    """
    try:
        settings = get_settings()
        current_time = time.time()
        uptime = current_time - START_TIME
        
        return HealthResponse(
            status="healthy",
            timestamp=datetime.utcnow(),
            version=settings.app_version,
            services={"backend_com": "healthy"},
            uptime=uptime
        )
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}", exc_info=e)
        raise HTTPException(
            status_code=500,
            detail="Health check failed"
        )


@router.get(
    "/detailed",
    response_model=Dict[str, Any],
    summary="Health Check Detalhado",
    description="Verifica saúde do serviço e todas as dependências"
)
async def detailed_health_check():
    """
    Health check completo incluindo dependências.
    
    Verifica:
    - Status do backend_com
    - Conectividade com backend_bd
    - Status do MongoDB
    - Status do Qdrant
    - Métricas de performance
    
    Returns:
        dict: Status detalhado de todos os componentes
    """
    try:
        settings = get_settings()
        current_time = time.time()
        uptime = current_time - START_TIME
        
        health_status = {
            "service": {
                "name": settings.app_name,
                "version": settings.app_version,
                "status": "healthy",
                "uptime_seconds": uptime,
                "environment": settings.environment,
                "timestamp": datetime.utcnow().isoformat()
            },
            "dependencies": {},
            "metrics": {
                "uptime_seconds": uptime,
                "memory_usage": _get_memory_usage(),
                "response_time_ms": 0  # Será calculado no final
            }
        }
        
        start_check_time = time.time()
        
        # Verifica backend_bd (MongoDB + Qdrant)
        try:
            persistence_gateway = PersistenceGateway()
            bd_health = await persistence_gateway.health_check()
            
            if bd_health.success:
                health_status["dependencies"]["backend_bd"] = {
                    "status": "healthy",
                    "response_time_ms": bd_health.duration_ms,
                    "details": bd_health.data
                }
            else:
                health_status["dependencies"]["backend_bd"] = {
                    "status": "unhealthy",
                    "error": bd_health.error_message,
                    "response_time_ms": bd_health.duration_ms
                }
                health_status["service"]["status"] = "degraded"
            
            await persistence_gateway.close()
            
        except Exception as e:
            health_status["dependencies"]["backend_bd"] = {
                "status": "unhealthy",
                "error": str(e)
            }
            health_status["service"]["status"] = "degraded"
        
        # Calcula tempo de resposta total
        total_check_time = (time.time() - start_check_time) * 1000
        health_status["metrics"]["response_time_ms"] = round(total_check_time, 2)
        
        # Determina status HTTP baseado na saúde geral
        if health_status["service"]["status"] == "unhealthy":
            raise HTTPException(
                status_code=503,
                detail=health_status
            )
        
        return health_status
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Detailed health check failed: {str(e)}", exc_info=e)
        raise HTTPException(
            status_code=500,
            detail={
                "service": {
                    "status": "unhealthy",
                    "error": str(e),
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
        )


@router.get(
    "/ready",
    response_model=Dict[str, Any],
    summary="Readiness Check",
    description="Verifica se o serviço está pronto para receber tráfego"
)
async def readiness_check():
    """
    Readiness check para Kubernetes/orquestradores.
    
    Verifica se o serviço está totalmente inicializado e
    pronto para processar requisições de usuários.
    
    Returns:
        dict: Status de prontidão do serviço
    """
    try:
        settings = get_settings()
        
        readiness_status = {
            "ready": True,
            "checks": {},
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Verifica se configurações essenciais estão carregadas
        essential_configs = [
            ("backend_bd_url", settings.backend_bd_url),
            ("app_name", settings.app_name),
            ("environment", settings.environment)
        ]
        
        for config_name, config_value in essential_configs:
            if not config_value:
                readiness_status["ready"] = False
                readiness_status["checks"][config_name] = {
                    "status": "failed",
                    "reason": "Configuration not loaded"
                }
            else:
                readiness_status["checks"][config_name] = {
                    "status": "passed"
                }
        
        # Testa conectividade básica com backend_bd
        try:
            persistence_gateway = PersistenceGateway()
            bd_health = await persistence_gateway.health_check()
            
            if bd_health.success:
                readiness_status["checks"]["backend_bd_connectivity"] = {
                    "status": "passed",
                    "response_time_ms": bd_health.duration_ms
                }
            else:
                readiness_status["ready"] = False
                readiness_status["checks"]["backend_bd_connectivity"] = {
                    "status": "failed",
                    "reason": bd_health.error_message
                }
            
            await persistence_gateway.close()
            
        except Exception as e:
            readiness_status["ready"] = False
            readiness_status["checks"]["backend_bd_connectivity"] = {
                "status": "failed",
                "reason": str(e)
            }
        
        # Retorna status HTTP apropriado
        if not readiness_status["ready"]:
            raise HTTPException(
                status_code=503,
                detail=readiness_status
            )
        
        return readiness_status
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Readiness check failed: {str(e)}", exc_info=e)
        raise HTTPException(
            status_code=500,
            detail={
                "ready": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
        )


@router.get(
    "/live",
    response_model=Dict[str, str],
    summary="Liveness Check", 
    description="Verifica se o serviço está vivo (para Kubernetes)"
)
async def liveness_check():
    """
    Liveness check para Kubernetes.
    
    Verificação simples que retorna apenas se o processo
    está executando. Não verifica dependências externas.
    
    Returns:
        dict: Status de liveness simples
    """
    return {
        "alive": "true",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get(
    "/metrics",
    response_model=Dict[str, Any],
    summary="Métricas do Sistema",
    description="Retorna métricas básicas para monitoramento"
)
async def get_metrics():
    """
    Endpoint de métricas para monitoramento.
    
    Fornece métricas básicas do sistema que podem ser
    coletadas por ferramentas como Prometheus.
    
    Returns:
        dict: Métricas do sistema
    """
    try:
        current_time = time.time()
        uptime = current_time - START_TIME
        
        metrics = {
            "uptime_seconds": uptime,
            "memory_usage": _get_memory_usage(),
            "timestamp": datetime.utcnow().isoformat(),
            "counters": {
                # Em implementação real, estes contadores seriam mantidos
                "requests_total": 0,
                "requests_success": 0,
                "requests_error": 0
            },
            "gauges": {
                "active_connections": 0,
                "queue_size": 0
            }
        }
        
        return metrics
        
    except Exception as e:
        logger.error(f"Metrics collection failed: {str(e)}", exc_info=e)
        raise HTTPException(
            status_code=500,
            detail="Failed to collect metrics"
        )


def _get_memory_usage() -> Dict[str, float]:
    """
    Obtém informações de uso de memória.
    
    Returns:
        dict: Informações de memória em MB
    """
    try:
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        
        return {
            "rss_mb": round(memory_info.rss / 1024 / 1024, 2),
            "vms_mb": round(memory_info.vms / 1024 / 1024, 2),
            "percent": round(process.memory_percent(), 2)
        }
        
    except ImportError:
        # psutil não disponível - retorna informações básicas usando resource
        try:
            import resource
            
            memory_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            
            # ru_maxrss está em KB no Linux, bytes no macOS
            import sys
            if sys.platform == 'darwin':  # macOS
                memory_mb = memory_usage / 1024 / 1024
            else:  # Linux
                memory_mb = memory_usage / 1024
            
            return {
                "rss_mb": round(memory_mb, 2),
                "vms_mb": 0,
                "percent": 0
            }
        except Exception:
            # Fallback final - retorna valores padrão
            return {
                "rss_mb": 0,
                "vms_mb": 0,
                "percent": 0
            }
        
    except Exception as e:
        # Erro ao usar psutil - log e retorna valores padrão
        logger.warning(f"Failed to get memory usage: {str(e)}")
        return {
            "rss_mb": 0,
            "vms_mb": 0,
            "percent": 0
        }