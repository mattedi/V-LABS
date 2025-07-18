from fastapi import FastAPI
from app.routers import usuarios, perguntas, respostas, embeddings, avaliacoes, logs

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
app.include_router(respostas.router)
app.include_router(embeddings.router)
app.include_router(avaliacoes.router)
app.include_router(logs.router)

# Rota de saúde para verificar se a API está funcionando

# Rota básica de saúde
@app.get("/")
def root():
    return {"mensagem": "API está no ar"}

