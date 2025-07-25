"""
Utilitários de logging para o backend_com.

Implementa configuração centralizada de logs e funções
auxiliares para auditoria e monitoramento usando apenas
a biblioteca padrão do Python.
"""

import logging
import json
import time
from datetime import datetime
from typing import Any, Dict, Optional
from functools import wraps


def setup_logger(name: str, level: str = "INFO", 
                json_format: bool = False) -> logging.Logger:
    """
    Configura logger com formato estruturado usando biblioteca padrão.
    
    Args:
        name: Nome do logger
        level: Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        json_format: Se deve usar formato JSON (implementação simples)
        
    Returns:
        logging.Logger: Logger configurado
    """
    logger = logging.getLogger(name)
    
    # Remove handlers existentes para evitar duplicatas
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Configura nível
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(numeric_level)
    
    # Cria handler para console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(numeric_level)
    
    # Configura formato
    if json_format:
        # Formato JSON simples usando CustomJSONFormatter
        formatter = CustomJSONFormatter()
    else:
        # Formato tradicional
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger


class CustomJSONFormatter(logging.Formatter):
    """
    Formatter customizado para logs em formato JSON usando biblioteca padrão.
    """
    
    def format(self, record):
        log_entry = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'name': record.name,
            'level': record.levelname,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        # Adiciona informações extras se existirem
        if hasattr(record, 'extra') and record.extra:
            log_entry.update(record.extra)
        
        # Adiciona informações de exceção se existirem
        if record.exc_info:
            log_entry['exception'] = self.formatException(record.exc_info)
        
        return json.dumps(log_entry, ensure_ascii=False, default=str)


def log_request(request_data: Dict[str, Any], user_id: Optional[str] = None, 
               logger: Optional[logging.Logger] = None) -> None:
    """
    Registra informações de requisição HTTP.
    
    Args:
        request_data: Dados da requisição
        user_id: ID do usuário (opcional)
        logger: Logger específico (opcional)
    """
    if logger is None:
        logger = logging.getLogger("v_labs.requests")
    
    log_data = {
        "event_type": "http_request",
        "timestamp": datetime.utcnow().isoformat(),
        "method": request_data.get("method"),
        "path": request_data.get("path"),
        "query_params": request_data.get("query_params"),
        "user_agent": request_data.get("user_agent"),
        "remote_addr": request_data.get("remote_addr"),
        "user_id": user_id,
        "content_length": request_data.get("content_length")
    }
    
    # Remove dados sensíveis
    if "headers" in request_data:
        safe_headers = {
            k: v for k, v in request_data["headers"].items()
            if k.lower() not in ["authorization", "cookie", "x-api-key"]
        }
        log_data["headers"] = safe_headers
    
    logger.info("HTTP Request", extra=log_data)


def log_response(response_data: Dict[str, Any], duration_ms: float,
                user_id: Optional[str] = None, logger: Optional[logging.Logger] = None) -> None:
    """
    Registra informações de resposta HTTP.
    
    Args:
        response_data: Dados da resposta
        duration_ms: Duração da requisição em milissegundos
        user_id: ID do usuário (opcional)
        logger: Logger específico (opcional)
    """
    if logger is None:
        logger = logging.getLogger("v_labs.responses")
    
    log_data = {
        "event_type": "http_response",
        "timestamp": datetime.utcnow().isoformat(),
        "status_code": response_data.get("status_code"),
        "content_length": response_data.get("content_length"),
        "duration_ms": round(duration_ms, 2),
        "user_id": user_id
    }
    
    # Determina nível de log baseado no status
    status_code = response_data.get("status_code", 200)
    
    if status_code >= 500:
        logger.error("HTTP Response", extra=log_data)
    elif status_code >= 400:
        logger.warning("HTTP Response", extra=log_data)
    else:
        logger.info("HTTP Response", extra=log_data)


def log_error(error: Exception, context: Optional[Dict[str, Any]] = None,
             user_id: Optional[str] = None, logger: Optional[logging.Logger] = None) -> None:
    """
    Registra erro com contexto adicional.
    
    Args:
        error: Exceção ocorrida
        context: Contexto adicional do erro
        user_id: ID do usuário (opcional)
        logger: Logger específico (opcional)
    """
    if logger is None:
        logger = logging.getLogger("v_labs.errors")
    
    log_data = {
        "event_type": "error",
        "timestamp": datetime.utcnow().isoformat(),
        "error_type": type(error).__name__,
        "error_message": str(error),
        "user_id": user_id,
        "context": context or {}
    }
    
    # Adiciona traceback se disponível
    import traceback
    log_data["traceback"] = traceback.format_exc()
    
    logger.error("Application Error", extra=log_data, exc_info=error)


def log_performance(operation: str, duration_ms: float, 
                   metadata: Optional[Dict[str, Any]] = None,
                   user_id: Optional[str] = None, 
                   logger: Optional[logging.Logger] = None) -> None:
    """
    Registra métricas de performance.
    
    Args:
        operation: Nome da operação
        duration_ms: Duração em milissegundos
        metadata: Metadados adicionais
        user_id: ID do usuário (opcional)
        logger: Logger específico (opcional)
    """
    if logger is None:
        logger = logging.getLogger("v_labs.performance")
    
    log_data = {
        "event_type": "performance",
        "timestamp": datetime.utcnow().isoformat(),
        "operation": operation,
        "duration_ms": round(duration_ms, 2),
        "user_id": user_id,
        "metadata": metadata or {}
    }
    
    # Alerta para operações lentas (> 5 segundos)
    if duration_ms > 5000:
        logger.warning("Slow Operation", extra=log_data)
    else:
        logger.info("Performance Metric", extra=log_data)


def log_business_event(event_name: str, data: Dict[str, Any],
                      user_id: Optional[str] = None,
                      logger: Optional[logging.Logger] = None) -> None:
    """
    Registra evento de negócio para auditoria.
    
    Args:
        event_name: Nome do evento
        data: Dados do evento
        user_id: ID do usuário
        logger: Logger específico (opcional)
    """
    if logger is None:
        logger = logging.getLogger("v_labs.business")
    
    log_data = {
        "event_type": "business_event",
        "timestamp": datetime.utcnow().isoformat(),
        "event_name": event_name,
        "user_id": user_id,
        "data": data
    }
    
    logger.info("Business Event", extra=log_data)


def log_security_event(event_type: str, details: Dict[str, Any],
                      severity: str = "INFO", user_id: Optional[str] = None,
                      logger: Optional[logging.Logger] = None) -> None:
    """
    Registra evento de segurança para monitoramento.
    
    Args:
        event_type: Tipo do evento (login_fail, token_invalid, etc.)
        details: Detalhes do evento
        severity: Severidade (INFO, WARNING, ERROR, CRITICAL)
        user_id: ID do usuário (opcional)
        logger: Logger específico (opcional)
    """
    if logger is None:
        logger = logging.getLogger("v_labs.security")
    
    log_data = {
        "event_type": "security_event",
        "timestamp": datetime.utcnow().isoformat(),
        "security_event_type": event_type,
        "severity": severity.upper(),
        "user_id": user_id,
        "details": details
    }
    
    # Log com nível apropriado baseado na severidade
    severity_upper = severity.upper()
    if severity_upper == "CRITICAL":
        logger.critical("Security Event", extra=log_data)
    elif severity_upper == "ERROR":
        logger.error("Security Event", extra=log_data)
    elif severity_upper == "WARNING":
        logger.warning("Security Event", extra=log_data)
    else:
        logger.info("Security Event", extra=log_data)


def performance_monitor(operation_name: str, logger: Optional[logging.Logger] = None):
    """
    Decorator para monitorar performance de funções.
    
    Args:
        operation_name: Nome da operação para logging
        logger: Logger específico (opcional)
    
    Returns:
        Decorator function
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                
                # Log sucesso
                duration_ms = (time.time() - start_time) * 1000
                log_performance(
                    operation=f"{operation_name}.{func.__name__}",
                    duration_ms=duration_ms,
                    metadata={"status": "success"},
                    logger=logger
                )
                
                return result
                
            except Exception as e:
                # Log erro com performance
                duration_ms = (time.time() - start_time) * 1000
                log_performance(
                    operation=f"{operation_name}.{func.__name__}",
                    duration_ms=duration_ms,
                    metadata={"status": "error", "error": str(e)},
                    logger=logger
                )
                
                # Log erro detalhado
                log_error(
                    error=e,
                    context={
                        "operation": operation_name,
                        "function": func.__name__,
                        "duration_ms": duration_ms
                    },
                    logger=logger
                )
                
                raise
        
        return wrapper
    return decorator


def audit_log(action: str, resource_type: str, resource_id: Optional[str] = None,
             user_id: Optional[str] = None, details: Optional[Dict[str, Any]] = None,
             logger: Optional[logging.Logger] = None) -> None:
    """
    Registra evento de auditoria para compliance.
    
    Args:
        action: Ação realizada (CREATE, READ, UPDATE, DELETE)
        resource_type: Tipo do recurso (user, question, answer, etc.)
        resource_id: ID do recurso (opcional)
        user_id: ID do usuário que realizou a ação
        details: Detalhes adicionais da ação
        logger: Logger específico (opcional)
    """
    if logger is None:
        logger = logging.getLogger("v_labs.audit")
    
    log_data = {
        "event_type": "audit",
        "timestamp": datetime.utcnow().isoformat(),
        "action": action.upper(),
        "resource_type": resource_type,
        "resource_id": resource_id,
        "user_id": user_id,
        "details": details or {}
    }
    
    logger.info("Audit Event", extra=log_data)


def log_database_operation(operation: str, table: str, duration_ms: float,
                          affected_rows: Optional[int] = None,
                          query_hash: Optional[str] = None,
                          logger: Optional[logging.Logger] = None) -> None:
    """
    Registra operação de banco de dados para monitoramento.
    
    Args:
        operation: Tipo de operação (SELECT, INSERT, UPDATE, DELETE)
        table: Tabela afetada
        duration_ms: Duração da operação em milissegundos
        affected_rows: Número de linhas afetadas
        query_hash: Hash da query para identificação
        logger: Logger específico (opcional)
    """
    if logger is None:
        logger = logging.getLogger("v_labs.database")
    
    log_data = {
        "event_type": "database_operation",
        "timestamp": datetime.utcnow().isoformat(),
        "operation": operation.upper(),
        "table": table,
        "duration_ms": round(duration_ms, 2),
        "affected_rows": affected_rows,
        "query_hash": query_hash
    }
    
    # Alerta para queries lentas (> 1 segundo)
    if duration_ms > 1000:
        logger.warning("Slow Database Query", extra=log_data)
    else:
        logger.info("Database Operation", extra=log_data)


def log_external_api_call(service_name: str, endpoint: str, method: str,
                         status_code: int, duration_ms: float,
                         user_id: Optional[str] = None,
                         logger: Optional[logging.Logger] = None) -> None:
    """
    Registra chamada para API externa.
    
    Args:
        service_name: Nome do serviço externo
        endpoint: Endpoint chamado
        method: Método HTTP
        status_code: Código de status da resposta
        duration_ms: Duração da chamada em milissegundos
        user_id: ID do usuário (opcional)
        logger: Logger específico (opcional)
    """
    if logger is None:
        logger = logging.getLogger("v_labs.external_api")
    
    log_data = {
        "event_type": "external_api_call",
        "timestamp": datetime.utcnow().isoformat(),
        "service_name": service_name,
        "endpoint": endpoint,
        "method": method.upper(),
        "status_code": status_code,
        "duration_ms": round(duration_ms, 2),
        "user_id": user_id
    }
    
    # Determina nível de log baseado no status
    if status_code >= 500:
        logger.error("External API Call Failed", extra=log_data)
    elif status_code >= 400:
        logger.warning("External API Call Error", extra=log_data)
    else:
        logger.info("External API Call", extra=log_data)


def configure_structured_logging():
    """
    Configura logging estruturado usando biblioteca padrão do Python.
    
    Configuração global simplificada para toda a aplicação.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def get_correlation_id() -> str:
    """
    Gera ID de correlação para rastreamento de requisições.
    
    Returns:
        str: ID de correlação único
    """
    import uuid
    return str(uuid.uuid4())


class RequestLogger:
    """
    Context manager para logging automático de requisições.
    """
    
    def __init__(self, operation: str, user_id: Optional[str] = None,
                 logger: Optional[logging.Logger] = None):
        self.operation = operation
        self.user_id = user_id
        self.logger = logger or logging.getLogger("v_labs.requests")
        self.start_time = None
        self.correlation_id = get_correlation_id()
    
    def __enter__(self):
        self.start_time = time.time()
        
        self.logger.info(
            f"Starting {self.operation}",
            extra={
                "event_type": "operation_start",
                "operation": self.operation,
                "correlation_id": self.correlation_id,
                "user_id": self.user_id,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
        
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration_ms = (time.time() - self.start_time) * 1000
        
        if exc_type is None:
            # Sucesso
            self.logger.info(
                f"Completed {self.operation}",
                extra={
                    "event_type": "operation_complete",
                    "operation": self.operation,
                    "correlation_id": self.correlation_id,
                    "user_id": self.user_id,
                    "duration_ms": round(duration_ms, 2),
                    "status": "success",
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
        else:
            # Erro
            self.logger.error(
                f"Failed {self.operation}",
                extra={
                    "event_type": "operation_failed",
                    "operation": self.operation,
                    "correlation_id": self.correlation_id,
                    "user_id": self.user_id,
                    "duration_ms": round(duration_ms, 2),
                    "status": "error",
                    "error_type": exc_type.__name__,
                    "error_message": str(exc_val),
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
    
    def add_context(self, **kwargs):
        """Adiciona contexto adicional ao log."""
        self.logger.info(
            f"Context for {self.operation}",
            extra={
                "event_type": "operation_context",
                "operation": self.operation,
                "correlation_id": self.correlation_id,
                "context": kwargs,
                "timestamp": datetime.utcnow().isoformat()
            }
        )