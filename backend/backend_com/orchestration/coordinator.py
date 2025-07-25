"""
Coordenador base para orquestração de fluxos complexos.

Define interfaces comuns e funcionalidades básicas para
coordenação entre diferentes serviços e gateways.
"""

import time
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from ..gateways import PersistenceGateway
from ..utils.logging import setup_logger, RequestLogger


class OrchestrationStatus(str, Enum):
    """Status de operações de orquestração."""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PARTIAL_SUCCESS = "partial_success"


@dataclass
class OrchestrationResult:
    """
    Resultado padronizado para operações de orquestração.
    """
    success: bool
    status: OrchestrationStatus
    data: Optional[Dict[str, Any]] = None
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    metadata: Optional[Dict[str, Any]] = None
    duration_ms: Optional[float] = None
    steps_completed: int = 0
    total_steps: int = 0
    
    @classmethod
    def success_result(cls, data: Optional[Dict[str, Any]] = None,
                      metadata: Optional[Dict[str, Any]] = None,
                      duration_ms: Optional[float] = None,
                      steps_completed: int = 0,
                      total_steps: int = 0) -> 'OrchestrationResult':
        """Cria resultado de sucesso."""
        return cls(
            success=True,
            status=OrchestrationStatus.SUCCESS,
            data=data,
            metadata=metadata,
            duration_ms=duration_ms,
            steps_completed=steps_completed,
            total_steps=total_steps
        )
    
    @classmethod
    def error_result(cls, errors: Union[str, List[str]],
                    status: OrchestrationStatus = OrchestrationStatus.FAILED,
                    data: Optional[Dict[str, Any]] = None,
                    metadata: Optional[Dict[str, Any]] = None,
                    duration_ms: Optional[float] = None,
                    steps_completed: int = 0,
                    total_steps: int = 0) -> 'OrchestrationResult':
        """Cria resultado de erro."""
        if isinstance(errors, str):
            errors = [errors]
        
        return cls(
            success=False,
            status=status,
            data=data,
            errors=errors,
            metadata=metadata,
            duration_ms=duration_ms,
            steps_completed=steps_completed,
            total_steps=total_steps
        )
    
    @classmethod
    def partial_result(cls, data: Optional[Dict[str, Any]] = None,
                      errors: Optional[List[str]] = None,
                      warnings: Optional[List[str]] = None,
                      metadata: Optional[Dict[str, Any]] = None,
                      duration_ms: Optional[float] = None,
                      steps_completed: int = 0,
                      total_steps: int = 0) -> 'OrchestrationResult':
        """Cria resultado parcial (alguns passos falharam)."""
        return cls(
            success=True,
            status=OrchestrationStatus.PARTIAL_SUCCESS,
            data=data,
            errors=errors or [],
            warnings=warnings or [],
            metadata=metadata,
            duration_ms=duration_ms,
            steps_completed=steps_completed,
            total_steps=total_steps
        )


class OrchestrationError(Exception):
    """Erro específico de orquestração."""
    
    def __init__(self, message: str, step: Optional[str] = None,
                 details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.step = step
        self.details = details or {}
        self.timestamp = datetime.utcnow()


class Coordinator(ABC):
    """
    Classe base para coordenadores de orquestração.
    
    Providencia funcionalidades comuns para gerenciar fluxos
    complexos que envolvem múltiplos serviços.
    """
    
    def __init__(self, name: str):
        self.name = name
        self.logger = setup_logger(f"orchestration.{name}")
        self.persistence_gateway = PersistenceGateway()
        self._active_workflows: Dict[str, Dict[str, Any]] = {}
    
    @abstractmethod
    async def execute(self, *args, **kwargs) -> OrchestrationResult:
        """
        Executa o fluxo de orquestração.
        
        Returns:
            OrchestrationResult: Resultado da orquestração
        """
        pass
    
    async def _execute_step(self, step_name: str, step_function,
                           *args, **kwargs) -> Dict[str, Any]:
        """
        Executa um passo da orquestração com logging e tratamento de erro.
        
        Args:
            step_name: Nome do passo
            step_function: Função a ser executada
            *args: Argumentos posicionais
            **kwargs: Argumentos nomeados
            
        Returns:
            dict: Resultado do passo
            
        Raises:
            OrchestrationError: Se o passo falhar
        """
        self.logger.info(f"Starting step: {step_name}")
        start_time = time.time()
        
        try:
            result = await step_function(*args, **kwargs)
            duration_ms = (time.time() - start_time) * 1000
            
            self.logger.info(
                f"Step completed: {step_name}",
                extra={
                    "step": step_name,
                    "duration_ms": duration_ms,
                    "success": True
                }
            )
            
            return {
                "success": True,
                "data": result,
                "duration_ms": duration_ms,
                "step": step_name
            }
            
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            
            self.logger.error(
                f"Step failed: {step_name}",
                extra={
                    "step": step_name,
                    "duration_ms": duration_ms,
                    "error": str(e),
                    "success": False
                },
                exc_info=e
            )
            
            raise OrchestrationError(
                f"Step '{step_name}' failed: {str(e)}",
                step=step_name,
                details={"duration_ms": duration_ms}
            )
    
    async def _validate_input(self, data: Dict[str, Any],
                             required_fields: List[str]) -> OrchestrationResult:
        """
        Valida dados de entrada da orquestração.
        
        Args:
            data: Dados para validar
            required_fields: Campos obrigatórios
            
        Returns:
            OrchestrationResult: Resultado da validação
        """
        missing_fields = []
        
        for field in required_fields:
            if field not in data or data[field] is None:
                missing_fields.append(field)
        
        if missing_fields:
            return OrchestrationResult.error_result(
                f"Missing required fields: {', '.join(missing_fields)}"
            )
        
        return OrchestrationResult.success_result()
    
    async def _log_workflow_start(self, workflow_id: str, workflow_type: str,
                                 input_data: Dict[str, Any]) -> None:
        """
        Registra início de workflow para auditoria.
        
        Args:
            workflow_id: ID único do workflow
            workflow_type: Tipo do workflow
            input_data: Dados de entrada (sem informações sensíveis)
        """
        log_data = {
            "workflow_id": workflow_id,
            "workflow_type": workflow_type,
            "coordinator": self.name,
            "input_summary": self._sanitize_log_data(input_data),
            "status": "started"
        }
        
        await self.persistence_gateway.create_log_entry(log_data)
        
        self._active_workflows[workflow_id] = {
            "type": workflow_type,
            "start_time": time.time(),
            "status": OrchestrationStatus.RUNNING
        }
    
    async def _log_workflow_end(self, workflow_id: str,
                               result: OrchestrationResult) -> None:
        """
        Registra fim de workflow para auditoria.
        
        Args:
            workflow_id: ID do workflow
            result: Resultado final da orquestração
        """
        workflow_info = self._active_workflows.get(workflow_id, {})
        start_time = workflow_info.get("start_time", time.time())
        total_duration_ms = (time.time() - start_time) * 1000
        
        log_data = {
            "workflow_id": workflow_id,
            "workflow_type": workflow_info.get("type", "unknown"),
            "coordinator": self.name,
            "status": result.status.value,
            "success": result.success,
            "duration_ms": total_duration_ms,
            "steps_completed": result.steps_completed,
            "total_steps": result.total_steps,
            "errors": result.errors,
            "warnings": result.warnings
        }
        
        await self.persistence_gateway.create_log_entry(log_data)
        
        # Remove workflow dos ativos
        if workflow_id in self._active_workflows:
            del self._active_workflows[workflow_id]
    
    def _sanitize_log_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Remove informações sensíveis dos dados para logging.
        
        Args:
            data: Dados originais
            
        Returns:
            dict: Dados limpos para log
        """
        sensitive_fields = {
            'senha', 'password', 'token', 'secret', 'key',
            'auth', 'authorization', 'credential'
        }
        
        sanitized = {}
        
        for key, value in data.items():
            key_lower = key.lower()
            
            if any(sensitive in key_lower for sensitive in sensitive_fields):
                sanitized[key] = "[REDACTED]"
            elif isinstance(value, dict):
                sanitized[key] = self._sanitize_log_data(value)
            elif isinstance(value, list) and len(value) > 0:
                # Para listas, sanitiza apenas o primeiro elemento como exemplo
                if isinstance(value[0], dict):
                    sanitized[key] = [self._sanitize_log_data(value[0]), "..."]
                else:
                    sanitized[key] = f"[{len(value)} items]"
            else:
                sanitized[key] = value
        
        return sanitized
    
    async def _rollback_operation(self, operation_id: str,
                                 rollback_data: Dict[str, Any]) -> bool:
        """
        Executa rollback de uma operação.
        
        Args:
            operation_id: ID da operação
            rollback_data: Dados necessários para rollback
            
        Returns:
            bool: True se rollback foi bem-sucedido
        """
        try:
            self.logger.warning(
                f"Executing rollback for operation: {operation_id}",
                extra={
                    "operation_id": operation_id,
                    "rollback_data": self._sanitize_log_data(rollback_data)
                }
            )
            
            # Implementação específica deve ser feita nas subclasses
            success = await self._execute_rollback(operation_id, rollback_data)
            
            if success:
                self.logger.info(f"Rollback successful for operation: {operation_id}")
            else:
                self.logger.error(f"Rollback failed for operation: {operation_id}")
            
            return success
            
        except Exception as e:
            self.logger.error(
                f"Error during rollback for operation: {operation_id}",
                extra={"error": str(e)},
                exc_info=e
            )
            return False
    
    async def _execute_rollback(self, operation_id: str,
                               rollback_data: Dict[str, Any]) -> bool:
        """
        Implementação específica de rollback.
        
        Deve ser sobrescrita pelas subclasses conforme necessário.
        
        Args:
            operation_id: ID da operação
            rollback_data: Dados para rollback
            
        Returns:
            bool: True se bem-sucedido
        """
        # Implementação padrão - sem rollback específico
        return True
    
    async def get_workflow_status(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtém status de workflow ativo.
        
        Args:
            workflow_id: ID do workflow
            
        Returns:
            dict: Status do workflow ou None se não encontrado
        """
        if workflow_id not in self._active_workflows:
            return None
        
        workflow_info = self._active_workflows[workflow_id].copy()
        
        # Adiciona duração atual
        if "start_time" in workflow_info:
            workflow_info["current_duration_ms"] = (
                time.time() - workflow_info["start_time"]
            ) * 1000
        
        return workflow_info
    
    async def cancel_workflow(self, workflow_id: str) -> bool:
        """
        Cancela workflow ativo.
        
        Args:
            workflow_id: ID do workflow
            
        Returns:
            bool: True se cancelamento foi bem-sucedido
        """
        if workflow_id not in self._active_workflows:
            return False
        
        try:
            self._active_workflows[workflow_id]["status"] = OrchestrationStatus.CANCELLED
            
            self.logger.info(f"Workflow cancelled: {workflow_id}")
            
            # Log do cancelamento
            await self._log_workflow_end(
                workflow_id,
                OrchestrationResult.error_result(
                    "Workflow cancelled by user",
                    status=OrchestrationStatus.CANCELLED
                )
            )
            
            return True
            
        except Exception as e:
            self.logger.error(
                f"Error cancelling workflow: {workflow_id}",
                extra={"error": str(e)},
                exc_info=e
            )
            return False
    
    async def close(self) -> None:
        """
        Limpa recursos e fecha conexões.
        """
        await self.persistence_gateway.close()
        
        self.logger.info(f"Coordinator {self.name} closed")