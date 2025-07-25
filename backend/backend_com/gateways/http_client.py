"""
Cliente HTTP reutilizável para comunicação com serviços externos.

Implementa funcionalidades de requisições HTTP com retry,
timeout e tratamento de erros robusto.
"""

import asyncio
import json
import time
from typing import Any, Dict, Optional, Union
from dataclasses import dataclass
import httpx

from .base_gateway import (
    GatewayError, 
    ConnectionError, 
    TimeoutError, 
    ServiceUnavailableError
)
from ..utils.logging import setup_logger


@dataclass
class RequestConfig:
    """Configuração para requisições HTTP."""
    
    timeout: int = 30
    max_retries: int = 3
    retry_delay: float = 1.0
    retry_backoff: float = 2.0
    headers: Optional[Dict[str, str]] = None
    verify_ssl: bool = True


@dataclass 
class HTTPResponse:
    """Resposta HTTP padronizada."""
    
    status_code: int
    content: Union[Dict[str, Any], str, bytes]
    headers: Dict[str, str]
    duration_ms: float
    url: str
    
    @property
    def is_success(self) -> bool:
        """Verifica se resposta foi bem-sucedida."""
        return 200 <= self.status_code < 300
    
    @property
    def is_json(self) -> bool:
        """Verifica se conteúdo é JSON."""
        return isinstance(self.content, dict)


class HTTPClient:
    """
    Cliente HTTP assíncrono com recursos avançados.
    
    Fornece funcionalidades de retry, timeout, logging e
    tratamento de erros para comunicação com APIs externas.
    """
    
    def __init__(self, base_url: str, default_config: Optional[RequestConfig] = None):
        self.base_url = base_url.rstrip('/')
        self.default_config = default_config or RequestConfig()
        self.logger = setup_logger("http_client")
        self._client: Optional[httpx.AsyncClient] = None
    
    async def _get_client(self) -> httpx.AsyncClient:
        """Obtém cliente HTTP reutilizável."""
        if self._client is None:
            self._client = httpx.AsyncClient(
                timeout=httpx.Timeout(self.default_config.timeout),
                verify=self.default_config.verify_ssl,
                limits=httpx.Limits(max_keepalive_connections=20, max_connections=100)
            )
        return self._client
    
    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None,
                  config: Optional[RequestConfig] = None) -> HTTPResponse:
        """
        Executa requisição GET.
        
        Args:
            endpoint: Endpoint para requisição
            params: Parâmetros de query
            config: Configuração da requisição
            
        Returns:
            HTTPResponse: Resposta da requisição
        """
        return await self._request("GET", endpoint, params=params, config=config)
    
    async def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None,
                   json_data: Optional[Dict[str, Any]] = None,
                   config: Optional[RequestConfig] = None) -> HTTPResponse:
        """
        Executa requisição POST.
        
        Args:
            endpoint: Endpoint para requisição
            data: Dados para enviar como form-data
            json_data: Dados para enviar como JSON
            config: Configuração da requisição
            
        Returns:
            HTTPResponse: Resposta da requisição
        """
        return await self._request("POST", endpoint, data=data, 
                                 json_data=json_data, config=config)
    
    async def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None,
                  json_data: Optional[Dict[str, Any]] = None,
                  config: Optional[RequestConfig] = None) -> HTTPResponse:
        """
        Executa requisição PUT.
        
        Args:
            endpoint: Endpoint para requisição
            data: Dados para enviar como form-data
            json_data: Dados para enviar como JSON
            config: Configuração da requisição
            
        Returns:
            HTTPResponse: Resposta da requisição
        """
        return await self._request("PUT", endpoint, data=data,
                                 json_data=json_data, config=config)
    
    async def delete(self, endpoint: str, params: Optional[Dict[str, Any]] = None,
                     config: Optional[RequestConfig] = None) -> HTTPResponse:
        """
        Executa requisição DELETE.
        
        Args:
            endpoint: Endpoint para requisição
            params: Parâmetros de query
            config: Configuração da requisição
            
        Returns:
            HTTPResponse: Resposta da requisição
        """
        return await self._request("DELETE", endpoint, params=params, config=config)
    
    async def _request(self, method: str, endpoint: str,
                      params: Optional[Dict[str, Any]] = None,
                      data: Optional[Dict[str, Any]] = None,
                      json_data: Optional[Dict[str, Any]] = None,
                      config: Optional[RequestConfig] = None) -> HTTPResponse:
        """
        Executa requisição HTTP com retry e tratamento de erros.
        
        Args:
            method: Método HTTP
            endpoint: Endpoint para requisição
            params: Parâmetros de query
            data: Dados form-data
            json_data: Dados JSON
            config: Configuração da requisição
            
        Returns:
            HTTPResponse: Resposta da requisição
            
        Raises:
            GatewayError: Em caso de erro na requisição
        """
        req_config = config or self.default_config
        url = self._build_url(endpoint)
        headers = self._prepare_headers(req_config.headers)
        
        last_exception = None
        
        for attempt in range(req_config.max_retries + 1):
            start_time = time.time()
            
            try:
                self.logger.info(
                    f"HTTP {method} request attempt {attempt + 1}",
                    extra={
                        "method": method,
                        "url": url,
                        "attempt": attempt + 1,
                        "max_attempts": req_config.max_retries + 1
                    }
                )
                
                client = await self._get_client()
                
                # Prepara argumentos da requisição
                request_kwargs = {
                    "method": method,
                    "url": url,
                    "headers": headers,
                    "timeout": req_config.timeout
                }
                
                if params:
                    request_kwargs["params"] = params
                
                if json_data:
                    request_kwargs["json"] = json_data
                elif data:
                    request_kwargs["data"] = data
                
                # Executa requisição
                response = await client.request(**request_kwargs)
                duration_ms = (time.time() - start_time) * 1000
                
                # Processa resposta
                http_response = await self._process_response(
                    response, url, duration_ms
                )
                
                self.logger.info(
                    f"HTTP {method} request successful",
                    extra={
                        "method": method,
                        "url": url,
                        "status_code": response.status_code,
                        "duration_ms": duration_ms,
                        "attempt": attempt + 1
                    }
                )
                
                return http_response
                
            except httpx.ConnectError as e:
                last_exception = ConnectionError(
                    f"Failed to connect to {url}",
                    details={"original_error": str(e)}
                )
                
            except httpx.TimeoutException as e:
                last_exception = TimeoutError(
                    f"Request to {url} timed out after {req_config.timeout}s",
                    details={"original_error": str(e)}
                )
                
            except httpx.HTTPStatusError as e:
                duration_ms = (time.time() - start_time) * 1000
                
                # Para erros HTTP, não tenta novamente
                if e.response.status_code < 500:
                    http_response = await self._process_response(
                        e.response, url, duration_ms
                    )
                    return http_response
                
                last_exception = ServiceUnavailableError(
                    f"Server error {e.response.status_code} from {url}",
                    status_code=e.response.status_code,
                    details={"response_text": e.response.text}
                )
                
            except Exception as e:
                last_exception = GatewayError(
                    f"Unexpected error during request to {url}",
                    details={"original_error": str(e)}
                )
            
            # Log do erro e aguarda antes do próximo retry
            duration_ms = (time.time() - start_time) * 1000
            
            self.logger.warning(
                f"HTTP {method} request failed, attempt {attempt + 1}",
                extra={
                    "method": method,
                    "url": url,
                    "error": str(last_exception),
                    "duration_ms": duration_ms,
                    "attempt": attempt + 1,
                    "will_retry": attempt < req_config.max_retries
                }
            )
            
            # Aguarda antes do próximo retry (com backoff exponencial)
            if attempt < req_config.max_retries:
                delay = req_config.retry_delay * (req_config.retry_backoff ** attempt)
                await asyncio.sleep(delay)
        
        # Todas as tentativas falharam
        self.logger.error(
            f"HTTP {method} request failed after {req_config.max_retries + 1} attempts",
            extra={
                "method": method,
                "url": url,
                "final_error": str(last_exception)
            }
        )
        
        raise last_exception
    
    async def _process_response(self, response: httpx.Response, 
                               url: str, duration_ms: float) -> HTTPResponse:
        """
        Processa resposta HTTP e converte para HTTPResponse.
        
        Args:
            response: Resposta do httpx
            url: URL da requisição
            duration_ms: Duração da requisição
            
        Returns:
            HTTPResponse: Resposta processada
        """
        # Tenta fazer parse do JSON se content-type for apropriado
        content_type = response.headers.get("content-type", "").lower()
        
        if "application/json" in content_type:
            try:
                content = response.json()
            except json.JSONDecodeError:
                content = response.text
        else:
            content = response.text
        
        return HTTPResponse(
            status_code=response.status_code,
            content=content,
            headers=dict(response.headers),
            duration_ms=duration_ms,
            url=url
        )
    
    def _build_url(self, endpoint: str) -> str:
        """Constrói URL completa."""
        endpoint = endpoint.lstrip('/')
        return f"{self.base_url}/{endpoint}"
    
    def _prepare_headers(self, additional_headers: Optional[Dict[str, str]]) -> Dict[str, str]:
        """Prepara headers da requisição."""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "V-LABS-Backend-Com/1.0"
        }
        
        if additional_headers:
            headers.update(additional_headers)
        
        return headers
    
    async def close(self) -> None:
        """Fecha cliente HTTP e limpa recursos."""
        if self._client:
            await self._client.aclose()
            self._client = None
        
        self.logger.info("HTTP client closed")