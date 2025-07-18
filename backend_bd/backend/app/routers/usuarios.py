from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

# Modelo de entrada
class Usuario(BaseModel):
    id: Optional[int] = None
    nome: str
    email: str

# Simulando banco de dados
usuarios_db = []

@router.get("/usuarios/ping")
def ping():
    return {"mensagem": "Ping Usuario"}

@router.post("/usuarios/novo")
def criar_usuario(usuario: Usuario):
    usuarios_db.append(usuario)
    return {"mensagem": "Usuário criado", "usuario": usuario}

@router.put("/usuarios/{usuario_id}")
def atualizar_usuario(usuario_id: int, usuario: Usuario):
    for idx, u in enumerate(usuarios_db):
        if u.id == usuario_id:
            usuarios_db[idx] = usuario
            return {"mensagem": "Usuário atualizado", "usuario": usuario}
    return {"erro": "Usuário não encontrado"}

@router.delete("/usuarios/{usuario_id}")
def deletar_usuario(usuario_id: int):
    for idx, u in enumerate(usuarios_db):
        if u.id == usuario_id:
            del usuarios_db[idx]
            return {"mensagem": "Usuário deletado"}
    return {"erro": "Usuário não encontrado"}