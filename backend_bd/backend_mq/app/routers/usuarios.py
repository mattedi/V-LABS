# app/routers/usuarios.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from bson import ObjectId
from app.database.mongo import colecao_usuarios

router = APIRouter()

# Modelo de entrada
class Usuario(BaseModel):
    nome: str
    email: EmailStr

class UsuarioOut(Usuario):
    id: str

# Endpoint de saúde
@router.get("/usuarios/ping")
def ping():
    return {"mensagem": "Ping Usuario"}

# Criar novo usuário
@router.post("/usuarios/novo", response_model=UsuarioOut)
def criar_usuario(usuario: Usuario):
    result = colecao_usuarios.insert_one(usuario.dict())
    return {**usuario.dict(), "id": str(result.inserted_id)}

# Listar usuários
@router.get("/usuarios", response_model=List[UsuarioOut])
def listar_usuarios():
    usuarios = colecao_usuarios.find()
    return [
        {"id": str(u["_id"]), "nome": u["nome"], "email": u["email"]}
        for u in usuarios
    ]

# Atualizar usuário
@router.put("/usuarios/{usuario_id}")
def atualizar_usuario(usuario_id: str, usuario: Usuario):
    result = colecao_usuarios.update_one(
        {"_id": ObjectId(usuario_id)},
        {"$set": usuario.dict()}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {"mensagem": "Usuário atualizado"}

# Deletar usuário
@router.delete("/usuarios/{usuario_id}")
def deletar_usuario(usuario_id: str):
    result = colecao_usuarios.delete_one({"_id": ObjectId(usuario_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {"mensagem": "Usuário deletado"}
