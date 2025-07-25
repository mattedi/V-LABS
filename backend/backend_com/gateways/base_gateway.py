"""
Gateway base para comunicação com serviços externos.

Define interfaces comuns e tratamento de erros para todos os gateways.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Union
from dataclasses import dataclass
from datetime import datetime
import logging

from ..utils.logging import setup_logger


class GatewayError(Exception):
    """Erro base para operações de gateway."""
    
    def __init__(self, message: str, status_code: Optional[int] = None, 
                 details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        self.timestamp = datetime.utcnow()


class ConnectionError(GatewayError):
    """Erro de conexão com serviço externo."""
    pass


class TimeoutError(GatewayError):
    """Erro de timeout em operação."""
    pass


class ServiceUnavailableError(GatewayError):
    """Serviço externo indisponível."""
    pass


class AuthenticationError(GatewayError):
    """Erro de autenticação com serviço externo."""
    pass


class ValidationError(GatewayError):
    """Erro de validação de dados."""
    pass


@dataclass
class GatewayResponse:
    """
    Resposta padronizada para operações de gateway.
    """
    success: bool
    data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    status_code: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None
    duration_ms: Optional[float] = None
    
    @classmethod
    def success_response(cls, data: Optional[Dict[str, Any]] = None,
                        metadata: Optional[Dict[str, Any]] = None,
                        duration_ms: Optional[float] = None) -> 'GatewayResponse':
        """Cria resposta de sucesso."""
        return cls(
            success=True,
            data=data,
            metadata=metadata,
            duration_ms=duration_ms
        )
    
    @classmethod
    def error_response(cls, error_message: str, status_code: Optional[int] = None,
                      metadata: Optional[Dict[str, Any]] = None,
                      duration_ms: Optional[float] = None) -> 'GatewayResponse':
        """Cria resposta de erro."""
        return cls(
            success=False,
            error_message=error_message,
            status_code=status_code,
            metadata=metadata,
            duration_ms=duration_ms
        )


class BaseGateway(ABC):
    """
    Classe base para todos os gateways de comunicação.
    
    Fornece funcionalidades comuns como logging, tratamento de erros
    e métricas básicas.
    """
    
    def __init__(self, service_name: str, base_url: str, timeout: int = 30):
        self.service_name = service_name
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.logger = setup_logger(f"gateway.{service_name}")
        self._connection_pool = None
        
    @abstractmethod
    async def health_check(self) -> GatewayResponse:
        """
        Verifica se o serviço está disponível.
        
        Returns:
            GatewayResponse: Status de saúde do serviço
        """
        pass
    
    def _log_request(self, method: str, endpoint: str, 
                    data: Optional[Dict[str, Any]] = None) -> None:
        """Log de requisição enviada."""
        self.logger.info(
            f"Sending {method} request to {self.service_name}",
            extra={
                "service": self.service_name,
                "method": method,
                "endpoint": endpoint,
                "has_data": data is not None
            }
        )
    
    def _log_response(self, method: str, endpoint: str, status_code: int,
                     duration_ms: float, success: bool) -> None:
        """Log de resposta recebida."""
        log_level = "info" if success else "error"
        getattr(self.logger, log_level)(
            f"Received response from {self.service_name}",
            extra={
                "service": self.service_name,
                "method": method,
                "endpoint": endpoint,
                "status_code": status_code,
                "duration_ms": duration_ms,
                "success": success
            }
        )
    
    def _log_error(self, method: str, endpoint: str, error: Exception,
                  duration_ms: Optional[float] = None) -> None:
        """Log de erro durante comunicação."""
        self.logger.error(
            f"Error communicating with {self.service_name}",
            extra={
                "service": self.service_name,
                "method": method,
                "endpoint": endpoint,
                "error_type": type(error).__name__,
                "error_message": str(error),
                "duration_ms": duration_ms
            },
            exc_info=error
        )
    
    def _handle_http_error(self, status_code: int, response_text: str,
                          endpoint: str) -> GatewayError:
        """
        Converte erros HTTP em exceções específicas do gateway.
        
        Args:
            status_code: Código de status HTTP
            response_text: Texto da resposta
            endpoint: Endpoint chamado
            
        Returns:
            GatewayError: Exceção apropriada
        """
        if status_code == 401:
            return AuthenticationError(
                f"Authentication failed for {endpoint}",
                status_code=status_code,
                details={"response": response_text}
            )
        
        elif status_code == 403:
            return AuthenticationError(
                f"Access forbidden for {endpoint}",
                status_code=status_code,
                details={"response": response_text}
            )
        
        elif status_code == 404:
            return ValidationError(
                f"Resource not found: {endpoint}",
                status_code=status_code,
                details={"response": response_text}
            )
        
        elif status_code == 422:
            return ValidationError(
                f"Validation error for {endpoint}",
                status_code=status_code,
                details={"response": response_text}
            )
        
        elif status_code == 429:
            return ServiceUnavailableError(
                f"Rate limit exceeded for {endpoint}",
                status_code=status_code,
                details={"response": response_text}
            )
        
        elif 500 <= status_code < 600:
            return ServiceUnavailableError(
                f"Server error from {self.service_name}: {status_code}",
                status_code=status_code,
                details={"response": response_text}
            )
        
        else:
            return GatewayError(
                f"HTTP error {status_code} from {endpoint}",
                status_code=status_code,
                details={"response": response_text}
            )
    
    def _build_url(self, endpoint: str) -> str:
        """
        Constrói URL completa para endpoint.
        
        Args:
            endpoint: Endpoint relativo
            
        Returns:
            str: URL completa
        """
        endpoint = endpoint.lstrip('/')
        return f"{self.base_url}/{endpoint}"
    
    def _prepare_headers(self, additional_headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """
        Prepara headers padrão para requisições.
        
        Args:
            additional_headers: Headers adicionais
            
        Returns:
            dict: Headers completos
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": f"V-LABS-Backend-Com/1.0"
        }
        
        if additional_headers:
            headers.update(additional_headers)
        
        return headers
    
    async def close(self) -> None:
        """
        Fecha conexões e limpa recursos.
        """
        if self._connection_pool:
            await self._connection_pool.close()
        
        self.logger.info(f"Gateway connection to {self.service_name} closed")