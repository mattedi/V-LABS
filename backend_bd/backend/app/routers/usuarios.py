from fastapi import APIRouter

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"]
)

@router.get("/listar_perguntas")
def listar_perguntas():
    return [
        {"id": 1, "pergunta": "O que é uma fraça?"},
        {"id": 2, "pergunta": "O que é num denominador?"},
        {"id": 3, "pergunta": "Como simplificar uma fração?"},
        {"id": 4, "pergunta": "O que é um número primo?"},
        {"id": 5, "pergunta": "Como calcular a média de um conjunto de números?"}]
