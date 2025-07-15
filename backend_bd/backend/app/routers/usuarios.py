from fastapi import APIRouter

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@router.get("/")
def listar_usuarios():
    return ["Usuário 1", "Usuário 2"]