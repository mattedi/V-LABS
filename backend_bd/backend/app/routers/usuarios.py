from fastapi import APIRouter

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"]
)

@router.get("/ping")
def ping_usuario():
    return {"status": "Usuários operando"}

