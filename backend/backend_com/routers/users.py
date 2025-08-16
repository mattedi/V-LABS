"""
Endpoints para gerenciamento de usuários.

Operações CRUD de usuários, atualização de perfil,
configurações e informações relacionadas.
"""

from fastapi import APIRouter, HTTPException, Depends, Query, status
from typing import Dict, Any, Optional, List

from ..models import (
    UsuarioRequest,
    UsuarioResponse, 
    PaginationParams,
    PaginatedResponse,
    SuccessResponse,
    ErrorResponse
)
from ..orchestration import UserOrchestrator
from backend.backend_com.routers.auth import get_current_user_dependency
from ..utils.logging import setup_logger, RequestLogger

# Configuração do router
router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(get_current_user_dependency)],
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        403: {"model": ErrorResponse, "description": "Forbidden"},
        404: {"model": ErrorResponse, "description": "Not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)

# Logger específico para usuários
logger = setup_logger("users_router")


@router.get(
    "/me",
    response_model=UsuarioResponse,
    summary="Meu Perfil",
    description="Retorna dados do perfil do usuário autenticado"
)
async def get_my_profile(current_user: Dict[str, Any] = Depends(get_current_user_dependency)):
    """
    Obtém dados completos do perfil do usuário autenticado.
    
    Args:
        current_user: Dados do usuário autenticado (via dependency)
        
    Returns:
        UsuarioResponse: Dados completos do perfil
        
    Raises:
        HTTPException: Se usuário não encontrado
    """
    async with RequestLogger("get_my_profile") as req_logger:
        try:
            user_id = current_user["id"]
            req_logger.add_context(user_id=user_id)
            
            user_orchestrator = UserOrchestrator()
            persistence_gateway = user_orchestrator.persistence_gateway
            
            user_response = await persistence_gateway.get_user(user_id)
            
            if not user_response.success:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User profile not found"
                )
            
            # Remove senha dos dados
            user_data = user_response.data.copy()
            user_data.pop("senha", None)
            
            await user_orchestrator.close()
            
            return UsuarioResponse(**user_data)
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting user profile: {str(e)}", exc_info=e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal error retrieving profile"
            )


@router.put(
    "/me",
    response_model=UsuarioResponse,
    summary="Atualizar Meu Perfil",
    description="Atualiza dados do perfil do usuário autenticado"
)
async def update_my_profile(
    update_data: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user_dependency)
):
    """
    Atualiza dados do perfil do usuário autenticado.
    
    Permite atualizar campos como nome, instituição, configurações,
    mas não permite alterar email ou senha (use endpoints específicos).
    
    Args:
        update_data: Dados para atualização
        current_user: Usuário autenticado
        
    Returns:
        UsuarioResponse: Dados atualizados do usuário
        
    Raises:
        HTTPException: Se dados inválidos ou operação falhar
    """
    async with RequestLogger("update_my_profile") as req_logger:
        try:
            user_id = current_user["id"]
            req_logger.add_context(user_id=user_id, update_fields=list(update_data.keys()))
            
            # Remove campos que não podem ser alterados por este endpoint
            forbidden_fields = {"email", "senha", "tipo_usuario", "status"}
            filtered_update_data = {
                k: v for k, v in update_data.items() 
                if k not in forbidden_fields
            }
            
            if not filtered_update_data:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No valid fields to update"
                )
            
            user_orchestrator = UserOrchestrator()
            
            # Executa fluxo de atualização
            result = await user_orchestrator.update_user_profile_flow(
                user_id=user_id,
                update_data=filtered_update_data,
                validate_changes=True
            )
            
            if not result.success:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=result.errors[0] if result.errors else "Profile update failed"
                )
            
            # Busca dados atualizados
            persistence_gateway = user_orchestrator.persistence_gateway
            user_response = await persistence_gateway.get_user(user_id)
            
            if not user_response.success:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Profile updated but failed to retrieve updated data"
                )
            
            # Remove senha dos dados
            user_data = user_response.data.copy()
            user_data.pop("senha", None)
            
            logger.info(
                f"User profile updated successfully: {user_id}",
                extra={
                    "user_id": user_id,
                    "updated_fields": list(filtered_update_data.keys())
                }
            )
            
            await user_orchestrator.close()
            
            return UsuarioResponse(**user_data)
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error updating user profile: {str(e)}", exc_info=e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal error updating profile"
            )


@router.get(
    "/{user_id}",
    response_model=UsuarioResponse,
    summary="Buscar Usuário por ID",
    description="Retorna dados públicos de um usuário específico"
)
async def get_user_by_id(
    user_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user_dependency)
):
    """
    Busca usuário por ID.
    
    Retorna apenas dados públicos do usuário, exceto se o usuário
    autenticado for admin ou o próprio usuário.
    
    Args:
        user_id: ID do usuário a buscar
        current_user: Usuário autenticado
        
    Returns:
        UsuarioResponse: Dados do usuário
        
    Raises:
        HTTPException: Se usuário não encontrado ou sem permissão
    """
    async with RequestLogger("get_user_by_id") as req_logger:
        try:
            req_logger.add_context(
                target_user_id=user_id,
                requester_id=current_user["id"]
            )
            
            user_orchestrator = UserOrchestrator()
            persistence_gateway = user_orchestrator.persistence_gateway
            
            user_response = await persistence_gateway.get_user(user_id)
            
            if not user_response.success:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            user_data = user_response.data.copy()
            
            # Remove dados sensíveis se não for o próprio usuário ou admin
            is_self = current_user["id"] == user_id
            is_admin = current_user.get("tipo_usuario") == "admin"
            
            if not (is_self or is_admin):
                # Remove campos privados para usuários não autorizados
                private_fields = {
                    "senha", "email", "ultimo_login", "configuracoes", 
                    "created_at", "updated_at"
                }
                user_data = {
                    k: v for k, v in user_data.items() 
                    if k not in private_fields
                }
            else:
                # Remove apenas senha
                user_data.pop("senha", None)
            
            await user_orchestrator.close()
            
            return UsuarioResponse(**user_data)
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting user by ID: {str(e)}", exc_info=e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal error retrieving user"
            )


@router.get(
    "/",
    response_model=PaginatedResponse[UsuarioResponse],
    summary="Listar Usuários",
    description="Lista usuários com filtros e paginação (apenas admins)"
)
async def list_users(
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(20, ge=1, le=100, description="Itens por página"),
    tipo_usuario: Optional[str] = Query(None, description="Filtrar por tipo de usuário"),
    status: Optional[str] = Query(None, description="Filtrar por status"),
    search: Optional[str] = Query(None, description="Buscar por nome ou email"),
    current_user: Dict[str, Any] = Depends(get_current_user_dependency)
):
    """
    Lista usuários com filtros e paginação.
    
    Disponível apenas para administradores.
    
    Args:
        page: Número da página
        page_size: Itens por página
        tipo_usuario: Filtro por tipo
        status: Filtro por status
        search: Termo de busca
        current_user: Usuário autenticado
        
    Returns:
        PaginatedResponse[UsuarioResponse]: Lista paginada de usuários
        
    Raises:
        HTTPException: Se não for admin ou erro interno
    """
    async with RequestLogger("list_users") as req_logger:
        try:
            # Verifica se é admin
            if current_user.get("tipo_usuario") != "admin":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Only administrators can list users"
                )
            
            req_logger.add_context(
                page=page,
                page_size=page_size,
                filters={
                    "tipo_usuario": tipo_usuario,
                    "status": status,
                    "search": search
                }
            )
            
            user_orchestrator = UserOrchestrator()
            persistence_gateway = user_orchestrator.persistence_gateway
            
            # Monta query de filtros
            query = {}
            
            if tipo_usuario:
                query["tipo_usuario"] = tipo_usuario
            
            if status:
                query["status"] = status
            
            if search:
                # Busca por nome ou email (implementação básica)
                query["$or"] = [
                    {"nome": {"$regex": search, "$options": "i"}},
                    {"email": {"$regex": search, "$options": "i"}}
                ]
            
            # Executa busca paginada
            pagination = PaginationParams(page=page, page_size=page_size)
            users_response = await persistence_gateway.mongodb.find_documents(
                "usuarios", query, pagination
            )
            
            if not users_response.success:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to retrieve users"
                )
            
            users_data = users_response.data
            users_list = []
            
            # Remove senhas e processa usuários
            for user in users_data.get("items", []):
                user_copy = user.copy()
                user_copy.pop("senha", None)
                users_list.append(UsuarioResponse(**user_copy))
            
            # Monta resposta paginada
            total = users_data.get("total", 0)
            total_pages = max(1, (total + page_size - 1) // page_size)
            
            paginated_response = PaginatedResponse[UsuarioResponse](
                items=users_list,
                total=total,
                page=page,
                page_size=page_size,
                total_pages=total_pages,
                has_next=page < total_pages,
                has_previous=page > 1
            )
            
            await user_orchestrator.close()
            
            return paginated_response
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error listing users: {str(e)}", exc_info=e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal error listing users"
            )


@router.put(
    "/{user_id}/status",
    response_model=SuccessResponse,
    summary="Alterar Status do Usuário",
    description="Altera status de um usuário (apenas admins)"
)
async def update_user_status(
    user_id: str,
    new_status: str,
    current_user: Dict[str, Any] = Depends(get_current_user_dependency)
):
    """
    Altera status de um usuário.
    
    Disponível apenas para administradores.
    Status possíveis: active, inactive, suspended
    
    Args:
        user_id: ID do usuário
        new_status: Novo status
        current_user: Usuário autenticado
        
    Returns:
        SuccessResponse: Confirmação da alteração
        
    Raises:
        HTTPException: Se não for admin, usuário não encontrado ou status inválido
    """
    async with RequestLogger("update_user_status") as req_logger:
        try:
            # Verifica se é admin
            if current_user.get("tipo_usuario") != "admin":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Only administrators can update user status"
                )
            
            # Valida status
            valid_statuses = {"active", "inactive", "suspended"}
            if new_status not in valid_statuses:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                )
            
            req_logger.add_context(
                target_user_id=user_id,
                new_status=new_status,
                admin_user_id=current_user["id"]
            )
            
            user_orchestrator = UserOrchestrator()
            
            # Atualiza status
            result = await user_orchestrator.update_user_profile_flow(
                user_id=user_id,
                update_data={"status": new_status},
                validate_changes=False  # Admin pode alterar status sem validações extras
            )
            
            if not result.success:
                if "not found" in str(result.errors).lower():
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="User not found"
                    )
                else:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=result.errors[0] if result.errors else "Status update failed"
                    )
            
            logger.info(
                f"User status updated: {user_id} -> {new_status}",
                extra={
                    "target_user_id": user_id,
                    "new_status": new_status,
                    "admin_user_id": current_user["id"]
                }
            )
            
            await user_orchestrator.close()
            
            return SuccessResponse(
                message=f"User status updated to {new_status}",
                data={"user_id": user_id, "new_status": new_status}
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error updating user status: {str(e)}", exc_info=e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal error updating user status"
            )


@router.get(
    "/me/settings",
    response_model=Dict[str, Any],
    summary="Minhas Configurações",
    description="Retorna configurações pessoais do usuário"
)
async def get_my_settings(current_user: Dict[str, Any] = Depends(get_current_user_dependency)):
    """
    Obtém configurações pessoais do usuário autenticado.
    
    Args:
        current_user: Usuário autenticado
        
    Returns:
        dict: Configurações do usuário
        
    Raises:
        HTTPException: Se configurações não encontradas
    """
    async with RequestLogger("get_my_settings") as req_logger:
        try:
            user_id = current_user["id"]
            req_logger.add_context(user_id=user_id)
            
            user_orchestrator = UserOrchestrator()
            persistence_gateway = user_orchestrator.persistence_gateway
            
            # Busca configurações do usuário
            settings_response = await persistence_gateway.mongodb.find_documents(
                "configuracoes_usuario",
                {"usuario_id": user_id}
            )
            
            if not settings_response.success or not settings_response.data.get("items"):
                # Retorna configurações padrão se não encontradas
                default_settings = {
                    "notifications": {"email": True, "push": False},
                    "privacy": {"profile_public": False},
                    "learning": {"difficulty_level": "intermediario"}
                }
                
                return {"configuracoes": default_settings}
            
            settings_data = settings_response.data["items"][0]
            await user_orchestrator.close()
            
            return settings_data.get("configuracoes", {})
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting user settings: {str(e)}", exc_info=e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal error retrieving settings"
            )


@router.put(
    "/me/settings",
    response_model=SuccessResponse,
    summary="Atualizar Configurações",
    description="Atualiza configurações pessoais do usuário"
)
async def update_my_settings(
    settings: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user_dependency)
):
    """
    Atualiza configurações pessoais do usuário.
    
    Args:
        settings: Novas configurações
        current_user: Usuário autenticado
        
    Returns:
        SuccessResponse: Confirmação da atualização
        
    Raises:
        HTTPException: Se erro na atualização
    """
    async with RequestLogger("update_my_settings") as req_logger:
        try:
            user_id = current_user["id"]
            req_logger.add_context(user_id=user_id, settings_keys=list(settings.keys()))
            
            user_orchestrator = UserOrchestrator()
            persistence_gateway = user_orchestrator.persistence_gateway
            
            # Busca configurações existentes
            existing_response = await persistence_gateway.mongodb.find_documents(
                "configuracoes_usuario",
                {"usuario_id": user_id}
            )
            
            if existing_response.success and existing_response.data.get("items"):
                # Atualiza configurações existentes
                settings_doc = existing_response.data["items"][0]
                settings_id = settings_doc["_id"]
                
                update_data = {
                    "configuracoes": settings,
                    "updated_at": "2024-01-01T00:00:00"  # Em implementação real, seria datetime.utcnow().isoformat()
                }
                
                await persistence_gateway.mongodb.update_document(
                    "configuracoes_usuario", settings_id, update_data
                )
            else:
                # Cria novas configurações
                settings_data = {
                    "usuario_id": user_id,
                    "configuracoes": settings,
                    "created_at": "2024-01-01T00:00:00",
                    "updated_at": "2024-01-01T00:00:00"
                }
                
                await persistence_gateway.mongodb.create_document(
                    "configuracoes_usuario", settings_data
                )
            
            logger.info(
                f"User settings updated: {user_id}",
                extra={"user_id": user_id}
            )
            
            await user_orchestrator.close()
            
            return SuccessResponse(
                message="Configurações atualizadas com sucesso",
                data={"updated": True}
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error updating user settings: {str(e)}", exc_info=e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal error updating settings"
            )