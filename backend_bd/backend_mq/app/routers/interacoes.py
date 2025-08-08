from fastapi import APIRouter, HTTPException, Query, status
from app.schemas import InteractionCreate
from app.database.mongo import salvar_interacao, obter_interacoes
from datetime import datetime
import logging
from typing import List, Dict, Optional, Protocol
from bson import ObjectId

# === CONFIGURAÇÃO DO ROUTER ===
router = APIRouter(prefix="/interacoes", tags=["interacoes"])
logger = logging.getLogger(__name__)

# === PROTOCOLO PARA TIPAGEM ===
class EmbeddingModel(Protocol):
    """Protocolo para modelos de embedding - melhora tipagem."""
    model_name: str
    
    def encode(self, texts: str, **kwargs) -> List[float]:
        """Gera embedding para texto."""
        ...

# === IMPORTS COM FALLBACK MELHORADO ===
def _setup_embedding_services() -> tuple[EmbeddingModel, bool, callable]:
    """
    Configura serviços de embedding com fallback robusto.
    
    Returns:
        tuple: (modelo, disponibilidade, função_indexar)
    """
    try:
        from sentence_transformers import SentenceTransformer
        from app.database.qdrant_client import indexar_documento
        
        # Inicializar modelo de embeddings
        model = SentenceTransformer("all-MiniLM-L6-v2")
        logger.info("✅ Sentence Transformers e Qdrant disponíveis")
        
        return model, True, indexar_documento
        
    except ImportError as e:
        logger.warning(f"⚠️ Embeddings não disponíveis: {e}")
        logger.info("🔄 Usando implementação mock para desenvolvimento")
        
        # Mock melhorado com comportamento determinístico
        class MockSentenceTransformer:
            def __init__(self, model_name: str):
                self.model_name = f"mock-{model_name}"
            
            def encode(self, texts: str, **kwargs) -> List[float]:
                """Gera embedding mock determinístico baseado no hash do texto."""
                import hashlib
                import numpy as np
                
                # Seed determinístico baseado no conteúdo
                seed = int(hashlib.md5(texts.encode()).hexdigest()[:8], 16) % (2**32)
                np.random.seed(seed)
                return np.random.rand(384).tolist()
        
        def mock_indexar_documento(*args, **kwargs) -> str:
            """Mock para indexação no Qdrant."""
            logger.debug("Mock: Documento 'indexado' (Qdrant não disponível)")
            return f"mock_index_{datetime.utcnow().timestamp()}"
        
        model = MockSentenceTransformer("all-MiniLM-L6-v2")
        return model, False, mock_indexar_documento

# Configurar serviços uma única vez na inicialização
model, EMBEDDINGS_AVAILABLE, indexar_documento = _setup_embedding_services()

# === CONSTANTES ===
COLLECTION_NAME = "interacoes"
DEFAULT_LIMIT = 50
MAX_LIMIT = 200
EMBEDDING_DIMENSION = 384
MAX_TEXT_LENGTH = 500  # Para payload Qdrant

# === FUNÇÕES AUXILIARES MELHORADAS ===
def gerar_embedding(texto: str) -> List[float]:
    """
    Gera embedding para o texto fornecido.
    
    Args:
        texto: Texto para vetorização
        
    Returns:
        List[float]: Vetor embedding (384 dimensões)
        
    Raises:
        ValueError: Se texto inválido
    """
    if not texto or not isinstance(texto, str) or not texto.strip():
        logger.warning("Texto vazio ou inválido fornecido para embedding")
        return [0.0] * EMBEDDING_DIMENSION
    
    try:
        texto_limpo = texto.strip()[:1000]  # Limitar tamanho para evitar problemas
        vetor = model.encode(texto_limpo)
        
        # Garantir que é lista e tem dimensão correta
        if hasattr(vetor, 'tolist'):
            vetor = vetor.tolist()
        
        if len(vetor) != EMBEDDING_DIMENSION:
            logger.error(f"Dimensão do embedding incorreta: {len(vetor)} (esperado: {EMBEDDING_DIMENSION})")
            return [0.0] * EMBEDDING_DIMENSION
        
        logger.debug(f"Embedding gerado - texto: {len(texto_limpo)} chars, dimensões: {len(vetor)}")
        return vetor
        
    except Exception as e:
        logger.error(f"Erro ao gerar embedding: {e}")
        # Fallback para vetor zero em vez de aleatório (mais previsível)
        return [0.0] * EMBEDDING_DIMENSION

def processar_timestamp(timestamp_input) -> datetime:
    """
    Processa e valida timestamp de entrada com melhor tratamento de erros.
    
    Args:
        timestamp_input: Timestamp em vários formatos
        
    Returns:
        datetime: Timestamp processado e validado
    """
    if isinstance(timestamp_input, datetime):
        return timestamp_input
    
    if isinstance(timestamp_input, str):
        # Tentar múltiplos formatos
        formatos = [
            "%Y-%m-%dT%H:%M:%S.%fZ",      # ISO com microssegundos
            "%Y-%m-%dT%H:%M:%SZ",         # ISO básico
            "%Y-%m-%dT%H:%M:%S",          # ISO sem timezone
            "%Y-%m-%d %H:%M:%S",          # Formato brasileiro
        ]
        
        for formato in formatos:
            try:
                return datetime.strptime(timestamp_input, formato)
            except ValueError:
                continue
        
        # Último recurso: usar fromisoformat
        try:
            return datetime.fromisoformat(timestamp_input.replace('Z', '+00:00'))
        except ValueError:
            logger.warning(f"Formato de timestamp não reconhecido: {timestamp_input}")
    
    # Fallback para timestamp atual
    logger.info("Usando timestamp atual como fallback")
    return datetime.utcnow()

def validar_interacao(interacao: InteractionCreate) -> None:
    """
    Valida dados da interação com verificações mais robustas.
    
    Args:
        interacao: Dados da interação
        
    Raises:
        HTTPException: Se validação falhar
    """
    validacoes = [
        (not interacao.user_id or not interacao.user_id.strip(), 
         "user_id é obrigatório e não pode estar vazio"),
        (len(interacao.user_id.strip()) > 100, 
         "user_id muito longo (máximo 100 caracteres)"),
        (not interacao.pergunta or not interacao.pergunta.strip(), 
         "pergunta é obrigatória e não pode estar vazia"),
        (len(interacao.pergunta.strip()) < 3, 
         "pergunta muito curta (mínimo 3 caracteres)"),
        (len(interacao.pergunta.strip()) > 5000, 
         "pergunta muito longa (máximo 5000 caracteres)"),
        (not interacao.resposta or not interacao.resposta.strip(), 
         "resposta é obrigatória e não pode estar vazia"),
        (len(interacao.resposta.strip()) > 10000, 
         "resposta muito longa (máximo 10000 caracteres)")
    ]
    
    for condicao, mensagem in validacoes:
        if condicao:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=mensagem
            )

def converter_object_id(doc: Dict) -> Dict:
    """
    Converte ObjectId do MongoDB para string de forma segura.
    
    Args:
        doc: Documento do MongoDB
        
    Returns:
        Dict: Documento com ID convertido
    """
    if not isinstance(doc, dict):
        return doc
    
    doc_copy = doc.copy()
    if '_id' in doc_copy:
        doc_copy['id'] = str(doc_copy['_id'])
        del doc_copy['_id']
    
    return doc_copy

def preparar_payload_qdrant(interacao: InteractionCreate, mongo_id: str, timestamp: datetime) -> Dict:
    """
    Prepara payload otimizado para indexação no Qdrant.
    
    Args:
        interacao: Dados da interação
        mongo_id: ID gerado pelo MongoDB
        timestamp: Timestamp processado
        
    Returns:
        Dict: Payload formatado para Qdrant
    """
    return {
        "user_id": interacao.user_id.strip(),
        "pergunta": interacao.pergunta.strip()[:MAX_TEXT_LENGTH],
        "resposta": interacao.resposta.strip()[:MAX_TEXT_LENGTH],
        "timestamp": timestamp.isoformat(),
        "mongo_id": str(mongo_id),
        "complexidade": getattr(interacao, 'complexidade', None),
        "created_at": datetime.utcnow().isoformat(),
        "embedding_model": model.model_name
    }

# === ENDPOINTS ===

@router.post("/", 
             summary="Criar uma nova interação",
             description="Salva uma nova interação no MongoDB e indexa no Qdrant para busca semântica",
             response_model=Dict[str, str])
def criar_interacao(interacao: InteractionCreate):
    """
    Cria uma nova interação e a processa completamente.
    
    Processo:
    1. Valida dados de entrada
    2. Salva no MongoDB  
    3. Gera embedding da pergunta
    4. Indexa no Qdrant (se disponível)
    
    Args:
        interacao: Dados da interação
        
    Returns:
        Dict com status e ID da interação criada
        
    Raises:
        HTTPException: Em caso de erro de validação ou processamento
    """
    try:
        # 1. Validação rigorosa
        validar_interacao(interacao)
        logger.info(f"Processando interação para user_id: {interacao.user_id}")
        
        # 2. Preparar dados para MongoDB
        timestamp = processar_timestamp(getattr(interacao, 'timestamp', None))
        
        dados_mongo = {
            "user_id": interacao.user_id.strip(),
            "pergunta": interacao.pergunta.strip(),
            "resposta": interacao.resposta.strip(),
            "complexidade": getattr(interacao, 'complexidade', None),
            "timestamp": timestamp,
            "created_at": datetime.utcnow(),
            "metadata": {
                "embedding_model": model.model_name,
                "qdrant_available": EMBEDDINGS_AVAILABLE,
                "api_version": "v1.0"
            }
        }
        
        # Adicionar análise se disponível
        if hasattr(interacao, 'analise') and interacao.analise:
            dados_mongo["analise"] = {
                "pontos_fortes": getattr(interacao.analise, 'pontos_fortes', []),
                "aspectos_melhorar": getattr(interacao.analise, 'aspectos_melhorar', []),
                "passos_recomendados": getattr(interacao.analise, 'passos_recomendados', [])
            }
        
        # 3. Salvar no MongoDB
        logger.info("Salvando interação no MongoDB...")
        mongo_id = salvar_interacao(dados_mongo)
        
        if not mongo_id:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Falha ao salvar interação no banco de dados"
            )
        
        logger.info(f"Interação salva no MongoDB com ID: {mongo_id}")
        
        # 4. Processamento de embeddings 
        embedding_status = "skipped"
        try:
            logger.info("Gerando embedding da pergunta...")
            vetor = gerar_embedding(interacao.pergunta)
            
            if any(v != 0.0 for v in vetor):  # Verificar se não é vetor zero
                payload_qdrant = preparar_payload_qdrant(interacao, mongo_id, timestamp)
                
                logger.info("Indexando no Qdrant...")
                # Chamar função de indexação (funciona para mock e real)
                index_result = indexar_documento(COLLECTION_NAME, str(mongo_id), vetor, payload_qdrant)
                
                embedding_status = "success" if EMBEDDINGS_AVAILABLE else "mock"
                logger.info(f"Embedding indexado: {embedding_status} (result: {index_result})")
            else:
                embedding_status = "zero_vector"
                logger.warning("Vetor zero gerado - indexação pulada")
                
        except Exception as e:
            embedding_status = "failed"
            logger.error(f"Erro no processamento de embeddings: {e}")
            # Não falhar a requisição por problemas de embedding
        
        return {
            "status": "sucesso",
            "message": "Interação processada com sucesso",
            "id": str(mongo_id),
            "embedding_status": embedding_status,
            "timestamp": timestamp.isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Erro inesperado ao criar interação: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.get("/", 
            summary="Listar interações por usuário",
            description="Retorna histórico de conversas formatado para interface de chat",
            response_model=List[Dict])
def listar_interacoes(
    user_id: str = Query(..., description="ID do usuário", min_length=1),
    limite: int = Query(DEFAULT_LIMIT, description="Número máximo de interações", ge=1, le=MAX_LIMIT),
    formato: str = Query("chat", description="Formato de resposta: 'chat' ou 'raw'", regex="^(chat|raw)$")
) -> List[Dict]:
    """
    Lista interações de um usuário específico.
    
    Args:
        user_id: ID do usuário
        limite: Número máximo de interações a retornar
        formato: Formato da resposta ('chat' para UI, 'raw' para dados brutos)
        
    Returns:
        Lista de interações formatadas
        
    Raises:
        HTTPException: Em caso de erro
    """
    try:
        user_id_clean = user_id.strip()
        if not user_id_clean:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="user_id não pode estar vazio"
            )
        
        logger.info(f"Buscando interações para user_id: {user_id_clean}, limite: {limite}")
        
        # Buscar interações do banco
        interacoes_raw = obter_interacoes(user_id_clean, limite)
        
        if not interacoes_raw:
            logger.info(f"Nenhuma interação encontrada para user_id: {user_id_clean}")
            return []
        
        if formato == "raw":
            # Retornar dados brutos (apenas converter ObjectId)
            return [converter_object_id(doc) for doc in interacoes_raw]
        
        # Formato 'chat' - preparar para interface
        mensagens = []
        
        for doc in interacoes_raw:
            try:
                doc_convertido = converter_object_id(doc)
                timestamp = processar_timestamp(doc.get("timestamp"))
                
                # Mensagem do usuário
                mensagens.append({
                    "id": f"{doc_convertido['id']}-user",
                    "text": doc.get("pergunta", "").strip(),
                    "sender": "user", 
                    "timestamp": timestamp.isoformat(),
                    "complexidade": doc.get("complexidade"),
                    "interacao_id": doc_convertido['id']
                })
                
                # Resposta do assistente
                mensagens.append({
                    "id": f"{doc_convertido['id']}-assistant",
                    "text": doc.get("resposta", "").strip(),
                    "sender": "assistant",
                    "timestamp": timestamp.isoformat(),
                    "analise": doc.get("analise"),
                    "interacao_id": doc_convertido['id']
                })
                
            except Exception as e:
                logger.warning(f"Erro ao processar documento {doc.get('_id')}: {e}")
                continue
        
        # Ordenar por timestamp
        mensagens.sort(key=lambda m: m["timestamp"])
        
        logger.info(f"Retornando {len(mensagens)} mensagens para {len(interacoes_raw)} interações")
        return mensagens
        
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Erro ao listar interações para user_id={user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao recuperar histórico de interações"
        )

@router.get("/{interacao_id}",
            summary="Obter interação específica",
            description="Retorna uma interação específica por ID")
def obter_interacao_por_id(interacao_id: str):
    """
    Obtém uma interação específica por ID.
    
    Args:
        interacao_id: ID da interação
        
    Returns:
        Dados da interação
        
    Raises:
        HTTPException: Se interação não encontrada ou erro
    """
    try:
        if not interacao_id.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID da interação é obrigatório"
            )
        
        # Validar formato ObjectId
        try:
            ObjectId(interacao_id)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Formato de ID inválido"
            )
        
        from app.database.mongo import buscar_interacao_por_id
        interacao = buscar_interacao_por_id(interacao_id)
        
        if not interacao:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Interação não encontrada"
            )
        
        return converter_object_id(interacao)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Erro ao obter interação {interacao_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

@router.delete("/{interacao_id}",
               summary="Excluir interação",
               description="Remove uma interação do sistema")
def excluir_interacao(interacao_id: str):
    """
    Exclui uma interação específica.
    
    Args:
        interacao_id: ID da interação a ser excluída
        
    Returns:
        Confirmação de exclusão
        
    Raises:
        HTTPException: Se erro na exclusão
    """
    try:
        # Validar formato ObjectId
        try:
            ObjectId(interacao_id)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Formato de ID inválido"
            )
        
        from app.database.mongo import colecao_logs_interacao
        
        if not colecao_logs_interacao:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Serviço de banco de dados indisponível"
            )
        
        resultado = colecao_logs_interacao.delete_one({"_id": ObjectId(interacao_id)})
        
        if resultado.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Interação não encontrada"
            )
        
        logger.info(f"Interação {interacao_id} excluída com sucesso")
        return {"status": "sucesso", "message": "Interação excluída"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Erro ao excluir interação {interacao_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

# === ENDPOINT DE SAÚDE ===
@router.get("/health",
            summary="Status do serviço de interações",
            description="Verifica saúde do serviço e dependências")
def health_check():
    """Verifica status do serviço de interações."""
    try:
        from app.database.mongo import colecao_logs_interacao
        
        # Teste básico de conectividade MongoDB
        mongo_status = "connected"
        try:
            if colecao_logs_interacao:
                # Tentar operação simples
                colecao_logs_interacao.find_one({}, {"_id": 1})
            else:
                mongo_status = "disconnected"
        except Exception:
            mongo_status = "error"
        
        status_check = {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "services": {
                "mongodb": mongo_status,
                "embeddings": "available" if EMBEDDINGS_AVAILABLE else "mock",
                "qdrant": "available" if EMBEDDINGS_AVAILABLE else "unavailable"
            },
            "model_info": {
                "name": model.model_name,
                "type": "sentence_transformer" if EMBEDDINGS_AVAILABLE else "mock",
                "dimension": EMBEDDING_DIMENSION
            },
            "limits": {
                "default_limit": DEFAULT_LIMIT,
                "max_limit": MAX_LIMIT,
                "max_text_length": MAX_TEXT_LENGTH
            }
        }
        
        return status_check
        
    except Exception as e:
        logger.error(f"Erro no health check: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }