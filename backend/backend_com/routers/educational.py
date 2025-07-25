"""
Endpoints educacionais para perguntas, respostas e avaliações.

Gerencia todo o fluxo educacional: criação de perguntas,
respostas, avaliações e busca semântica de conteúdo.
"""

from fastapi import APIRouter, HTTPException, Depends, Query, status
from typing import Dict, Any, Optional, List

from ..models import (
    PerguntaRequest,
    PerguntaResponse,
    RespostaRequest, 
    RespostaResponse,
    AvaliacaoRequest,
    AvaliacaoResponse,
    BuscaSemanticaRequest,
    BuscaSemanticaResponse,
    PaginationParams,
    PaginatedResponse,
    SuccessResponse,
    ErrorResponse
)
from ..orchestration import EducationalOrchestrator
from ..routers.auth import get_current_user_dependency
from ..utils.logging import setup_logger, RequestLogger

# Configuração do router
router = APIRouter(
    prefix="/educational",
    tags=["Educational"],
    dependencies=[Depends(get_current_user_dependency)],
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        404: {"model": ErrorResponse, "description": "Not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)

# Logger específico para endpoints educacionais
logger = setup_logger("educational_router")


# === ENDPOINTS DE PERGUNTAS ===

@router.post(
    "/questions",
    response_model=PerguntaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar Pergunta",
    description="Cria nova pergunta com embedding automático e busca por similares"
)
async def create_question(
    question_data: PerguntaRequest,
    find_similar: bool = Query(True, description="Buscar perguntas similares"),
    generate_recommendations: bool = Query(True, description="Gerar recomendações de estudo"),
    current_user: Dict[str, Any] = Depends(get_current_user_dependency)
):
    """
    Cria uma nova pergunta no sistema.
    
    Este endpoint executa o fluxo completo:
    - Valida dados da pergunta
    - Cria pergunta no MongoDB
    - Gera embedding para busca semântica
    - Busca perguntas similares (opcional)
    - Gera recomendações de estudo (opcional)
    
    Args:
        question_data: Dados da pergunta
        find_similar: Se deve buscar perguntas similares
        generate_recommendations: Se deve gerar recomendações
        current_user: Usuário autenticado
        
    Returns:
        PerguntaResponse: Pergunta criada com dados adicionais
        
    Raises:
        HTTPException: Se dados inválidos ou erro interno
    """
    async with RequestLogger("create_question") as req_logger:
        try:
            # Adiciona user_id aos dados da pergunta
            question_dict = question_data.model_dump()
            question_dict["usuario_id"] = current_user["id"]
            
            req_logger.add_context(
                user_id=current_user["id"],
                tipo_entrada=question_dict.get("tipo_entrada"),
                disciplina=question_dict.get("disciplina"),
                find_similar=find_similar,
                generate_recommendations=generate_recommendations
            )
            
            educational_orchestrator = EducationalOrchestrator()
            
            # Executa fluxo de criação de pergunta
            result = await educational_orchestrator.create_question_flow(
                question_data=question_dict,
                find_similar=find_similar,
                generate_recommendations=generate_recommendations
            )
            
            if not result.success:
                logger.warning(
                    f"Question creation failed: {result.errors}",
                    extra={"user_id": current_user["id"]}
                )
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=result.errors[0] if result.errors else "Question creation failed"
                )
            
            # Busca dados completos da pergunta criada
            question_id = result.data["question_id"]
            persistence_gateway = educational_orchestrator.persistence_gateway
            
            question_response = await persistence_gateway.get_question(question_id)
            
            if not question_response.success:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Question created but failed to retrieve data"
                )
            
            question_data_response = question_response.data
            
            # Adiciona dados extras do fluxo de orquestração
            if result.data.get("similar_questions"):
                question_data_response["perguntas_similares"] = result.data["similar_questions"]
            
            if result.data.get("recommendations"):
                question_data_response["recomendacoes"] = result.data["recommendations"]
            
            logger.info(
                f"Question created successfully: {question_id}",
                extra={
                    "question_id": question_id,
                    "user_id": current_user["id"],
                    "embedding_created": result.data.get("embedding_created", False),
                    "similar_found": len(result.data.get("similar_questions", []))
                }
            )
            
            await educational_orchestrator.close()
            
            return PerguntaResponse(**question_data_response)
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error creating question: {str(e)}", exc_info=e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal error during question creation"
            )


@router.get(
    "/questions/{question_id}",
    response_model=Dict[str, Any],
    summary="Buscar Pergunta Completa",
    description="Retorna pergunta com todas as respostas e metadados"
)
async def get_question_complete(
    question_id: str,
    include_evaluations: bool = Query(False, description="Incluir avaliações das respostas"),
    current_user: Dict[str, Any] = Depends(get_current_user_dependency)
):
    """
    Busca pergunta completa com respostas e avaliações.
    
    Args:
        question_id: ID da pergunta
        include_evaluations: Se deve incluir avaliações
        current_user: Usuário autenticado
        
    Returns:
        dict: Pergunta completa com dados relacionados
        
    Raises:
        HTTPException: Se pergunta não encontrada
    """
    async with RequestLogger("get_question_complete") as req_logger:
        try:
            req_logger.add_context(
                question_id=question_id,
                include_evaluations=include_evaluations,
                user_id=current_user["id"]
            )
            
            educational_orchestrator = EducationalOrchestrator()
            
            # Busca pergunta completa
            result = await educational_orchestrator.get_question_with_answers(
                question_id=question_id,
                include_evaluations=include_evaluations
            )
            
            if not result.success:
                if "not found" in str(result.errors).lower():
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Question not found"
                    )
                else:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=result.errors[0] if result.errors else "Failed to retrieve question"
                    )
            
            await educational_orchestrator.close()
            
            return result.data
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting complete question: {str(e)}", exc_info=e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal error retrieving question"
            )


@router.get(
    "/questions",
    response_model=PaginatedResponse[PerguntaResponse],
    summary="Listar Perguntas",
    description="Lista perguntas com filtros e paginação"
)
async def list_questions(
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(20, ge=1, le=100, description="Itens por página"),
    disciplina: Optional[str] = Query(None, description="Filtrar por disciplina"),
    nivel_dificuldade: Optional[str] = Query(None, description="Filtrar por nível"),
    tipo_entrada: Optional[str] = Query(None, description="Filtrar por tipo de entrada"),
    usuario_id: Optional[str] = Query(None, description="Filtrar por usuário"),
    current_user: Dict[str, Any] = Depends(get_current_user_dependency)
):
    """
    Lista perguntas com filtros e paginação.
    
    Args:
        page: Número da página
        page_size: Itens por página
        disciplina: Filtro por disciplina
        nivel_dificuldade: Filtro por nível
        tipo_entrada: Filtro por tipo
        usuario_id: Filtro por usuário
        current_user: Usuário autenticado
        
    Returns:
        PaginatedResponse[PerguntaResponse]: Lista paginada de perguntas
    """
    async with RequestLogger("list_questions") as req_logger:
        try:
            req_logger.add_context(
                page=page,
                page_size=page_size,
                filters={
                    "disciplina": disciplina,
                    "nivel_dificuldade": nivel_dificuldade,
                    "tipo_entrada": tipo_entrada,
                    "usuario_id": usuario_id
                }
            )
            
            educational_orchestrator = EducationalOrchestrator()
            persistence_gateway = educational_orchestrator.persistence_gateway
            
            # Monta query de filtros
            query = {"status": {"$ne": "deleted"}}
            
            if disciplina:
                query["disciplina"] = disciplina
            
            if nivel_dificuldade:
                query["nivel_dificuldade"] = nivel_dificuldade
                
            if tipo_entrada:
                query["tipo_entrada"] = tipo_entrada
                
            if usuario_id:
                query["usuario_id"] = usuario_id
            
            # Executa busca paginada
            pagination = PaginationParams(page=page, page_size=page_size)
            questions_response = await persistence_gateway.search_questions(query, pagination)
            
            if not questions_response.success:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to retrieve questions"
                )
            
            questions_data = questions_response.data
            questions_list = []
            
            # Processa perguntas
            for question in questions_data.get("items", []):
                questions_list.append(PerguntaResponse(**question))
            
            # Monta resposta paginada
            total = questions_data.get("total", 0)
            total_pages = max(1, (total + page_size - 1) // page_size)
            
            paginated_response = PaginatedResponse[PerguntaResponse](
                items=questions_list,
                total=total,
                page=page,
                page_size=page_size,
                total_pages=total_pages,
                has_next=page < total_pages,
                has_previous=page > 1
            )
            
            await educational_orchestrator.close()
            
            return paginated_response
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error listing questions: {str(e)}", exc_info=e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal error listing questions"
            )


# === ENDPOINTS DE RESPOSTAS ===

@router.post(
    "/questions/{question_id}/answers",
    response_model=RespostaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar Resposta",
    description="Cria nova resposta para uma pergunta"
)
async def create_answer(
    question_id: str,
    answer_data: RespostaRequest,
    calculate_quality: bool = Query(True, description="Calcular score de qualidade"),
    current_user: Dict[str, Any] = Depends(get_current_user_dependency)
):
    """
    Cria nova resposta para uma pergunta.
    
    Executa fluxo completo:
    - Valida dados da resposta
    - Verifica se pergunta existe
    - Cria resposta no MongoDB
    - Gera embedding para busca semântica
    - Atualiza contador na pergunta
    - Calcula score de qualidade (opcional)
    
    Args:
        question_id: ID da pergunta
        answer_data: Dados da resposta
        calculate_quality: Se deve calcular qualidade
        current_user: Usuário autenticado
        
    Returns:
        RespostaResponse: Resposta criada
    """
    async with RequestLogger("create_answer") as req_logger:
        try:
            # Adiciona dados do usuário e pergunta
            answer_dict = answer_data.model_dump()
            answer_dict["pergunta_id"] = question_id
            answer_dict["usuario_id"] = current_user["id"]
            
            req_logger.add_context(
                question_id=question_id,
                user_id=current_user["id"],
                calculate_quality=calculate_quality
            )
            
            educational_orchestrator = EducationalOrchestrator()
            
            # Executa fluxo de criação de resposta
            result = await educational_orchestrator.create_answer_flow(
                answer_data=answer_dict,
                calculate_quality=calculate_quality
            )
            
            if not result.success:
                logger.warning(
                    f"Answer creation failed: {result.errors}",
                    extra={
                        "question_id": question_id,
                        "user_id": current_user["id"]
                    }
                )
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=result.errors[0] if result.errors else "Answer creation failed"
                )
            
            # Busca dados completos da resposta criada
            answer_id = result.data["answer_id"]
            persistence_gateway = educational_orchestrator.persistence_gateway
            
            answer_response = await persistence_gateway.get_answer(answer_id)
            
            if not answer_response.success:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Answer created but failed to retrieve data"
                )
            
            answer_data_response = answer_response.data
            
            # Adiciona score de qualidade se calculado
            if result.data.get("quality_score") is not None:
                answer_data_response["quality_score"] = result.data["quality_score"]
            
            logger.info(
                f"Answer created successfully: {answer_id}",
                extra={
                    "answer_id": answer_id,
                    "question_id": question_id,
                    "user_id": current_user["id"],
                    "embedding_created": result.data.get("embedding_created", False),
                    "quality_score": result.data.get("quality_score")
                }
            )
            
            await educational_orchestrator.close()
            
            return RespostaResponse(**answer_data_response)
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error creating answer: {str(e)}", exc_info=e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal error during answer creation"
            )


@router.get(
    "/questions/{question_id}/answers",
    response_model=PaginatedResponse[RespostaResponse],
    summary="Listar Respostas da Pergunta",
    description="Lista todas as respostas de uma pergunta específica"
)
async def list_question_answers(
    question_id: str,
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(20, ge=1, le=50, description="Itens por página"),
    current_user: Dict[str, Any] = Depends(get_current_user_dependency)
):
    """
    Lista respostas de uma pergunta específica.
    
    Args:
        question_id: ID da pergunta
        page: Número da página
        page_size: Itens por página
        current_user: Usuário autenticado
        
    Returns:
        PaginatedResponse[RespostaResponse]: Lista paginada de respostas
    """
    async with RequestLogger("list_question_answers") as req_logger:
        try:
            req_logger.add_context(
                question_id=question_id,
                page=page,
                page_size=page_size
            )
            
            educational_orchestrator = EducationalOrchestrator()
            persistence_gateway = educational_orchestrator.persistence_gateway
            
            # Busca respostas da pergunta
            pagination = PaginationParams(page=page, page_size=page_size)
            answers_response = await persistence_gateway.get_answers_by_question(
                question_id, pagination
            )
            
            if not answers_response.success:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to retrieve answers"
                )
            
            answers_data = answers_response.data
            answers_list = []
            
            # Processa respostas
            for answer in answers_data.get("items", []):
                answers_list.append(RespostaResponse(**answer))
            
            # Monta resposta paginada
            total = answers_data.get("total", 0)
            total_pages = max(1, (total + page_size - 1) // page_size)
            
            paginated_response = PaginatedResponse[RespostaResponse](
                items=answers_list,
                total=total,
                page=page,
                page_size=page_size,
                total_pages=total_pages,
                has_next=page < total_pages,
                has_previous=page > 1
            )
            
            await educational_orchestrator.close()
            
            return paginated_response
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error listing question answers: {str(e)}", exc_info=e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal error listing answers"
            )


# === ENDPOINTS DE AVALIAÇÕES ===

@router.post(
    "/answers/{answer_id}/evaluations",
    response_model=AvaliacaoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar Avaliação",
    description="Cria nova avaliação para uma resposta"
)
async def create_evaluation(
    answer_id: str,
    evaluation_data: AvaliacaoRequest,
    update_user_stats: bool = Query(True, description="Atualizar estatísticas do usuário"),
    generate_feedback: bool = Query(True, description="Gerar feedback personalizado"),
    current_user: Dict[str, Any] = Depends(get_current_user_dependency)
):
    """
    Cria nova avaliação para uma resposta.
    
    Args:
        answer_id: ID da resposta
        evaluation_data: Dados da avaliação
        update_user_stats: Se deve atualizar stats
        generate_feedback: Se deve gerar feedback
        current_user: Usuário autenticado
        
    Returns:
        AvaliacaoResponse: Avaliação criada
    """
    async with RequestLogger("create_evaluation") as req_logger:
        try:
            # Adiciona dados do usuário e resposta
            evaluation_dict = evaluation_data.model_dump()
            evaluation_dict["resposta_id"] = answer_id
            evaluation_dict["avaliador_id"] = current_user["id"]
            
            req_logger.add_context(
                answer_id=answer_id,
                evaluator_id=current_user["id"],
                nota=evaluation_dict.get("nota")
            )
            
            educational_orchestrator = EducationalOrchestrator()
            
            # Executa fluxo de criação de avaliação
            result = await educational_orchestrator.create_evaluation_flow(
                evaluation_data=evaluation_dict,
                update_user_stats=update_user_stats,
                generate_feedback=generate_feedback
            )
            
            if not result.success:
                logger.warning(
                    f"Evaluation creation failed: {result.errors}",
                    extra={
                        "answer_id": answer_id,
                        "evaluator_id": current_user["id"]
                    }
                )
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=result.errors[0] if result.errors else "Evaluation creation failed"
                )
            
            # Busca dados completos da avaliação criada
            evaluation_id = result.data["evaluation_id"]
            persistence_gateway = educational_orchestrator.persistence_gateway
            
            evaluation_response = await persistence_gateway.mongodb.get_document(
                "avaliacoes", evaluation_id
            )
            
            if not evaluation_response.success:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Evaluation created but failed to retrieve data"
                )
            
            logger.info(
                f"Evaluation created successfully: {evaluation_id}",
                extra={
                    "evaluation_id": evaluation_id,
                    "answer_id": answer_id,
                    "evaluator_id": current_user["id"],
                    "nota": evaluation_dict.get("nota")
                }
            )
            
            await educational_orchestrator.close()
            
            return AvaliacaoResponse(**evaluation_response.data)
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error creating evaluation: {str(e)}", exc_info=e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal error during evaluation creation"
            )


# === ENDPOINTS DE BUSCA SEMÂNTICA ===

@router.post(
    "/search",
    response_model=BuscaSemanticaResponse,
    summary="Busca Semântica",
    description="Busca conteúdo educacional usando similaridade semântica"
)
async def semantic_search(
    search_request: BuscaSemanticaRequest,
    current_user: Dict[str, Any] = Depends(get_current_user_dependency)
):
    """
    Executa busca semântica no conteúdo educacional.
    
    Args:
        search_request: Parâmetros de busca
        current_user: Usuário autenticado
        
    Returns:
        BuscaSemanticaResponse: Resultados da busca semântica
    """
    async with RequestLogger("semantic_search") as req_logger:
        try:
            req_logger.add_context(
                query=search_request.query,
                limite=search_request.limite,
                user_id=current_user["id"]
            )
            
            educational_orchestrator = EducationalOrchestrator()
            
            # Executa busca semântica
            result = await educational_orchestrator.search_educational_content(
                query=search_request.query,
                content_types=["question", "answer"],  # Busca em perguntas e respostas
                filters=search_request.filtros,
                limit=search_request.limite
            )
            
            if not result.success:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=result.errors[0] if result.errors else "Semantic search failed"
                )
            
            # Converte resultado para formato de resposta
            search_response = BuscaSemanticaResponse(
                resultados=result.data["results"],
                total_encontrados=result.data["total_found"],
                tempo_busca=result.duration_ms / 1000,  # Converte para segundos
                query_original=search_request.query,
                score_threshold=search_request.score_threshold,
                metadados_busca={
                    "content_types": result.data["content_types"],
                    "user_id": current_user["id"]
                }
            )
            
            logger.info(
                f"Semantic search completed: {result.data['total_found']} results",
                extra={
                    "query": search_request.query,
                    "results_count": result.data["total_found"],
                    "user_id": current_user["id"]
                }
            )
            
            await educational_orchestrator.close()
            
            return search_response
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in semantic search: {str(e)}", exc_info=e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal error during semantic search"
            )


@router.get(
    "/search/similar/{content_id}",
    response_model=List[Dict[str, Any]],
    summary="Buscar Conteúdo Similar",
    description="Encontra conteúdo similar a uma pergunta ou resposta específica"
)
async def find_similar_content(
    content_id: str,
    content_type: str = Query(..., description="Tipo de conteúdo (question ou answer)"),
    limit: int = Query(10, ge=1, le=50, description="Limite de resultados"),
    current_user: Dict[str, Any] = Depends(get_current_user_dependency)
):
    """
    Encontra conteúdo similar a um item específico.
    
    Args:
        content_id: ID do conteúdo de referência
        content_type: Tipo do conteúdo (question ou answer)
        limit: Limite de resultados
        current_user: Usuário autenticado
        
    Returns:
        List[Dict]: Lista de conteúdo similar
    """
    async with RequestLogger("find_similar_content") as req_logger:
        try:
            if content_type not in ["question", "answer"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Content type must be 'question' or 'answer'"
                )
            
            req_logger.add_context(
                content_id=content_id,
                content_type=content_type,
                limit=limit
            )
            
            educational_orchestrator = EducationalOrchestrator()
            persistence_gateway = educational_orchestrator.persistence_gateway
            
            # Busca conteúdo original
            if content_type == "question":
                content_response = await persistence_gateway.get_question(content_id)
                content_field = "conteudo"
            else:
                content_response = await persistence_gateway.get_answer(content_id)
                content_field = "conteudo"
            
            if not content_response.success:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"{content_type.title()} not found"
                )
            
            content_text = content_response.data.get(content_field, "")
            
            if not content_text:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Content has no text for similarity search"
                )
            
            # Executa busca por similaridade
            similar_response = await persistence_gateway.qdrant.search_similar(
                query_text=content_text,
                limit=limit + 1,  # +1 para excluir o próprio item
                score_threshold=0.5,
                filters={"type": content_type}
            )
            
            if not similar_response.success:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to find similar content"
                )
            
            # Remove o próprio item dos resultados
            similar_items = []
            for item in similar_response.data.get("resultados", []):
                item_id = item.get("payload", {}).get(f"{content_type}_id")
                if item_id != content_id:
                    similar_items.append(item)
            
            # Limita ao número solicitado
            similar_items = similar_items[:limit]
            
            await educational_orchestrator.close()
            
            return similar_items
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error finding similar content: {str(e)}", exc_info=e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal error finding similar content"
            )


# === ENDPOINTS DE ESTATÍSTICAS ===

@router.get(
    "/stats/user/{user_id}",
    response_model=Dict[str, Any],
    summary="Estatísticas do Usuário",
    description="Retorna estatísticas educacionais de um usuário"
)
async def get_user_educational_stats(
    user_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user_dependency)
):
    """
    Obtém estatísticas educacionais de um usuário.
    
    Args:
        user_id: ID do usuário
        current_user: Usuário autenticado
        
    Returns:
        dict: Estatísticas educacionais
    """
    async with RequestLogger("get_user_educational_stats") as req_logger:
        try:
            # Verifica se pode acessar estatísticas do usuário
            if user_id != current_user["id"] and current_user.get("tipo_usuario") != "admin":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Can only access own statistics"
                )
            
            req_logger.add_context(
                target_user_id=user_id,
                requester_id=current_user["id"]
            )
            
            educational_orchestrator = EducationalOrchestrator()
            persistence_gateway = educational_orchestrator.persistence_gateway
            
            # Busca estatísticas básicas
            stats = {
                "user_id": user_id,
                "perguntas": {
                    "total": 0,
                    "por_disciplina": {},
                    "por_dificuldade": {}
                },
                "respostas": {
                    "total": 0,
                    "media_qualidade": 0,
                    "total_avaliacoes": 0
                },
                "avaliacoes": {
                    "dadas": 0,
                    "recebidas": 0,
                    "nota_media_dada": 0,
                    "nota_media_recebida": 0
                }
            }
            
            # Conta perguntas do usuário
            questions_response = await persistence_gateway.search_questions(
                {"usuario_id": user_id, "status": {"$ne": "deleted"}},
                PaginationParams(page=1, page_size=1000)  # Limite alto para contar tudo
            )
            
            if questions_response.success:
                questions = questions_response.data.get("items", [])
                stats["perguntas"]["total"] = len(questions)
                
                # Agrupa por disciplina
                for question in questions:
                    disciplina = question.get("disciplina", "Outras")
                    stats["perguntas"]["por_disciplina"][disciplina] = stats["perguntas"]["por_disciplina"].get(disciplina, 0) + 1
                    
                    nivel = question.get("nivel_dificuldade", "intermediario")
                    stats["perguntas"]["por_dificuldade"][nivel] = stats["perguntas"]["por_dificuldade"].get(nivel, 0) + 1
            
            # Conta respostas do usuário
            answers_response = await persistence_gateway.mongodb.find_documents(
                "respostas",
                {"usuario_id": user_id, "status": {"$ne": "deleted"}},
                PaginationParams(page=1, page_size=1000)
            )
            
            if answers_response.success:
                answers = answers_response.data.get("items", [])
                stats["respostas"]["total"] = len(answers)
            
            await educational_orchestrator.close()
            
            return stats
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting user educational stats: {str(e)}", exc_info=e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal error retrieving statistics"
            )