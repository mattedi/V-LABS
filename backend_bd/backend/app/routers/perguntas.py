from fastapi import APIRouter

router = APIRouter(prefix="/perguntas", tags=["perguntas"])

@router.get("/")
def listar_perguntas():
    return ["Pergunta 1", "Pergunta 2"]