"""
Engine de workflow para orquestração avançada.

Implementa sistema flexível de workflows que podem ser
definidos dinamicamente e executados de forma assíncrona.
"""

import asyncio
import time
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

from ..utils import generate_uuid
from ..utils.logging import setup_logger


class WorkflowState(str, Enum):
    """Estados possíveis de um workflow."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PAUSED = "paused"


class StepState(str, Enum):
    """Estados possíveis de um passo."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"
    RETRYING = "retrying"


@dataclass
class WorkflowStep:
    """
    Definição de um passo do workflow.
    """
    name: str
    function: Callable
    args: tuple = field(default_factory=tuple)
    kwargs: dict = field(default_factory=dict)
    retry_count: int = 0
    max_retries: int = 3
    timeout: Optional[int] = None
    depends_on: List[str] = field(default_factory=list)
    can_fail: bool = False  # Se True, falha não interrompe workflow
    condition: Optional[Callable] = None  # Condição para executar passo
    
    # Estados do passo
    state: StepState = StepState.PENDING
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    result: Optional[Any] = None
    error: Optional[str] = None


@dataclass
class WorkflowResult:
    """
    Resultado da execução de um workflow.
    """
    workflow_id: str
    state: WorkflowState
    steps_results: Dict[str, Any]
    total_steps: int
    completed_steps: int
    failed_steps: int
    skipped_steps: int
    start_time: float
    end_time: Optional[float] = None
    duration_ms: Optional[float] = None
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class WorkflowEngine:
    """
    Engine para execução de workflows complexos.
    
    Permite definir e executar workflows com dependências,
    retry automático, execução paralela e tratamento de erros.
    """
    
    def __init__(self, name: str = "workflow_engine"):
        self.name = name
        self.logger = setup_logger(f"workflow.{name}")
        self._active_workflows: Dict[str, WorkflowResult] = {}
        self._workflow_definitions: Dict[str, List[WorkflowStep]] = {}
    
    def define_workflow(self, workflow_name: str, steps: List[WorkflowStep]) -> None:
        """
        Define um workflow reutilizável.
        
        Args:
            workflow_name: Nome do workflow
            steps: Lista de passos do workflow
        """
        self._workflow_definitions[workflow_name] = steps
        self.logger.info(f"Workflow defined: {workflow_name} with {len(steps)} steps")
    
    async def execute_workflow(self, workflow_name: str, 
                             context: Optional[Dict[str, Any]] = None,
                             parallel_execution: bool = False) -> WorkflowResult:
        """
        Executa um workflow definido.
        
        Args:
            workflow_name: Nome do workflow
            context: Contexto/dados compartilhados entre passos
            parallel_execution: Se deve executar passos em paralelo quando possível
            
        Returns:
            WorkflowResult: Resultado da execução
        """
        if workflow_name not in self._workflow_definitions:
            raise ValueError(f"Workflow not defined: {workflow_name}")
        
        workflow_id = generate_uuid()
        steps = self._workflow_definitions[workflow_name].copy()
        
        return await self._execute_steps(
            workflow_id, steps, context or {}, parallel_execution
        )
    
    async def execute_ad_hoc_workflow(self, steps: List[WorkflowStep],
                                    context: Optional[Dict[str, Any]] = None,
                                    parallel_execution: bool = False) -> WorkflowResult:
        """
        Executa workflow ad-hoc (não definido previamente).
        
        Args:
            steps: Lista de passos para executar
            context: Contexto compartilhado
            parallel_execution: Execução paralela
            
        Returns:
            WorkflowResult: Resultado da execução
        """
        workflow_id = generate_uuid()
        
        return await self._execute_steps(
            workflow_id, steps, context or {}, parallel_execution
        )
    
    async def _execute_steps(self, workflow_id: str, steps: List[WorkflowStep],
                           context: Dict[str, Any], 
                           parallel_execution: bool) -> WorkflowResult:
        """
        Executa lista de passos do workflow.
        
        Args:
            workflow_id: ID único do workflow
            steps: Passos para executar
            context: Contexto compartilhado
            parallel_execution: Se deve executar em paralelo
            
        Returns:
            WorkflowResult: Resultado da execução
        """
        start_time = time.time()
        
        # Inicializa resultado do workflow
        workflow_result = WorkflowResult(
            workflow_id=workflow_id,
            state=WorkflowState.RUNNING,
            steps_results={},
            total_steps=len(steps),
            completed_steps=0,
            failed_steps=0,
            skipped_steps=0,
            start_time=start_time
        )
        
        self._active_workflows[workflow_id] = workflow_result
        
        self.logger.info(
            f"Starting workflow execution: {workflow_id}",
            extra={
                "workflow_id": workflow_id,
                "total_steps": len(steps),
                "parallel_execution": parallel_execution
            }
        )
        
        try:
            if parallel_execution:
                await self._execute_parallel(workflow_id, steps, context, workflow_result)
            else:
                await self._execute_sequential(workflow_id, steps, context, workflow_result)
            
            # Determina estado final
            if workflow_result.failed_steps > 0:
                # Verifica se todos os passos que falharam podem falhar
                critical_failures = any(
                    step.state == StepState.FAILED and not step.can_fail 
                    for step in steps
                )
                
                if critical_failures:
                    workflow_result.state = WorkflowState.FAILED
                else:
                    workflow_result.state = WorkflowState.COMPLETED
            else:
                workflow_result.state = WorkflowState.COMPLETED
            
        except Exception as e:
            workflow_result.state = WorkflowState.FAILED
            workflow_result.errors.append(str(e))
            
            self.logger.error(
                f"Workflow execution failed: {workflow_id}",
                extra={
                    "workflow_id": workflow_id,
                    "error": str(e)
                },
                exc_info=e
            )
        
        finally:
            # Finaliza workflow
            end_time = time.time()
            workflow_result.end_time = end_time
            workflow_result.duration_ms = (end_time - start_time) * 1000
            
            self.logger.info(
                f"Workflow execution finished: {workflow_id}",
                extra={
                    "workflow_id": workflow_id,
                    "state": workflow_result.state.value,
                    "duration_ms": workflow_result.duration_ms,
                    "completed_steps": workflow_result.completed_steps,
                    "failed_steps": workflow_result.failed_steps
                }
            )
            
            # Remove dos workflows ativos
            if workflow_id in self._active_workflows:
                del self._active_workflows[workflow_id]
        
        return workflow_result
    
    async def _execute_sequential(self, workflow_id: str, steps: List[WorkflowStep],
                                context: Dict[str, Any], 
                                workflow_result: WorkflowResult) -> None:
        """Executa passos sequencialmente."""
        for step in steps:
            if workflow_result.state == WorkflowState.CANCELLED:
                break
            
            await self._execute_single_step(step, context, workflow_result)
            
            # Para execução se passo crítico falhou
            if step.state == StepState.FAILED and not step.can_fail:
                break
    
    async def _execute_parallel(self, workflow_id: str, steps: List[WorkflowStep],
                              context: Dict[str, Any],
                              workflow_result: WorkflowResult) -> None:
        """Executa passos em paralelo respeitando dependências."""
        completed_steps = set()
        pending_steps = {step.name: step for step in steps}
        running_tasks = {}
        
        while pending_steps or running_tasks:
            if workflow_result.state == WorkflowState.CANCELLED:
                # Cancela todas as tasks em execução
                for task in running_tasks.values():
                    task.cancel()
                break
            
            # Inicia passos que podem ser executados
            ready_steps = self._get_ready_steps(pending_steps, completed_steps)
            
            for step_name in ready_steps:
                step = pending_steps.pop(step_name)
                
                # Cria task para execução assíncrona
                task = asyncio.create_task(
                    self._execute_single_step(step, context, workflow_result)
                )
                running_tasks[step_name] = task
            
            # Aguarda pelo menos uma task completar
            if running_tasks:
                done, pending = await asyncio.wait(
                    running_tasks.values(),
                    return_when=asyncio.FIRST_COMPLETED
                )
                
                # Processa tasks completadas
                for task in done:
                    # Encontra qual passo foi completado
                    for step_name, step_task in list(running_tasks.items()):
                        if step_task == task:
                            completed_steps.add(step_name)
                            del running_tasks[step_name]
                            break
            
            # Se não há mais passos prontos e nenhum executando, para
            if not ready_steps and not running_tasks:
                break
        
        # Aguarda tasks restantes
        if running_tasks:
            await asyncio.gather(*running_tasks.values(), return_exceptions=True)
    
    def _get_ready_steps(self, pending_steps: Dict[str, WorkflowStep],
                        completed_steps: set) -> List[str]:
        """
        Retorna lista de passos prontos para execução.
        
        Args:
            pending_steps: Passos pendentes
            completed_steps: Passos já completados
            
        Returns:
            List[str]: Nomes dos passos prontos
        """
        ready = []
        
        for step_name, step in pending_steps.items():
            # Verifica se todas as dependências foram completadas
            dependencies_met = all(
                dep in completed_steps for dep in step.depends_on
            )
            
            if dependencies_met:
                ready.append(step_name)
        
        return ready
    
    async def _execute_single_step(self, step: WorkflowStep, 
                                 context: Dict[str, Any],
                                 workflow_result: WorkflowResult) -> None:
        """
        Executa um único passo do workflow.
        
        Args:
            step: Passo para executar
            context: Contexto compartilhado
            workflow_result: Resultado do workflow
        """
        # Verifica condição se definida
        if step.condition and not await self._evaluate_condition(step.condition, context):
            step.state = StepState.SKIPPED
            workflow_result.skipped_steps += 1
            workflow_result.steps_results[step.name] = {"skipped": True, "reason": "condition_not_met"}
            return
        
        step.state = StepState.RUNNING
        step.start_time = time.time()
        
        self.logger.info(f"Executing step: {step.name}")
        
        for attempt in range(step.max_retries + 1):
            try:
                if step.timeout:
                    # Executa com timeout
                    result = await asyncio.wait_for(
                        step.function(*step.args, **step.kwargs, context=context),
                        timeout=step.timeout
                    )
                else:
                    # Executa sem timeout
                    result = await step.function(*step.args, **step.kwargs, context=context)
                
                # Sucesso
                step.state = StepState.COMPLETED
                step.result = result
                step.end_time = time.time()
                
                workflow_result.completed_steps += 1
                workflow_result.steps_results[step.name] = {
                    "success": True,
                    "result": result,
                    "duration_ms": (step.end_time - step.start_time) * 1000,
                    "attempts": attempt + 1
                }
                
                self.logger.info(
                    f"Step completed: {step.name}",
                    extra={
                        "step": step.name,
                        "duration_ms": (step.end_time - step.start_time) * 1000,
                        "attempts": attempt + 1
                    }
                )
                
                return
                
            except asyncio.TimeoutError:
                error_msg = f"Step {step.name} timed out after {step.timeout}s"
                step.error = error_msg
                
                if attempt < step.max_retries:
                    step.state = StepState.RETRYING
                    step.retry_count += 1
                    
                    self.logger.warning(
                        f"Step timeout, retrying: {step.name}",
                        extra={
                            "step": step.name,
                            "attempt": attempt + 1,
                            "max_retries": step.max_retries
                        }
                    )
                    
                    # Aguarda antes do retry
                    await asyncio.sleep(2 ** attempt)  # Backoff exponencial
                else:
                    # Esgotou tentativas
                    step.state = StepState.FAILED
                    step.end_time = time.time()
                    
                    workflow_result.failed_steps += 1
                    workflow_result.errors.append(error_msg)
                    workflow_result.steps_results[step.name] = {
                        "success": False,
                        "error": error_msg,
                        "attempts": attempt + 1
                    }
                    
                    self.logger.error(f"Step failed after {attempt + 1} attempts: {step.name}")
                    break
                    
            except Exception as e:
                error_msg = f"Step {step.name} failed: {str(e)}"
                step.error = error_msg
                
                if attempt < step.max_retries:
                    step.state = StepState.RETRYING
                    step.retry_count += 1
                    
                    self.logger.warning(
                        f"Step failed, retrying: {step.name}",
                        extra={
                            "step": step.name,
                            "error": str(e),
                            "attempt": attempt + 1,
                            "max_retries": step.max_retries
                        }
                    )
                    
                    await asyncio.sleep(2 ** attempt)
                else:
                    # Esgotou tentativas
                    step.state = StepState.FAILED
                    step.end_time = time.time()
                    
                    workflow_result.failed_steps += 1
                    workflow_result.errors.append(error_msg)
                    workflow_result.steps_results[step.name] = {
                        "success": False,
                        "error": error_msg,
                        "attempts": attempt + 1
                    }
                    
                    self.logger.error(
                        f"Step failed after {attempt + 1} attempts: {step.name}",
                        exc_info=e
                    )
                    break
    
    async def _evaluate_condition(self, condition: Callable, 
                                context: Dict[str, Any]) -> bool:
        """
        Avalia condição para execução de passo.
        
        Args:
            condition: Função de condição
            context: Contexto do workflow
            
        Returns:
            bool: True se condição for atendida
        """
        try:
            if asyncio.iscoroutinefunction(condition):
                return await condition(context)
            else:
                return condition(context)
        except Exception as e:
            self.logger.warning(f"Error evaluating condition: {str(e)}")
            return False
    
    def get_workflow_status(self, workflow_id: str) -> Optional[WorkflowResult]:
        """
        Obtém status de workflow ativo.
        
        Args:
            workflow_id: ID do workflow
            
        Returns:
            WorkflowResult: Status atual ou None se não encontrado
        """
        return self._active_workflows.get(workflow_id)
    
    def cancel_workflow(self, workflow_id: str) -> bool:
        """
        Cancela workflow em execução.
        
        Args:
            workflow_id: ID do workflow
            
        Returns:
            bool: True se cancelamento foi bem-sucedido
        """
        if workflow_id not in self._active_workflows:
            return False
        
        workflow_result = self._active_workflows[workflow_id]
        workflow_result.state = WorkflowState.CANCELLED
        
        self.logger.info(f"Workflow cancelled: {workflow_id}")
        return True
    
    def pause_workflow(self, workflow_id: str) -> bool:
        """
        Pausa workflow em execução.
        
        Args:
            workflow_id: ID do workflow
            
        Returns:
            bool: True se pausa foi bem-sucedida
        """
        if workflow_id not in self._active_workflows:
            return False
        
        workflow_result = self._active_workflows[workflow_id]
        
        if workflow_result.state == WorkflowState.RUNNING:
            workflow_result.state = WorkflowState.PAUSED
            self.logger.info(f"Workflow paused: {workflow_id}")
            return True
        
        return False
    
    def resume_workflow(self, workflow_id: str) -> bool:
        """
        Resume workflow pausado.
        
        Args:
            workflow_id: ID do workflow
            
        Returns:
            bool: True se resume foi bem-sucedido
        """
        if workflow_id not in self._active_workflows:
            return False
        
        workflow_result = self._active_workflows[workflow_id]
        
        if workflow_result.state == WorkflowState.PAUSED:
            workflow_result.state = WorkflowState.RUNNING
            self.logger.info(f"Workflow resumed: {workflow_id}")
            return True
        
        return False
    
    def list_active_workflows(self) -> List[str]:
        """
        Lista workflows atualmente ativos.
        
        Returns:
            List[str]: Lista de IDs de workflows ativos
        """
        return list(self._active_workflows.keys())
    
    def list_defined_workflows(self) -> List[str]:
        """
        Lista workflows definidos no engine.
        
        Returns:
            List[str]: Lista de nomes de workflows definidos
        """
        return list(self._workflow_definitions.keys())
    
    async def cleanup_completed_workflows(self, max_age_hours: int = 24) -> int:
        """
        Remove workflows completados antigos da memória.
        
        Args:
            max_age_hours: Idade máxima em horas para manter workflows
            
        Returns:
            int: Número de workflows removidos
        """
        current_time = time.time()
        cutoff_time = current_time - (max_age_hours * 3600)
        
        workflows_to_remove = []
        
        for workflow_id, result in self._active_workflows.items():
            if (result.state in [WorkflowState.COMPLETED, WorkflowState.FAILED, WorkflowState.CANCELLED] 
                and result.end_time and result.end_time < cutoff_time):
                workflows_to_remove.append(workflow_id)
        
        for workflow_id in workflows_to_remove:
            del self._active_workflows[workflow_id]
        
        if workflows_to_remove:
            self.logger.info(f"Cleaned up {len(workflows_to_remove)} old workflows")
        
        return len(workflows_to_remove)


# === FUNÇÕES UTILITÁRIAS PARA CRIAÇÃO DE WORKFLOWS ===

def create_simple_step(name: str, function: Callable, *args, **kwargs) -> WorkflowStep:
    """
    Cria passo simples de workflow.
    
    Args:
        name: Nome do passo
        function: Função para executar
        *args: Argumentos posicionais
        **kwargs: Argumentos nomeados
        
    Returns:
        WorkflowStep: Passo configurado
    """
    return WorkflowStep(name=name, function=function, args=args, kwargs=kwargs)


def create_conditional_step(name: str, function: Callable, condition: Callable,
                          *args, **kwargs) -> WorkflowStep:
    """
    Cria passo condicional de workflow.
    
    Args:
        name: Nome do passo
        function: Função para executar
        condition: Condição para execução
        *args: Argumentos posicionais
        **kwargs: Argumentos nomeados
        
    Returns:
        WorkflowStep: Passo condicional configurado
    """
    return WorkflowStep(
        name=name, 
        function=function, 
        condition=condition,
        args=args, 
        kwargs=kwargs
    )


def create_retry_step(name: str, function: Callable, max_retries: int = 3,
                     timeout: Optional[int] = None, *args, **kwargs) -> WorkflowStep:
    """
    Cria passo com retry automático.
    
    Args:
        name: Nome do passo
        function: Função para executar
        max_retries: Número máximo de tentativas
        timeout: Timeout em segundos
        *args: Argumentos posicionais
        **kwargs: Argumentos nomeados
        
    Returns:
        WorkflowStep: Passo com retry configurado
    """
    return WorkflowStep(
        name=name,
        function=function,
        max_retries=max_retries,
        timeout=timeout,
        args=args,
        kwargs=kwargs
    )


def create_dependent_step(name: str, function: Callable, depends_on: List[str],
                         *args, **kwargs) -> WorkflowStep:
    """
    Cria passo com dependências.
    
    Args:
        name: Nome do passo
        function: Função para executar
        depends_on: Lista de passos dos quais depende
        *args: Argumentos posicionais
        **kwargs: Argumentos nomeados
        
    Returns:
        WorkflowStep: Passo com dependências configurado
    """
    return WorkflowStep(
        name=name,
        function=function,
        depends_on=depends_on,
        args=args,
        kwargs=kwargs
    )


def create_optional_step(name: str, function: Callable, can_fail: bool = True,
                        *args, **kwargs) -> WorkflowStep:
    """
    Cria passo opcional (que pode falhar sem interromper workflow).
    
    Args:
        name: Nome do passo
        function: Função para executar
        can_fail: Se pode falhar sem interromper workflow
        *args: Argumentos posicionais
        **kwargs: Argumentos nomeados
        
    Returns:
        WorkflowStep: Passo opcional configurado
    """
    return WorkflowStep(
        name=name,
        function=function,
        can_fail=can_fail,
        args=args,
        kwargs=kwargs
    )


# === EXEMPLOS DE USO ===

async def example_workflow_usage():
    """
    Exemplo de como usar o WorkflowEngine.
    """
    
    # Cria engine
    engine = WorkflowEngine("example_engine")
    
    # Funções exemplo
    async def step1(context):
        context["step1_result"] = "completed"
        return "Step 1 done"
    
    async def step2(context):
        if "step1_result" not in context:
            raise ValueError("Step 1 not completed")
        context["step2_result"] = "completed"
        return "Step 2 done"
    
    async def step3(context):
        return f"Final result: {context.get('step2_result', 'unknown')}"
    
    def condition_check(context):
        return context.get("step1_result") == "completed"
    
    # Define workflow
    steps = [
        create_simple_step("step1", step1),
        create_conditional_step("step2", step2, condition_check),
        create_dependent_step("step3", step3, ["step1", "step2"])
    ]
    
    engine.define_workflow("example_workflow", steps)
    
    # Executa workflow
    result = await engine.execute_workflow("example_workflow")
    
    print(f"Workflow completed: {result.state}")
    print(f"Steps results: {result.steps_results}")
    
    return result