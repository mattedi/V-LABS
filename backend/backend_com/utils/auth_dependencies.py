"""
Dependências de autenticação para FastAPI.
"""

from typing import Dict, Any
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .jwt_utils import verify_token

security = HTTPBearer()

async def get_current_user_from_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """Extrai usuário atual do token JWT."""
    token = credentials.credentials
    payload = verify_token(token, "access")
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado"
        )
    
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )
    
    return {"user_id": user_id}

async def get_current_user(
    current_user_data: Dict[str, Any] = Depends(get_current_user_from_token)
) -> Dict[str, Any]:
    """Obtém dados completos do usuário atual."""
    from ..orchestration.user_orchestrator import UserOrchestrator
    
    user_orchestrator = UserOrchestrator()
    try:
        user_id = current_user_data["user_id"]
        
        persistence_gateway = user_orchestrator.persistence_gateway
        result = await persistence_gateway.get_user(user_id)
        
        if not result.success:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuário não encontrado"
            )
        
        return result.data
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Erro ao obter dados do usuário"
        )
    finally:
        await user_orchestrator.close()
