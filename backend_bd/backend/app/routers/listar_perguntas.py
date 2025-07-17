from fastapi import APIRouter

router = APIRouter(
    prefix="/perguntas",
    tags=["perguntas"]
)

@router.get("/listar")
def listar_perguntas():
    return [
        {"id": 1, "pergunta": "O que é uma fração?"},
        {"id": 2, "pergunta": "O que é um denominador?"},
        {"id": 3, "pergunta": "Como simplificar uma fração?"},
        {"id": 4, "pergunta": "O que é um número primo?"},
        {"id": 5, "pergunta": "Como calcular a média de um conjunto de números?"}
    ]
