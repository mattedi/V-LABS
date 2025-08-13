"""
Roteadores do backend_com com integração real ao backend_bd.

Este módulo centraliza todos os roteadores da aplicação com
endpoints funcionais que se comunicam com o backend_bd.
"""

from fastapi import APIRouter, HTTPException, status
import time
import os
import sys

# Import do cliente backend_bd
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.backend_bd_client import get_backend_bd_client

# ===============================================
# HEALTH ROUTER - Monitoramento e Saúde
# ===============================================

health_router = APIRouter(prefix="/health", tags=["Health"])

@health_router.get("/", summary="Health Check Básico")
async def health_check():
    """Verificação básica de saúde do serviço."""
    return {
        "status": "healthy",
        "service": "V-LABS Backend Communication",
        "version": "1.0.0",
        "timestamp": time.time(),
        "message": "Service is running successfully"
    }

@health_router.get("/detailed", summary="Health Check Detalhado")
async def health_detailed():
    """Verificação detalhada com informações do sistema."""
    
    # Testa integração com backend_bd
    bd_client = get_backend_bd_client()
    bd_health = await bd_client.health_check()
    
    return {
        "status": "healthy",
        "service": "V-LABS Backend Communication",
        "version": "1.0.0",
        "timestamp": time.time(),
        "uptime": "Service operational",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "components": {
            "backend_bd": {
                "status": bd_health.get("status", "unknown"),
                "response_time_ms": bd_health.get("response_time_ms"),
                "url": bd_health.get("url")
            },
            "cache": "not_implemented", 
            "external_apis": "not_configured"
        },
        "system": {
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}",
            "platform": os.name
        }
    }

# ===============================================
# AUTH ROUTER - Autenticação e Autorização
# ===============================================

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

@auth_router.get("/", summary="Informações de Autenticação")
async def auth_info():
    """Informações sobre os endpoints de autenticação disponíveis."""
    return {
        "service": "Authentication Service",
        "status": "development",
        "available_endpoints": {
            "login": "POST /auth/login - Autenticar usuário",
            "register": "POST /auth/register - Registrar novo usuário",
            "logout": "POST /auth/logout - Fazer logout",
            "refresh": "POST /auth/refresh - Renovar token",
            "profile": "GET /auth/me - Obter perfil do usuário"
        },
        "authentication_methods": [
            "JWT Bearer Token",
            "Session Based (planned)"
        ]
    }

@auth_router.post("/login", summary="Login de Usuário")
async def login(credentials: dict):
    """
    Endpoint de login com integração real ao backend_bd.
    
    Args:
        credentials: {"email": str, "password": str}
    """
    
    # Valida entrada básica
    if not credentials.get("email") or not credentials.get("password"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email e senha são obrigatórios"
        )
    
    # Autentica no backend_bd
    bd_client = get_backend_bd_client()
    result = await bd_client.authenticate_user(
        credentials["email"], 
        credentials["password"]
    )
    
    if result.get("success"):
        return {
            "message": "Login realizado com sucesso",
            "user": result.get("user"),
            "token": "jwt_token_placeholder",  # Implementar JWT real
            "status": "authenticated"
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=result.get("message", "Falha na autenticação")
        )

@auth_router.get("/me", summary="Perfil do Usuário")
async def get_profile():
    """Obter perfil do usuário autenticado."""
    return {
        "message": "Profile endpoint em desenvolvimento", 
        "status": "not_implemented",
        "requires": "Bearer token"
    }

# ===============================================
# USERS ROUTER - Gerenciamento de Usuários
# ===============================================

users_router = APIRouter(prefix="/users", tags=["Users"])

@users_router.get("/", summary="Listar Usuários")
async def list_users(limit: int = 10):
    """Lista usuários do sistema via backend_bd."""
    
    # Busca usuários no backend_bd
    bd_client = get_backend_bd_client()
    result = await bd_client.get_users(limit=limit)
    
    if result.get("success"):
        return {
            "users": result.get("users", []),
            "total": result.get("total", 0),
            "limit": limit,
            "source": "backend_bd",
            "status": "success"
        }
    else:
        # Se backend_bd não disponível, retorna dados mock
        return {
            "users": [],
            "total": 0,
            "limit": limit,
            "source": "mock_data",
            "status": "backend_bd_unavailable",
            "message": result.get("message", "Backend_BD não disponível")
        }

@users_router.get("/stats", summary="Estatísticas de Usuários")
async def users_stats():
    """Estatísticas básicas de usuários."""
    
    # Busca dados reais do backend_bd
    bd_client = get_backend_bd_client()
    users_result = await bd_client.get_users(limit=1000)  # Busca mais para estatísticas
    
    if users_result.get("success"):
        users = users_result.get("users", [])
        
        # Calcula estatísticas reais
        stats = {
            "total_users": len(users),
            "active_users": len([u for u in users if u.get("active", True)]),
            "user_types": {},
            "created_today": 0,  # Implementar lógica de data
            "source": "backend_bd"
        }
        
        # Conta tipos de usuário
        for user in users:
            user_type = user.get("type", "unknown")
            stats["user_types"][user_type] = stats["user_types"].get(user_type, 0) + 1
            
        return stats
    else:
        # Fallback para dados mock
        return {
            "total_users": 0,
            "active_users": 0,
            "user_types": {
                "students": 0,
                "teachers": 0,
                "admins": 0
            },
            "source": "mock_data",
            "status": "backend_bd_unavailable"
        }

# ===============================================
# EDUCATIONAL ROUTER - Conteúdo Educacional
# ===============================================

educational_router = APIRouter(prefix="/educational", tags=["Educational"])

@educational_router.get("/", summary="Informações Educacionais")
async def educational_info():
    """Informações sobre endpoints de conteúdo educacional."""
    return {
        "service": "Educational Content Service",
        "status": "development",
        "available_endpoints": {
            "questions": "GET /educational/questions - Listar perguntas",
            "create_question": "POST /educational/questions - Criar pergunta",
            "answers": "GET /educational/answers - Listar respostas",
            "create_answer": "POST /educational/answers - Criar resposta",
            "search": "GET /educational/search - Busca semântica",
            "integration_test": "GET /educational/integration-test - Teste de integração"
        },
        "features": [
            "Question & Answer System",
            "Semantic Search",
            "Content Categories",
            "User Ratings",
            "Progress Tracking",
            "Backend_BD Integration"
        ]
    }

@educational_router.get("/questions", summary="Listar Perguntas")
async def get_questions(limit: int = 10, offset: int = 0):
    """Lista perguntas educacionais do backend_bd."""
    
    # Busca perguntas no backend_bd
    bd_client = get_backend_bd_client()
    result = await bd_client.get_questions(limit=limit, offset=offset)
    
    if result.get("success"):
        return {
            "questions": result.get("questions", []),
            "total": result.get("total", 0),
            "limit": limit,
            "offset": offset,
            "source": "backend_bd",
            "status": "success"
        }
    else:
        # Fallback para dados mock se backend_bd não disponível
        return {
            "questions": [
                {
                    "id": 1,
                    "title": "Exemplo de pergunta mock",
                    "content": "Esta é uma pergunta de exemplo quando backend_bd não está disponível",
                    "author": "Sistema",
                    "created_at": time.time()
                }
            ],
            "total": 1,
            "limit": limit,
            "offset": offset,
            "source": "mock_data",
            "status": "backend_bd_unavailable",
            "message": result.get("message", "Backend_BD não disponível")
        }

@educational_router.post("/questions", summary="Criar Pergunta")
async def create_question(question_data: dict):
    """Cria uma nova pergunta via backend_bd."""
    
    # Valida dados básicos
    if not question_data.get("title") or not question_data.get("content"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Título e conteúdo são obrigatórios"
        )
    
    # Cria pergunta no backend_bd
    bd_client = get_backend_bd_client()
    result = await bd_client.create_question(question_data)
    
    if result.get("success"):
        return {
            "message": "Pergunta criada com sucesso",
            "question": result.get("question"),
            "status": "created"
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=result.get("message", "Erro ao criar pergunta")
        )

@educational_router.get("/integration-test", summary="Teste de Integração")
async def test_integration():
    """Testa integração completa com backend_bd."""
    
    bd_client = get_backend_bd_client()
    
    # Testa múltiplas operações
    tests = {
        "health_check": await bd_client.health_check(),
        "get_questions": await bd_client.get_questions(limit=1),
        "get_users": await bd_client.get_users(limit=1)
    }
    
    # Analisa resultados
    all_passed = all(
        test.get("status") == "healthy" or test.get("success") 
        for test in tests.values()
    )
    
    return {
        "backend_com_status": "ok",
        "backend_bd_integration": "working" if all_passed else "failed",
        "test_results": tests,
        "overall_status": "passed" if all_passed else "failed",
        "tested_at": time.time()
    }

@educational_router.get("/search", summary="Busca Semântica")
async def semantic_search(query: str = ""):
    """Endpoint de busca semântica - implementação futura."""
    return {
        "results": [],
        "query": query,
        "status": "not_implemented",
        "message": "Semantic search em desenvolvimento"
    }

# ===============================================
# CONFIGURAÇÃO E EXPORTAÇÃO
# ===============================================

# Lista de todos os roteadores exportados
__all__ = [
    "health_router",
    "auth_router",
    "users_router", 
    "educational_router"
]

print("✅ Todos os roteadores carregados com integração backend_bd!")
print("📍 Health: /health")
print("🔐 Auth: /auth") 
print("👥 Users: /users")
print("📚 Educational: /educational")
print("🔗 Integration: /educational/integration-test")