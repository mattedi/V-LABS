from fastapi import FastAPI
from app.routers import usuarios, perguntas

app = FastAPI()

app.include_router(usuarios.router)
app.include_router(perguntas.router)