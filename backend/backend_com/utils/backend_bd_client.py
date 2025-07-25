# utils/backend_bd_client.py
"""
Cliente para comunicação com o backend_bd.
"""

import httpx
import asyncio
from typing import Dict, Any, Optional
from config import get_settings


class BackendBDClient:
    """Cliente para comunicação com backend_bd."""
    
    def __init__(self):
        self.settings = get_settings()
        self.base_url = self.settings.backend_bd_url
        self.timeout = self.settings.backend_bd_timeout
        
    async def health_check(self) -> Dict[str, Any]:
        """Verifica saúde do backend_bd."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.base_url}/health")
                response.raise_for_status()
                return response.json()
        except Exception as e:
            return {
                "status": "error",
                "message": f"Backend_BD não disponível: {str(e)}"
            }
    
    async def get_questions(self, limit: int = 10) -> Dict[str, Any]:
        """Busca perguntas no backend_bd."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/questions",
                    params={"limit": limit}
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            return {
                "error": True,
                "message": f"Erro ao buscar perguntas: {str(e)}",
                "questions": []
            }
    
    async def create_question(self, question_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria uma pergunta no backend_bd."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/questions",
                    json=question_data
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            return {
                "error": True,
                "message": f"Erro ao criar pergunta: {str(e)}"
            }


# Instância global do cliente
backend_bd_client = BackendBDClient()


# routers/__init__.py - Atualização para usar backend_bd real
"""
Exemplo de como atualizar os roteadores para usar backend_bd real.
"""

from fastapi import APIRouter, HTTPException
from utils.backend_bd_client import backend_bd_client

# Atualização do educational_router
educational_router = APIRouter(prefix="/educational", tags=["Educational"])

@educational_router.get("/questions", summary="Listar Perguntas Reais")
async def get_questions_real():
    """Busca perguntas reais do backend_bd."""
    
    # Chama o backend_bd
    result = await backend_bd_client.get_questions()
    
    if result.get("error"):
        raise HTTPException(
            status_code=503,
            detail=f"Serviço indisponível: {result.get('message')}"
        )
    
    return {
        "questions": result.get("questions", []),
        "total": len(result.get("questions", [])),
        "source": "backend_bd",
        "status": "success"
    }

@educational_router.get("/health-integration", summary="Teste de Integração")
async def test_integration():
    """Testa integração com backend_bd."""
    
    # Verifica conectividade
    health = await backend_bd_client.health_check()
    
    return {
        "backend_com_status": "ok",
        "backend_bd_status": health.get("status", "unknown"),
        "integration": "working" if health.get("status") == "ok" else "failed",
        "backend_bd_response": health
    }


# main.py - Endpoint para testar integração completa
@app.get("/system/status", summary="Status do Sistema Completo")
async def system_status():
    """Status de todo o sistema V-LABS."""
    
    # Testa backend_bd
    bd_health = await backend_bd_client.health_check()
    
    return {
        "system": "V-LABS",
        "components": {
            "backend_com": {
                "status": "ok",
                "url": "http://127.0.0.1:8000",
                "uptime_seconds": round(time.time() - app_start_time, 2)
            },
            "backend_bd": {
                "status": bd_health.get("status", "unknown"),
                "url": "http://127.0.0.1:8001",
                "response": bd_health
            },
            "frontend": {
                "status": "unknown",
                "note": "Status não verificado"
            }
        },
        "integration_test": {
            "backend_com_to_bd": "working" if bd_health.get("status") == "ok" else "failed"
        }
    }