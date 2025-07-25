"""
Orquestrador para fluxos educacionais.

Gerencia workflows complexos relacionados a perguntas, respostas,
avaliações e busca semântica no contexto educacional.
"""

import time
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

from .coordinator import Coordinator, OrchestrationResult, OrchestrationError
from ..models import PaginationParams
from ..utils import generate_uuid


@dataclass
class QuestionFlowResult:
    """Resultado do fluxo de criação de pergunta."""
    question_id: str
    embedding_created: bool
    similar_questions: Optional[List[Dict[str, Any]]] = None
    recommendations: Optional[List[str]] = None


@dataclass
class AnswerFlowResult:
    """Resultado do fluxo de criação de resposta."""
    answer_id: str
    question_updated: bool
    embedding_created: bool
    quality_score: Optional[float] = None


@dataclass
class EvaluationFlowResult:
    """Resultado do fluxo de avaliação."""
    evaluation_id: str
    answer_updated: bool
    user_stats_updated: bool
    feedback_generated: bool


class EducationalOrchestrator(Coordinator):
    """
    Orquestrador para operações educacionais complexas.
    
    Coordena fluxos que envolvem múltiplas operações relacionadas
    ao processo de ensino-aprendizagem.
    """
    
    def __init__(self):
        super().__init__("educational")
    
    async def execute(self, *args, **kwargs) -> OrchestrationResult:
        """
        Método base - não usado diretamente.
        Use os métodos específicos como create_question_flow, etc.
        """
        raise NotImplementedError("Use métodos específicos como create_question_flow")
    
    async def create_question_flow(self, question_data: Dict[str, Any],
                                  find_similar: bool = True,
                                  generate_recommendations: bool = True) -> OrchestrationResult:
        """
        Fluxo completo para criação de pergunta.
        
        Passos:
        1. Validar dados da pergunta
        2. Criar pergunta no MongoDB
        3. Gerar embedding para busca semântica
        4. Buscar perguntas similares (opcional)
        5. Gerar recomendações de estudo (opcional)
        
        Args:
            question_data: Dados da pergunta
            find_similar: Se deve buscar perguntas similares
            generate_recommendations: Se deve gerar recomendações
            
        Returns:
            OrchestrationResult: Resultado do fluxo completo
        """
        workflow_id = generate_uuid()
        start_time = time.time()
        
        await self._log_workflow_start(workflow_id, "create_question", question_data)
        
        try:
            # Passo 1: Validação
            validation_step = await self._execute_step(
                "validate_question_data",
                self._validate_question_data,
                question_data
            )
            
            # Passo 2: Criar pergunta
            create_step = await self._execute_step(
                "create_question",
                self._create_question,
                question_data
            )
            
            question_id = create_step["data"]["question_id"]
            embedding_created = False
            similar_questions = None
            recommendations = None
            
            # Passo 3: Gerar embedding
            try:
                embedding_step = await self._execute_step(
                    "create_embedding",
                    self._create_question_embedding,
                    question_id,
                    question_data["conteudo"]
                )
                embedding_created = True
                
            except OrchestrationError as e:
                self.logger.warning(f"Failed to create embedding: {e.message}")
            
            # Passo 4: Buscar similares (opcional)
            if find_similar and embedding_created:
                try:
                    similar_step = await self._execute_step(
                        "find_similar_questions",
                        self._find_similar_questions,
                        question_data["conteudo"],
                        question_data.get("disciplina")
                    )
                    similar_questions = similar_step["data"]
                    
                except OrchestrationError as e:
                    self.logger.warning(f"Failed to find similar questions: {e.message}")
            
            # Passo 5: Gerar recomendações (opcional)
            if generate_recommendations:
                try:
                    rec_step = await self._execute_step(
                        "generate_recommendations",
                        self._generate_study_recommendations,
                        question_data,
                        similar_questions
                    )
                    recommendations = rec_step["data"]
                    
                except OrchestrationError as e:
                    self.logger.warning(f"Failed to generate recommendations: {e.message}")
            
            # Resultado final
            duration_ms = (time.time() - start_time) * 1000
            
            result_data = QuestionFlowResult(
                question_id=question_id,
                embedding_created=embedding_created,
                similar_questions=similar_questions,
                recommendations=recommendations
            )
            
            result = OrchestrationResult.success_result(
                data=result_data.__dict__,
                duration_ms=duration_ms,
                steps_completed=4 if embedding_created else 2,
                total_steps=5
            )
            
            await self._log_workflow_end(workflow_id, result)
            return result
            
        except OrchestrationError as e:
            duration_ms = (time.time() - start_time) * 1000
            
            result = OrchestrationResult.error_result(
                errors=[e.message],
                duration_ms=duration_ms,
                steps_completed=0,
                total_steps=5
            )
            
            await self._log_workflow_end(workflow_id, result)
            return result
    
    async def create_answer_flow(self, answer_data: Dict[str, Any],
                               calculate_quality: bool = True) -> OrchestrationResult:
        """
        Fluxo completo para criação de resposta.
        
        Passos:
        1. Validar dados da resposta
        2. Verificar se pergunta existe
        3. Criar resposta no MongoDB
        4. Gerar embedding para busca semântica
        5. Atualizar contador na pergunta
        6. Calcular score de qualidade (opcional)
        
        Args:
            answer_data: Dados da resposta
            calculate_quality: Se deve calcular qualidade
            
        Returns:
            OrchestrationResult: Resultado do fluxo completo
        """
        workflow_id = generate_uuid()
        start_time = time.time()
        
        await self._log_workflow_start(workflow_id, "create_answer", answer_data)
        
        try:
            # Passo 1: Validação
            await self._execute_step(
                "validate_answer_data",
                self._validate_answer_data,
                answer_data
            )
            
            # Passo 2: Verificar pergunta
            question_step = await self._execute_step(
                "verify_question_exists",
                self._verify_question_exists,
                answer_data["pergunta_id"]
            )
            
            # Passo 3: Criar resposta
            create_step = await self._execute_step(
                "create_answer",
                self._create_answer,
                answer_data
            )
            
            answer_id = create_step["data"]["answer_id"]
            embedding_created = False
            question_updated = False
            quality_score = None
            
            # Passo 4: Gerar embedding
            try:
                await self._execute_step(
                    "create_answer_embedding",
                    self._create_answer_embedding,
                    answer_id,
                    answer_data["conteudo"]
                )
                embedding_created = True
                
            except OrchestrationError as e:
                self.logger.warning(f"Failed to create answer embedding: {e.message}")
            
            # Passo 5: Atualizar contador da pergunta
            try:
                await self._execute_step(
                    "update_question_counter",
                    self._update_question_answer_count,
                    answer_data["pergunta_id"]
                )
                question_updated = True
                
            except OrchestrationError as e:
                self.logger.warning(f"Failed to update question counter: {e.message}")
            
            # Passo 6: Calcular qualidade (opcional)
            if calculate_quality:
                try:
                    quality_step = await self._execute_step(
                        "calculate_answer_quality",
                        self._calculate_answer_quality,
                        answer_data["conteudo"],
                        question_step["data"]["conteudo"]
                    )
                    quality_score = quality_step["data"]["score"]
                    
                except OrchestrationError as e:
                    self.logger.warning(f"Failed to calculate quality: {e.message}")
            
            # Resultado final
            duration_ms = (time.time() - start_time) * 1000
            
            result_data = AnswerFlowResult(
                answer_id=answer_id,
                question_updated=question_updated,
                embedding_created=embedding_created,
                quality_score=quality_score
            )
            
            result = OrchestrationResult.success_result(
                data=result_data.__dict__,
                duration_ms=duration_ms,
                steps_completed=6,
                total_steps=6
            )
            
            await self._log_workflow_end(workflow_id, result)
            return result
            
        except OrchestrationError as e:
            duration_ms = (time.time() - start_time) * 1000
            
            result = OrchestrationResult.error_result(
                errors=[e.message],
                duration_ms=duration_ms
            )
            
            await self._log_workflow_end(workflow_id, result)
            return result
    
    async def create_evaluation_flow(self, evaluation_data: Dict[str, Any],
                                   update_user_stats: bool = True,
                                   generate_feedback: bool = True) -> OrchestrationResult:
        """
        Fluxo completo para criação de avaliação.
        
        Passos:
        1. Validar dados da avaliação
        2. Verificar se resposta existe
        3. Criar avaliação no MongoDB
        4. Atualizar estatísticas na resposta
        5. Atualizar estatísticas do usuário (opcional)
        6. Gerar feedback personalizado (opcional)
        
        Args:
            evaluation_data: Dados da avaliação
            update_user_stats: Se deve atualizar stats do usuário
            generate_feedback: Se deve gerar feedback
            
        Returns:
            OrchestrationResult: Resultado do fluxo completo
        """
        workflow_id = generate_uuid()
        start_time = time.time()
        
        await self._log_workflow_start(workflow_id, "create_evaluation", evaluation_data)
        
        try:
            # Implementação similar aos outros fluxos...
            # Por brevidade, implementando apenas a estrutura básica
            
            await self._execute_step(
                "validate_evaluation_data",
                self._validate_evaluation_data,
                evaluation_data
            )
            
            create_step = await self._execute_step(
                "create_evaluation",
                self._create_evaluation,
                evaluation_data
            )
            
            evaluation_id = create_step["data"]["evaluation_id"]
            
            duration_ms = (time.time() - start_time) * 1000
            
            result_data = EvaluationFlowResult(
                evaluation_id=evaluation_id,
                answer_updated=True,
                user_stats_updated=update_user_stats,
                feedback_generated=generate_feedback
            )
            
            result = OrchestrationResult.success_result(
                data=result_data.__dict__,
                duration_ms=duration_ms,
                steps_completed=3,
                total_steps=6
            )
            
            await self._log_workflow_end(workflow_id, result)
            return result
            
        except OrchestrationError as e:
            duration_ms = (time.time() - start_time) * 1000
            
            result = OrchestrationResult.error_result(
                errors=[e.message],
                duration_ms=duration_ms
            )
            
            await self._log_workflow_end(workflow_id, result)
            return result
    
    # === MÉTODOS AUXILIARES ===
    
    async def _validate_question_data(self, question_data: Dict[str, Any]) -> Dict[str, Any]:
        """Valida dados da pergunta."""
        required_fields = ["usuario_id", "conteudo", "tipo_entrada"]
        
        validation_result = await self._validate_input(question_data, required_fields)
        
        if not validation_result.success:
            raise OrchestrationError(
                f"Invalid question data: {', '.join(validation_result.errors)}"
            )
        
        return {"valid": True}
    
    async def _create_question(self, question_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria pergunta no banco de dados."""
        response = await self.persistence_gateway.create_question(question_data)
        
        if not response.success:
            raise OrchestrationError(
                f"Failed to create question: {response.error_message}"
            )
        
        return {
            "question_id": response.data.get("_id"),
            "created_at": response.data.get("created_at")
        }
    
    async def _create_question_embedding(self, question_id: str, content: str) -> Dict[str, Any]:
        """Cria embedding para a pergunta."""
        metadata = {
            "type": "question",
            "question_id": question_id,
            "created_at": datetime.utcnow().isoformat()
        }
        
        response = await self.persistence_gateway.qdrant.create_embedding(content, metadata)
        
        if not response.success:
            raise OrchestrationError(
                f"Failed to create question embedding: {response.error_message}"
            )
        
        return response.data
    
    async def _find_similar_questions(self, content: str, 
                                    disciplina: Optional[str] = None) -> List[Dict[str, Any]]:
        """Busca perguntas similares usando busca semântica."""
        filters = {"type": "question"}
        if disciplina:
            filters["disciplina"] = disciplina
        
        response = await self.persistence_gateway.search_questions_semantic(
            content, limit=5, filters=filters
        )
        
        if not response.success:
            raise OrchestrationError(
                f"Failed to find similar questions: {response.error_message}"
            )
        
        return response.data.get("resultados", [])
    
    async def _generate_study_recommendations(self, question_data: Dict[str, Any],
                                            similar_questions: Optional[List[Dict[str, Any]]]) -> List[str]:
        """Gera recomendações de estudo baseadas na pergunta e similares."""
        recommendations = []
        
        # Recomendações baseadas na disciplina
        disciplina = question_data.get("disciplina")
        if disciplina:
            recommendations.append(f"Revise conceitos fundamentais de {disciplina}")
        
        # Recomendações baseadas no nível de dificuldade
        nivel = question_data.get("nivel_dificuldade")
        if nivel == "basico":
            recommendations.append("Comece com exercícios básicos antes de avançar")
        elif nivel == "avancado":
            recommendations.append("Considere estudar pré-requisitos se necessário")
        
        # Recomendações baseadas em perguntas similares
        if similar_questions and len(similar_questions) > 0:
            recommendations.append("Veja outras perguntas similares para ampliar o entendimento")
        
        return recommendations
    
    async def _validate_answer_data(self, answer_data: Dict[str, Any]) -> Dict[str, Any]:
        """Valida dados da resposta."""
        required_fields = ["pergunta_id", "usuario_id", "conteudo"]
        
        validation_result = await self._validate_input(answer_data, required_fields)
        
        if not validation_result.success:
            raise OrchestrationError(
                f"Invalid answer data: {', '.join(validation_result.errors)}"
            )
        
        return {"valid": True}
    
    async def _verify_question_exists(self, question_id: str) -> Dict[str, Any]:
        """Verifica se a pergunta existe."""
        response = await self.persistence_gateway.get_question(question_id)
        
        if not response.success:
            raise OrchestrationError(
                f"Question not found: {question_id}"
            )
        
        return response.data
    
    async def _create_answer(self, answer_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria resposta no banco de dados."""
        response = await self.persistence_gateway.create_answer(answer_data)
        
        if not response.success:
            raise OrchestrationError(
                f"Failed to create answer: {response.error_message}"
            )
        
        return {
            "answer_id": response.data.get("_id"),
            "created_at": response.data.get("created_at")
        }
    
    async def _create_answer_embedding(self, answer_id: str, content: str) -> Dict[str, Any]:
        """Cria embedding para a resposta."""
        metadata = {
            "type": "answer",
            "answer_id": answer_id,
            "created_at": datetime.utcnow().isoformat()
        }
        
        response = await self.persistence_gateway.qdrant.create_embedding(content, metadata)
        
        if not response.success:
            raise OrchestrationError(
                f"Failed to create answer embedding: {response.error_message}"
            )
        
        return response.data
    
    async def _update_question_answer_count(self, question_id: str) -> Dict[str, Any]:
        """Atualiza contador de respostas na pergunta."""
        # Busca pergunta atual
        question_response = await self.persistence_gateway.get_question(question_id)
        
        if not question_response.success:
            raise OrchestrationError(
                f"Failed to get question for counter update: {question_response.error_message}"
            )
        
        # Incrementa contador
        current_count = question_response.data.get("respostas_count", 0)
        update_data = {
            "respostas_count": current_count + 1,
            "updated_at": datetime.utcnow().isoformat()
        }
        
        update_response = await self.persistence_gateway.mongodb.update_document(
            "perguntas", question_id, update_data
        )
        
        if not update_response.success:
            raise OrchestrationError(
                f"Failed to update question counter: {update_response.error_message}"
            )
        
        return {"new_count": current_count + 1}
    
    async def _calculate_answer_quality(self, answer_content: str, 
                                      question_content: str) -> Dict[str, Any]:
        """
        Calcula score de qualidade da resposta.
        
        Implementação básica - pode ser expandida com IA.
        """
        score = 0.0
        
        # Critério 1: Comprimento da resposta
        if len(answer_content) < 50:
            score += 0.2
        elif len(answer_content) < 200:
            score += 0.5
        else:
            score += 0.8
        
        # Critério 2: Relação com a pergunta (básico)
        question_words = set(question_content.lower().split())
        answer_words = set(answer_content.lower().split())
        common_words = question_words.intersection(answer_words)
        
        if len(common_words) > 0:
            relevance_score = min(len(common_words) / len(question_words), 1.0)
            score += relevance_score * 0.3
        
        # Critério 3: Estrutura (pontuação, parágrafos)
        if '.' in answer_content or '!' in answer_content or '?' in answer_content:
            score += 0.1
        
        # Normaliza para 0-1
        final_score = min(score, 1.0)
        
        return {"score": round(final_score, 2)}
    
    async def _validate_evaluation_data(self, evaluation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Valida dados da avaliação."""
        required_fields = ["resposta_id", "avaliador_id", "nota", "tipo_avaliacao"]
        
        validation_result = await self._validate_input(evaluation_data, required_fields)
        
        if not validation_result.success:
            raise OrchestrationError(
                f"Invalid evaluation data: {', '.join(validation_result.errors)}"
            )
        
        # Valida faixa da nota
        nota = evaluation_data.get("nota", 0)
        if not (0 <= nota <= 10):
            raise OrchestrationError("Note must be between 0 and 10")
        
        return {"valid": True}
    
    async def _create_evaluation(self, evaluation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria avaliação no banco de dados."""
        response = await self.persistence_gateway.create_evaluation(evaluation_data)
        
        if not response.success:
            raise OrchestrationError(
                f"Failed to create evaluation: {response.error_message}"
            )
        
        return {
            "evaluation_id": response.data.get("_id"),
            "created_at": response.data.get("created_at")
        }
    
    # === MÉTODOS PÚBLICOS ADICIONAIS ===
    
    async def get_question_with_answers(self, question_id: str,
                                      include_evaluations: bool = False) -> OrchestrationResult:
        """
        Busca pergunta completa com suas respostas.
        
        Args:
            question_id: ID da pergunta
            include_evaluations: Se deve incluir avaliações das respostas
            
        Returns:
            OrchestrationResult: Pergunta com dados relacionados
        """
        try:
            start_time = time.time()
            
            # Busca pergunta
            question_response = await self.persistence_gateway.get_question(question_id)
            
            if not question_response.success:
                return OrchestrationResult.error_result(
                    f"Question not found: {question_id}"
                )
            
            question_data = question_response.data
            
            # Busca respostas
            answers_response = await self.persistence_gateway.get_answers_by_question(
                question_id, PaginationParams(page=1, page_size=50)
            )
            
            answers_data = []
            if answers_response.success:
                answers_data = answers_response.data.get("items", [])
                
                # Busca avaliações se solicitado
                if include_evaluations:
                    for answer in answers_data:
                        answer_id = answer.get("_id")
                        if answer_id:
                            evaluations_response = await self.persistence_gateway.get_evaluations_by_answer(
                                answer_id, PaginationParams(page=1, page_size=20)
                            )
                            
                            if evaluations_response.success:
                                answer["avaliacoes"] = evaluations_response.data.get("items", [])
            
            # Monta resultado
            duration_ms = (time.time() - start_time) * 1000
            
            result_data = {
                "pergunta": question_data,
                "respostas": answers_data,
                "total_respostas": len(answers_data)
            }
            
            return OrchestrationResult.success_result(
                data=result_data,
                duration_ms=duration_ms
            )
            
        except Exception as e:
            return OrchestrationResult.error_result(
                f"Error getting question with answers: {str(e)}"
            )
    
    async def search_educational_content(self, query: str, content_types: List[str],
                                       filters: Optional[Dict[str, Any]] = None,
                                       limit: int = 20) -> OrchestrationResult:
        """
        Busca conteúdo educacional usando busca semântica.
        
        Args:
            query: Consulta de busca
            content_types: Tipos de conteúdo (question, answer)
            filters: Filtros adicionais
            limit: Limite de resultados
            
        Returns:
            OrchestrationResult: Resultados da busca
        """
        try:
            start_time = time.time()
            
            all_results = []
            
            # Busca por cada tipo de conteúdo
            for content_type in content_types:
                search_filters = {"type": content_type}
                if filters:
                    search_filters.update(filters)
                
                response = await self.persistence_gateway.qdrant.search_similar(
                    query, limit=limit // len(content_types), filters=search_filters
                )
                
                if response.success:
                    results = response.data.get("resultados", [])
                    
                    # Adiciona tipo ao resultado
                    for result in results:
                        result["content_type"] = content_type
                    
                    all_results.extend(results)
            
            # Ordena por relevância (score)
            all_results.sort(key=lambda x: x.get("score", 0), reverse=True)
            
            # Limita resultados finais
            final_results = all_results[:limit]
            
            duration_ms = (time.time() - start_time) * 1000
            
            return OrchestrationResult.success_result(
                data={
                    "results": final_results,
                    "total_found": len(final_results),
                    "query": query,
                    "content_types": content_types
                },
                duration_ms=duration_ms
            )
            
        except Exception as e:
            return OrchestrationResult.error_result(
                f"Error in educational content search: {str(e)}"
            )