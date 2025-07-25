"""
Gateway de persistência para comunicação com backend_bd.

Gerencia operações com MongoDB e Qdrant através do backend_bd,
fornecendo interface unificada para o sistema de persistência.
"""

import time
from typing import Any, Dict, List, Optional, Union
from datetime import datetime

from .base_gateway import BaseGateway, GatewayResponse, GatewayError
from .http_client import HTTPClient, RequestConfig
from ..config import get_settings
from ..models import PaginationParams


class MongoDBOperations:
    """
    Operações específicas do MongoDB através do backend_bd.
    """
    
    def __init__(self, client: HTTPClient):
        self.client = client
    
    async def create_document(self, collection: str, document: Dict[str, Any]) -> GatewayResponse:
        """
        Cria novo documento no MongoDB.
        
        Args:
            collection: Nome da coleção
            document: Documento para inserir
            
        Returns:
            GatewayResponse: Resultado da operação
        """
        try:
            response = await self.client.post(
                f"/mongodb/{collection}",
                json_data=document
            )
            
            if response.is_success:
                return GatewayResponse.success_response(
                    data=response.content,
                    duration_ms=response.duration_ms
                )
            else:
                return GatewayResponse.error_response(
                    error_message=f"Failed to create document: {response.content}",
                    status_code=response.status_code,
                    duration_ms=response.duration_ms
                )
                
        except Exception as e:
            return GatewayResponse.error_response(
                error_message=f"Error creating document: {str(e)}"
            )
    
    async def get_document(self, collection: str, document_id: str) -> GatewayResponse:
        """
        Busca documento por ID.
        
        Args:
            collection: Nome da coleção
            document_id: ID do documento
            
        Returns:
            GatewayResponse: Documento encontrado ou erro
        """
        try:
            response = await self.client.get(f"/mongodb/{collection}/{document_id}")
            
            if response.is_success:
                return GatewayResponse.success_response(
                    data=response.content,
                    duration_ms=response.duration_ms
                )
            else:
                return GatewayResponse.error_response(
                    error_message=f"Document not found: {document_id}",
                    status_code=response.status_code,
                    duration_ms=response.duration_ms
                )
                
        except Exception as e:
            return GatewayResponse.error_response(
                error_message=f"Error getting document: {str(e)}"
            )
    
    async def update_document(self, collection: str, document_id: str, 
                            update_data: Dict[str, Any]) -> GatewayResponse:
        """
        Atualiza documento existente.
        
        Args:
            collection: Nome da coleção
            document_id: ID do documento
            update_data: Dados para atualização
            
        Returns:
            GatewayResponse: Resultado da operação
        """
        try:
            response = await self.client.put(
                f"/mongodb/{collection}/{document_id}",
                json_data=update_data
            )
            
            if response.is_success:
                return GatewayResponse.success_response(
                    data=response.content,
                    duration_ms=response.duration_ms
                )
            else:
                return GatewayResponse.error_response(
                    error_message=f"Failed to update document: {response.content}",
                    status_code=response.status_code,
                    duration_ms=response.duration_ms
                )
                
        except Exception as e:
            return GatewayResponse.error_response(
                error_message=f"Error updating document: {str(e)}"
            )
    
    async def delete_document(self, collection: str, document_id: str) -> GatewayResponse:
        """
        Remove documento do MongoDB.
        
        Args:
            collection: Nome da coleção
            document_id: ID do documento
            
        Returns:
            GatewayResponse: Resultado da operação
        """
        try:
            response = await self.client.delete(f"/mongodb/{collection}/{document_id}")
            
            if response.is_success:
                return GatewayResponse.success_response(
                    data={"deleted": True, "document_id": document_id},
                    duration_ms=response.duration_ms
                )
            else:
                return GatewayResponse.error_response(
                    error_message=f"Failed to delete document: {response.content}",
                    status_code=response.status_code,
                    duration_ms=response.duration_ms
                )
                
        except Exception as e:
            return GatewayResponse.error_response(
                error_message=f"Error deleting document: {str(e)}"
            )
    
    async def find_documents(self, collection: str, query: Dict[str, Any],
                           pagination: Optional[PaginationParams] = None,
                           sort: Optional[Dict[str, int]] = None) -> GatewayResponse:
        """
        Busca documentos com filtros e paginação.
        
        Args:
            collection: Nome da coleção
            query: Filtros de busca
            pagination: Parâmetros de paginação
            sort: Critérios de ordenação
            
        Returns:
            GatewayResponse: Lista de documentos encontrados
        """
        try:
            params = {"query": query}
            
            if pagination:
                params.update({
                    "page": pagination.page,
                    "page_size": pagination.page_size
                })
            
            if sort:
                params["sort"] = sort
            
            response = await self.client.get(f"/mongodb/{collection}/search", params=params)
            
            if response.is_success:
                return GatewayResponse.success_response(
                    data=response.content,
                    duration_ms=response.duration_ms
                )
            else:
                return GatewayResponse.error_response(
                    error_message=f"Search failed: {response.content}",
                    status_code=response.status_code,
                    duration_ms=response.duration_ms
                )
                
        except Exception as e:
            return GatewayResponse.error_response(
                error_message=f"Error searching documents: {str(e)}"
            )


class QdrantOperations:
    """
    Operações específicas do Qdrant através do backend_bd.
    """
    
    def __init__(self, client: HTTPClient):
        self.client = client
    
    async def create_embedding(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> GatewayResponse:
        """
        Cria embedding para texto.
        
        Args:
            text: Texto para gerar embedding
            metadata: Metadados associados
            
        Returns:
            GatewayResponse: Embedding gerado
        """
        try:
            request_data = {
                "text": text,
                "metadata": metadata or {}
            }
            
            response = await self.client.post("/qdrant/embeddings", json_data=request_data)
            
            if response.is_success:
                return GatewayResponse.success_response(
                    data=response.content,
                    duration_ms=response.duration_ms
                )
            else:
                return GatewayResponse.error_response(
                    error_message=f"Failed to create embedding: {response.content}",
                    status_code=response.status_code,
                    duration_ms=response.duration_ms
                )
                
        except Exception as e:
            return GatewayResponse.error_response(
                error_message=f"Error creating embedding: {str(e)}"
            )
    
    async def search_similar(self, query_text: str, limit: int = 10,
                           score_threshold: float = 0.7,
                           filters: Optional[Dict[str, Any]] = None) -> GatewayResponse:
        """
        Busca por similaridade semântica.
        
        Args:
            query_text: Texto da consulta
            limit: Número máximo de resultados
            score_threshold: Score mínimo de similaridade
            filters: Filtros adicionais
            
        Returns:
            GatewayResponse: Resultados da busca semântica
        """
        try:
            request_data = {
                "query": query_text,
                "limit": limit,
                "score_threshold": score_threshold,
                "filters": filters or {}
            }
            
            response = await self.client.post("/qdrant/search", json_data=request_data)
            
            if response.is_success:
                return GatewayResponse.success_response(
                    data=response.content,
                    duration_ms=response.duration_ms
                )
            else:
                return GatewayResponse.error_response(
                    error_message=f"Semantic search failed: {response.content}",
                    status_code=response.status_code,
                    duration_ms=response.duration_ms
                )
                
        except Exception as e:
            return GatewayResponse.error_response(
                error_message=f"Error in semantic search: {str(e)}"
            )
    
    async def store_vector(self, vector_id: str, vector: List[float],
                          payload: Optional[Dict[str, Any]] = None) -> GatewayResponse:
        """
        Armazena vetor no Qdrant.
        
        Args:
            vector_id: ID único do vetor
            vector: Vetor de embeddings
            payload: Dados associados ao vetor
            
        Returns:
            GatewayResponse: Resultado da operação
        """
        try:
            request_data = {
                "id": vector_id,
                "vector": vector,
                "payload": payload or {}
            }
            
            response = await self.client.post("/qdrant/vectors", json_data=request_data)
            
            if response.is_success:
                return GatewayResponse.success_response(
                    data=response.content,
                    duration_ms=response.duration_ms
                )
            else:
                return GatewayResponse.error_response(
                    error_message=f"Failed to store vector: {response.content}",
                    status_code=response.status_code,
                    duration_ms=response.duration_ms
                )
                
        except Exception as e:
            return GatewayResponse.error_response(
                error_message=f"Error storing vector: {str(e)}"
            )
    
    async def delete_vector(self, vector_id: str) -> GatewayResponse:
        """
        Remove vetor do Qdrant.
        
        Args:
            vector_id: ID do vetor
            
        Returns:
            GatewayResponse: Resultado da operação
        """
        try:
            response = await self.client.delete(f"/qdrant/vectors/{vector_id}")
            
            if response.is_success:
                return GatewayResponse.success_response(
                    data={"deleted": True, "vector_id": vector_id},
                    duration_ms=response.duration_ms
                )
            else:
                return GatewayResponse.error_response(
                    error_message=f"Failed to delete vector: {response.content}",
                    status_code=response.status_code,
                    duration_ms=response.duration_ms
                )
                
        except Exception as e:
            return GatewayResponse.error_response(
                error_message=f"Error deleting vector: {str(e)}"
            )


class PersistenceGateway(BaseGateway):
    """
    Gateway principal para operações de persistência.
    
    Unifica acesso ao MongoDB e Qdrant através do backend_bd,
    fornecendo interface única para todas as operações de dados.
    """
    
    def __init__(self):
        settings = get_settings()
        super().__init__(
            service_name="backend_bd",
            base_url=settings.backend_bd_url,
            timeout=settings.backend_bd_timeout
        )
        
        # Configuração específica para backend_bd
        config = RequestConfig(
            timeout=settings.backend_bd_timeout,
            max_retries=3,
            retry_delay=1.0,
            retry_backoff=2.0
        )
        
        self.http_client = HTTPClient(settings.backend_bd_url, config)
        self.mongodb = MongoDBOperations(self.http_client)
        self.qdrant = QdrantOperations(self.http_client)
    
    async def health_check(self) -> GatewayResponse:
        """
        Verifica saúde do backend_bd (MongoDB + Qdrant).
        
        Returns:
            GatewayResponse: Status de saúde dos serviços
        """
        try:
            start_time = time.time()
            response = await self.http_client.get("/health")
            duration_ms = (time.time() - start_time) * 1000
            
            if response.is_success:
                return GatewayResponse.success_response(
                    data=response.content,
                    metadata={"service": self.service_name},
                    duration_ms=duration_ms
                )
            else:
                return GatewayResponse.error_response(
                    error_message=f"Health check failed: {response.content}",
                    status_code=response.status_code,
                    duration_ms=duration_ms
                )
                
        except Exception as e:
            return GatewayResponse.error_response(
                error_message=f"Health check error: {str(e)}"
            )
    
    # === OPERAÇÕES DE USUÁRIO ===
    
    async def create_user(self, user_data: Dict[str, Any]) -> GatewayResponse:
        """
        Cria novo usuário no sistema.
        
        Args:
            user_data: Dados do usuário
            
        Returns:
            GatewayResponse: Usuário criado
        """
        user_data["created_at"] = datetime.utcnow().isoformat()
        user_data["updated_at"] = datetime.utcnow().isoformat()
        
        return await self.mongodb.create_document("usuarios", user_data)
    
    async def get_user(self, user_id: str) -> GatewayResponse:
        """
        Busca usuário por ID.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            GatewayResponse: Dados do usuário
        """
        return await self.mongodb.get_document("usuarios", user_id)
    
    async def get_user_by_email(self, email: str) -> GatewayResponse:
        """
        Busca usuário por email.
        
        Args:
            email: Email do usuário
            
        Returns:
            GatewayResponse: Dados do usuário
        """
        query = {"email": email, "status": {"$ne": "deleted"}}
        result = await self.mongodb.find_documents("usuarios", query)
        
        if result.success and result.data.get("items"):
            # Retorna o primeiro usuário encontrado
            user = result.data["items"][0]
            return GatewayResponse.success_response(
                data=user,
                duration_ms=result.duration_ms
            )
        else:
            return GatewayResponse.error_response(
                error_message="User not found",
                status_code=404
            )
    
    async def update_user(self, user_id: str, update_data: Dict[str, Any]) -> GatewayResponse:
        """
        Atualiza dados do usuário.
        
        Args:
            user_id: ID do usuário
            update_data: Dados para atualização
            
        Returns:
            GatewayResponse: Usuário atualizado
        """
        update_data["updated_at"] = datetime.utcnow().isoformat()
        return await self.mongodb.update_document("usuarios", user_id, update_data)
    
    # === OPERAÇÕES DE PERGUNTA ===
    
    async def create_question(self, question_data: Dict[str, Any]) -> GatewayResponse:
        """
        Cria nova pergunta no sistema.
        
        Args:
            question_data: Dados da pergunta
            
        Returns:
            GatewayResponse: Pergunta criada
        """
        question_data["created_at"] = datetime.utcnow().isoformat()
        question_data["updated_at"] = datetime.utcnow().isoformat()
        
        # Cria pergunta no MongoDB
        mongo_result = await self.mongodb.create_document("perguntas", question_data)
        
        if mongo_result.success:
            # Cria embedding para busca semântica
            question_text = question_data.get("conteudo", "")
            if question_text:
                embedding_metadata = {
                    "type": "question",
                    "question_id": mongo_result.data.get("_id"),
                    "user_id": question_data.get("usuario_id"),
                    "disciplina": question_data.get("disciplina"),
                    "created_at": question_data["created_at"]
                }
                
                await self.qdrant.create_embedding(question_text, embedding_metadata)
        
        return mongo_result
    
    async def get_question(self, question_id: str) -> GatewayResponse:
        """
        Busca pergunta por ID.
        
        Args:
            question_id: ID da pergunta
            
        Returns:
            GatewayResponse: Dados da pergunta
        """
        return await self.mongodb.get_document("perguntas", question_id)
    
    async def search_questions(self, query: Dict[str, Any],
                             pagination: Optional[PaginationParams] = None) -> GatewayResponse:
        """
        Busca perguntas com filtros.
        
        Args:
            query: Filtros de busca
            pagination: Parâmetros de paginação
            
        Returns:
            GatewayResponse: Lista de perguntas
        """
        return await self.mongodb.find_documents("perguntas", query, pagination)
    
    async def search_questions_semantic(self, query_text: str, limit: int = 10,
                                      filters: Optional[Dict[str, Any]] = None) -> GatewayResponse:
        """
        Busca perguntas por similaridade semântica.
        
        Args:
            query_text: Texto da consulta
            limit: Número máximo de resultados
            filters: Filtros adicionais
            
        Returns:
            GatewayResponse: Perguntas similares
        """
        search_filters = {"type": "question"}
        if filters:
            search_filters.update(filters)
        
        return await self.qdrant.search_similar(query_text, limit, 0.7, search_filters)
    
    # === OPERAÇÕES DE RESPOSTA ===
    
    async def create_answer(self, answer_data: Dict[str, Any]) -> GatewayResponse:
        """
        Cria nova resposta no sistema.
        
        Args:
            answer_data: Dados da resposta
            
        Returns:
            GatewayResponse: Resposta criada
        """
        answer_data["created_at"] = datetime.utcnow().isoformat()
        answer_data["updated_at"] = datetime.utcnow().isoformat()
        
        # Cria resposta no MongoDB
        mongo_result = await self.mongodb.create_document("respostas", answer_data)
        
        if mongo_result.success:
            # Cria embedding para busca semântica
            answer_text = answer_data.get("conteudo", "")
            if answer_text:
                embedding_metadata = {
                    "type": "answer",
                    "answer_id": mongo_result.data.get("_id"),
                    "question_id": answer_data.get("pergunta_id"),
                    "user_id": answer_data.get("usuario_id"),
                    "created_at": answer_data["created_at"]
                }
                
                await self.qdrant.create_embedding(answer_text, embedding_metadata)
        
        return mongo_result
    
    async def get_answer(self, answer_id: str) -> GatewayResponse:
        """
        Busca resposta por ID.
        
        Args:
            answer_id: ID da resposta
            
        Returns:
            GatewayResponse: Dados da resposta
        """
        return await self.mongodb.get_document("respostas", answer_id)
    
    async def get_answers_by_question(self, question_id: str,
                                    pagination: Optional[PaginationParams] = None) -> GatewayResponse:
        """
        Busca respostas de uma pergunta específica.
        
        Args:
            question_id: ID da pergunta
            pagination: Parâmetros de paginação
            
        Returns:
            GatewayResponse: Lista de respostas
        """
        query = {"pergunta_id": question_id, "status": {"$ne": "deleted"}}
        sort = {"created_at": -1}  # Mais recentes primeiro
        
        return await self.mongodb.find_documents("respostas", query, pagination, sort)
    
    # === OPERAÇÕES DE AVALIAÇÃO ===
    
    async def create_evaluation(self, evaluation_data: Dict[str, Any]) -> GatewayResponse:
        """
        Cria nova avaliação no sistema.
        
        Args:
            evaluation_data: Dados da avaliação
            
        Returns:
            GatewayResponse: Avaliação criada
        """
        evaluation_data["created_at"] = datetime.utcnow().isoformat()
        evaluation_data["updated_at"] = datetime.utcnow().isoformat()
        
        return await self.mongodb.create_document("avaliacoes", evaluation_data)
    
    async def get_evaluations_by_answer(self, answer_id: str,
                                      pagination: Optional[PaginationParams] = None) -> GatewayResponse:
        """
        Busca avaliações de uma resposta específica.
        
        Args:
            answer_id: ID da resposta
            pagination: Parâmetros de paginação
            
        Returns:
            GatewayResponse: Lista de avaliações
        """
        query = {"resposta_id": answer_id, "status": {"$ne": "deleted"}}
        sort = {"created_at": -1}  # Mais recentes primeiro
        
        return await self.mongodb.find_documents("avaliacoes", query, pagination, sort)
    
    # === OPERAÇÕES DE LOG ===
    
    async def create_log_entry(self, log_data: Dict[str, Any]) -> GatewayResponse:
        """
        Cria entrada de log no sistema.
        
        Args:
            log_data: Dados do log
            
        Returns:
            GatewayResponse: Log criado
        """
        log_data["timestamp"] = datetime.utcnow().isoformat()
        
        return await self.mongodb.create_document("logs", log_data)
    
    async def close(self) -> None:
        """
        Fecha conexões e limpa recursos.
        """
        await self.http_client.close()
        await super().close()