from fastapi import FastAPI

app = FastAPI(
    title="Vibe Learning API - Minimal",
    version="1.0.0",
    description="Versão mínima para teste"
)

@app.get("/")
def root():
    return {"mensagem": "API funcionando!", "status": "OK"}

@app.get("/health")
def health():
    return {"status": "healthy"}
