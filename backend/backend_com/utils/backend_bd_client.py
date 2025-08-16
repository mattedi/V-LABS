"""
Cliente para comunicação com o backend_bd.

Este módulo fornece uma interface limpa para comunicação
com o serviço de persistência do V-LABS.
"""

import httpx
import time
from typing import Dict, Any, Optional, List
from backend_com.config import get_settings


class BackendBDClient:
    """
    Cliente assíncrono para comunicação com backend_bd.
    
    Fornece métodos para todas as operações de integração
    com o serviço de persistência.
    """
    
    def __init__(self):
        """Inicializa cliente com configurações do sistema."""
        self.settings = get_settings()
        self.base_url = self.settings.backend_bd_url
        self.timeout = self.settings.backend_bd_timeout
        
    async def health_check(self) -> Dict[str, Any]:
        """
        Verifica saúde do backend_bd.
        
        Returns:
            dict: Status de saúde e informações do serviço
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                start_time = time.time()
                response = await client.get(f"{self.base_url}/health")
                response_time = (time.time() - start_time) * 1000
                
                response.raise_for_status()
                
                return {
                    "status": "healthy",
                    "response_time_ms": round(response_time, 2),
                    "data": response.json(),
                    "url": f"{self.base_url}/health"
                }
                
        except httpx.TimeoutException:
            return {
                "status": "timeout",
                "message": f"Backend_BD timeout após {self.timeout}s",
                "url": f"{self.base_url}/health"
            }
        except httpx.HTTPStatusError as e:
            return {
                "status": "http_error",
                "status_code": e.response.status_code,
                "message": f"Backend_BD retornou {e.response.status_code}",
                "url": f"{self.base_url}/health"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Erro de conexão: {str(e)}",
                "url": f"{self.base_url}/health"
            }
    
    async def get_questions(self, limit: int = 10, offset: int = 0) -> Dict[str, Any]:
        """
        Busca perguntas no backend_bd.
        
        Args:
            limit: Número máximo de perguntas
            offset: Deslocamento para paginação
            
        Returns:
            dict: Lista de perguntas ou erro
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/questions",
                    params={"limit": limit, "offset": offset}
                )
                response.raise_for_status()
                
                data = response.json()
                return {
                    "success": True,
                    "questions": data.get("questions", []),
                    "total": data.get("total", 0),
                    "limit": limit,
                    "offset": offset,
                    "source": "backend_bd"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": True,
                "message": f"Erro ao buscar perguntas: {str(e)}",
                "questions": [],
                "total": 0
            }
    
    async def create_question(self, question_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cria uma pergunta no backend_bd.
        
        Args:
            question_data: Dados da pergunta
            
        Returns:
            dict: Pergunta criada ou erro
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/questions",
                    json=question_data
                )
                response.raise_for_status()
                
                return {
                    "success": True,
                    "question": response.json(),
                    "message": "Pergunta criada com sucesso"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": True,
                "message": f"Erro ao criar pergunta: {str(e)}"
            }
    
    async def get_users(self, limit: int = 10) -> Dict[str, Any]:
        """
        Busca usuários no backend_bd.
        
        Args:
            limit: Número máximo de usuários
            
        Returns:
            dict: Lista de usuários ou erro
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/users",
                    params={"limit": limit}
                )
                response.raise_for_status()
                
                data = response.json()
                return {
                    "success": True,
                    "users": data.get("users", []),
                    "total": data.get("total", 0),
                    "source": "backend_bd"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": True,
                "message": f"Erro ao buscar usuários: {str(e)}",
                "users": [],
                "total": 0
            }
    
    async def authenticate_user(self, email: str, password: str) -> Dict[str, Any]:
        """
        Autentica usuário no backend_bd.
        
        Args:
            email: Email do usuário
            password: Senha do usuário
            
        Returns:
            dict: Dados do usuário autenticado ou erro
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/auth/login",
                    json={"email": email, "password": password}
                )
                response.raise_for_status()
                
                return {
                    "success": True,
                    "user": response.json(),
                    "message": "Usuário autenticado com sucesso"
                }
                
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                return {
                    "success": False,
                    "error": True,
                    "message": "Credenciais inválidas"
                }
            else:
                return {
                    "success": False,
                    "error": True,
                    "message": f"Erro de autenticação: {e.response.status_code}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": True,
                "message": f"Erro ao autenticar: {str(e)}"
            }


# Instância global do cliente (singleton)
_backend_bd_client = None

def get_backend_bd_client() -> BackendBDClient:
    """
    Retorna instância singleton do cliente backend_bd.
    
    Returns:
        BackendBDClient: Instância do cliente
    """
    global _backend_bd_client
    if _backend_bd_client is None:
        _backend_bd_client = BackendBDClient()
    return _backend_bd_client