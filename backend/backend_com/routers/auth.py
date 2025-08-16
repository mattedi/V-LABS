"""
Endpoints de autenticação e autorização.

Gerencia login, logout, registro de usuários e
operações relacionadas à segurança.
"""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Any, Optional

from ..models import (
    LoginRequest, 
    LoginResponse, 
    UsuarioRequest, 
    UsuarioResponse,
    ErrorResponse,
    SuccessResponse
)
from ..orchestration import UserOrchestrator
from ..utils.logging import setup_logger, RequestLogger

# Configuração do router
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={
        400: {"model": ErrorResponse, "description": "Bad request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)

# Logger específico para autenticação
logger = setup_logger("auth_router")

# Security scheme para Bearer token
security = HTTPBearer()


@router.post(
    "/register",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar Novo Usuário",
    description="Cria uma nova conta de usuário no sistema"
)
async def register_user(user_data: UsuarioRequest):
    """
    Registra um novo usuário no sistema.
    
    Este endpoint executa o fluxo completo de registro:
    - Valida dados de entrada
    - Verifica se email já existe
    - Cria hash seguro da senha
    - Cria usuário no banco de dados
    - Configura preferências iniciais
    - Envia email de verificação (se configurado)
    
    Args:
        user_data: Dados do novo usuário
        
    Returns:
        UsuarioResponse: Dados do usuário criado
        
    Raises:
        HTTPException: Se dados inválidos ou email já existe
    """
    async with RequestLogger("register_user") as req_logger:
        try:
            # Inicializa orquestrador
            user_orchestrator = UserOrchestrator()
            
            # Converte para dict e remove senha do log
            user_dict = user_data.model_dump()
            req_logger.add_context(
                email=user_dict.get("email"),
                tipo_usuario=user_dict.get("tipo_usuario")
            )
            
            # Executa fluxo de registro
            result = await user_orchestrator.register_user_flow(
                user_dict,
                send_verification=True,
                send_welcome=True
            )
            
            if not result.success:
                logger.warning(
                    f"User registration failed: {result.errors}",
                    extra={"email": user_dict.get("email")}
                )
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=result.errors[0] if result.errors else "Registration failed"
                )
            
            # Busca dados completos do usuário criado
            user_id = result.data["user_id"]
            persistence_gateway = user_orchestrator.persistence_gateway
            
            user_response = await persistence_gateway.get_user(user_id)
            
            if not user_response.success:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="User created but failed to retrieve data"
                )
            
            # Remove senha dos dados de resposta
            user_data_response = user_response.data.copy()
            user_data_response.pop("senha", None)
            
            logger.info(
                f"User registered successfully: {user_id}",
                extra={
                    "user_id": user_id,
                    "email": user_dict.get("email"),
                    "verification_sent": result.data.get("email_verification_sent", False)
                }
            )
            
            await user_orchestrator.close()
            
            return UsuarioResponse(**user_data_response)
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in user registration: {str(e)}", exc_info=e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal error during registration"
            )


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="Autenticar Usuário",
    description="Autentica usuário e retorna tokens de acesso"
)
async def login_user(login_data: LoginRequest):
    """
    Autentica usuário no sistema.
    
    Executa o fluxo completo de autenticação:
    - Valida credenciais
    - Verifica status da conta
    - Gera tokens de acesso
    - Cria sessão de usuário
    - Atualiza último login
    
    Args:
        login_data: Credenciais de login
        
    Returns:
        LoginResponse: Tokens e dados do usuário
        
    Raises:
        HTTPException: Se credenciais inválidas ou conta inativa
    """
    async with RequestLogger("login_user") as req_logger:
        try:
            user_orchestrator = UserOrchestrator()
            
            req_logger.add_context(
                email=login_data.email,
                remember_me=login_data.lembrar_me
            )
            
            # Executa fluxo de autenticação
            result = await user_orchestrator.authenticate_user_flow(
                email=login_data.email,
                password=login_data.senha,
                remember_me=login_data.lembrar_me
            )
            
            if not result.success:
                logger.warning(
                    f"Authentication failed: {result.errors}",
                    extra={"email": login_data.email}
                )
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=result.errors[0] if result.errors else "Authentication failed"
                )
            
            # Busca dados completos do usuário
            user_id = result.data["user_id"]
            persistence_gateway = user_orchestrator.persistence_gateway
            
            user_response = await persistence_gateway.get_user(user_id)
            
            if not user_response.success:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Authentication successful but failed to retrieve user data"
                )
            
            # Remove senha dos dados
            user_data_response = user_response.data.copy()
            user_data_response.pop("senha", None)
            
            # Monta resposta de login
            login_response = LoginResponse(
                access_token=result.data["access_token"],
                token_type="bearer",
                expires_in=3600,  # Em implementação real, seria calculado
                refresh_token=result.data.get("refresh_token"),
                usuario=UsuarioResponse(**user_data_response)
            )
            
            logger.info(
                f"User authenticated successfully: {user_id}",
                extra={
                    "user_id": user_id,
                    "email": login_data.email,
                    "session_created": result.data.get("session_created", False)
                }
            )
            
            await user_orchestrator.close()
            
            return login_response
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in user authentication: {str(e)}", exc_info=e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal error during authentication"
            )


@router.post(
    "/logout",
    response_model=SuccessResponse,
    summary="Logout do Usuário",
    description="Encerra sessão do usuário e invalida tokens"
)
async def logout_user(
    logout_all: bool = False,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Realiza logout do usuário.
    
    Args:
        logout_all: Se deve fazer logout de todos os dispositivos
        credentials: Token de autorização
        
    Returns:
        SuccessResponse: Confirmação do logout
        
    Raises:
        HTTPException: Se token inválido
    """
    async with RequestLogger("logout_user") as req_logger:
        try:
            access_token = credentials.credentials
            
            # Busca usuário pelo token (implementação simplificada)
            user_orchestrator = UserOrchestrator()
            
            # Em implementação real, validaria token e obteria user_id
            # Por simplicidade, assumindo que token é válido
            user_id = "user_id_from_token"  # Placeholder
            
            req_logger.add_context(
                user_id=user_id,
                logout_all=logout_all
            )
            
            # Executa fluxo de logout
            result = await user_orchestrator.logout_user_flow(
                user_id=user_id,
                access_token=access_token,
                logout_all_devices=logout_all
            )
            
            if not result.success:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=result.errors[0] if result.errors else "Logout failed"
                )
            
            logger.info(
                f"User logged out successfully: {user_id}",
                extra={
                    "user_id": user_id,
                    "logout_all": logout_all
                }
            )
            
            await user_orchestrator.close()
            
            return SuccessResponse(
                message="Logout realizado com sucesso",
                data={"logged_out": True, "all_devices": logout_all}
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in user logout: {str(e)}", exc_info=e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal error during logout"
            )


@router.post(
    "/refresh",
    response_model=Dict[str, Any],
    summary="Renovar Token",
    description="Renova token de acesso usando refresh token"
)
async def refresh_token(refresh_token: str):
    """
    Renova token de acesso.
    
    Args:
        refresh_token: Token de renovação
        
    Returns:
        dict: Novo token de acesso
        
    Raises:
        HTTPException: Se refresh token inválido ou expirado
    """
    async with RequestLogger("refresh_token"):
        try:
            # Em implementação real, validaria refresh token
            # e geraria novo access token
            
            # Placeholder - implementação simplificada
            new_access_token = "new_access_token_here"
            
            logger.info("Token refreshed successfully")
            
            return {
                "access_token": new_access_token,
                "token_type": "bearer",
                "expires_in": 3600
            }
            
        except Exception as e:
            logger.error(f"Error refreshing token: {str(e)}", exc_info=e)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token"
            )


@router.post(
    "/change-password",
    response_model=SuccessResponse,
    summary="Alterar Senha",
    description="Altera senha do usuário autenticado"
)
async def change_password(
    current_password: str,
    new_password: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Altera senha do usuário.
    
    Args:
        current_password: Senha atual
        new_password: Nova senha
        credentials: Token de autorização
        
    Returns:
        SuccessResponse: Confirmação da alteração
        
    Raises:
        HTTPException: Se senha atual incorreta ou nova senha inválida
    """
    async with RequestLogger("change_password") as req_logger:
        try:
            access_token = credentials.credentials
            
            # Em implementação real, extrairia user_id do token
            user_id = "user_id_from_token"  # Placeholder
            
            req_logger.add_context(user_id=user_id)
            
            user_orchestrator = UserOrchestrator()
            
            # Executa fluxo de alteração de senha
            result = await user_orchestrator.change_password_flow(
                user_id=user_id,
                current_password=current_password,
                new_password=new_password
            )
            
            if not result.success:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=result.errors[0] if result.errors else "Password change failed"
                )
            
            logger.info(
                f"Password changed successfully: {user_id}",
                extra={"user_id": user_id}
            )
            
            await user_orchestrator.close()
            
            return SuccessResponse(
                message="Senha alterada com sucesso",
                data={"password_changed": True}
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error changing password: {str(e)}", exc_info=e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal error during password change"
            )


@router.get(
    "/me",
    response_model=UsuarioResponse,
    summary="Dados do Usuário Atual",
    description="Retorna dados do usuário autenticado"
)
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Obtém dados do usuário autenticado.
    
    Args:
        credentials: Token de autorização
        
    Returns:
        UsuarioResponse: Dados do usuário
        
    Raises:
        HTTPException: Se token inválido
    """
    async with RequestLogger("get_current_user"):
        try:
            access_token = credentials.credentials
            
            # Em implementação real, validaria token e obteria user_id
            user_id = "user_id_from_token"  # Placeholder
            
            user_orchestrator = UserOrchestrator()
            persistence_gateway = user_orchestrator.persistence_gateway
            
            user_response = await persistence_gateway.get_user(user_id)
            
            if not user_response.success:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            
            # Remove senha dos dados
            user_data = user_response.data.copy()
            user_data.pop("senha", None)
            
            await user_orchestrator.close()
            
            return UsuarioResponse(**user_data)
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting current user: {str(e)}", exc_info=e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal error retrieving user data"
            )


# Dependency para validar token e obter usuário atual
async def get_current_user_dependency(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """
    Dependency para validar token e obter usuário atual.
    
    Args:
        credentials: Token de autorização
        
    Returns:
        dict: Dados do usuário autenticado
        
    Raises:
        HTTPException: Se token inválido
    """
    try:
        access_token = credentials.credentials
        
        # Em implementação real, validaria token JWT
        # e extrairia dados do usuário
        
        # Placeholder - implementação simplificada
        user_data = {
            "id": "user_id_from_token",
            "email": "user@example.com",
            "nome": "Usuário Exemplo",
            "tipo_usuario": "student"
        }
        
        return user_data
        
    except Exception as e:
        logger.error(f"Token validation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )