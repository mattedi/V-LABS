from fastapi import FastAPI
from app.routers import usuarios, perguntas  # importa os módulos de rota

app = FastAPI(
    title="Vibe Learning API",
    version="1.0.0",
    description="API para tutoria multimodal com IA.",
    contact={
        "name": "Equipe V-LABS",
        "email": "contato@vlabs.ai",
        "url": "https://github.com/Vibe-Learning"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    }
)

# Inclusão dos módulos de rota
app.include_router(usuarios.router)
app.include_router(perguntas.router)

# Rota básica de saúde
@app.get("/")
def root():
    return {"mensagem": "API está no ar"}

