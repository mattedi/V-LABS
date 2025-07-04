// src/hooks/useAiFeedback.ts - VERSÃO SIMPLIFICADA E FUNCIONAL
import { useState } from 'react';

// Tipos locais (sem import externo)
interface AiFeedback {
  score: number;
  feedback: string;
  strengths: string[];
  areasToImprove: string[];
  nextSteps: string[];
}

interface AnalysisRequest {
  contentId: string;
  userResponse: string;
  mode: 'equation' | 'voice' | 'image' | 'text';
  metadata?: {
    userId?: string;
    timestamp?: string;
    timeSpent?: number;
    attempts?: number;
    difficulty?: string;
  };
}

export function useAiFeedback() {
  const [feedback, setFeedback] = useState<AiFeedback | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Simulação do serviço de IA (substitui aiService.analyzeResponse)
  const simulateAiAnalysis = async (request: AnalysisRequest): Promise<AiFeedback> => {
    // Simular delay da API
    await new Promise(resolve => setTimeout(resolve, 1500));

    // Simular possível erro (5% de chance)
    if (Math.random() < 0.05) {
      throw new Error('Erro na análise da IA');
    }

    // Gerar feedback baseado no modo
    const feedbackByMode = {
      equation: {
        feedback: 'Sua abordagem para resolver equações está melhorando. Continue praticando!',
        strengths: ['Raciocínio lógico', 'Aplicação de fórmulas'],
        areasToImprove: ['Velocidade de cálculo', 'Verificação de resultados'],
        nextSteps: ['Praticar equações mais complexas', 'Revisar propriedades algébricas']
      },
      voice: {
        feedback: 'Sua pronúncia está clara e bem articulada. Ótimo progresso!',
        strengths: ['Clareza na fala', 'Boa entonação'],
        areasToImprove: ['Velocidade da fala', 'Vocabulário técnico'],
        nextSteps: ['Praticar apresentações', 'Expandir vocabulário']
      },
      image: {
        feedback: 'Você demonstra boa capacidade de interpretação visual.',
        strengths: ['Atenção aos detalhes', 'Percepção visual'],
        areasToImprove: ['Análise contextual', 'Interpretação simbólica'],
        nextSteps: ['Analisar imagens mais complexas', 'Estudar semiótica']
      },
      text: {
        feedback: 'Sua compreensão textual está se desenvolvendo bem.',
        strengths: ['Interpretação literal', 'Identificação de ideias principais'],
        areasToImprove: ['Análise crítica', 'Síntese de informações'],
        nextSteps: ['Ler textos mais complexos', 'Praticar resumos']
      }
    };

    const modeData = feedbackByMode[request.mode];
    const baseScore = 60;
    const randomBonus = Math.floor(Math.random() * 30);

    return {
      score: baseScore + randomBonus,
      feedback: modeData.feedback,
      strengths: modeData.strengths,
      areasToImprove: modeData.areasToImprove,
      nextSteps: modeData.nextSteps
    };
  };

  const requestAnalysis = async (
    contentId: string,
    userResponse: string,
    mode: 'equation' | 'voice' | 'image' | 'text',
    metadata?: any
  ): Promise<void> => {
    setIsLoading(true);
    setError(null);

    try {
      const request: AnalysisRequest = {
        contentId,
        userResponse,
        mode,
        metadata: {
          timestamp: new Date().toISOString(),
          userId: 'current-user', // Simplificado
          ...metadata
        }
      };

      const result = await simulateAiAnalysis(request);
      
      // Normalizar resultado para garantir arrays
      const normalizedResult: AiFeedback = {
        score: result.score || 0,
        feedback: result.feedback || 'Análise em processamento...',
        strengths: Array.isArray(result.strengths) ? result.strengths : [],
        areasToImprove: Array.isArray(result.areasToImprove) ? result.areasToImprove : [],
        nextSteps: Array.isArray(result.nextSteps) ? result.nextSteps : []
      };

      setFeedback(normalizedResult);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Erro ao solicitar análise';
      setError(errorMessage);
      console.error('Erro na análise de IA:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const clearFeedback = (): void => {
    setFeedback(null);
    setError(null);
  };

  // Função para obter feedback rápido sem loading
  const getQuickFeedback = (mode: 'equation' | 'voice' | 'image' | 'text'): AiFeedback => {
    const quickFeedback = {
      equation: {
        score: 75,
        feedback: 'Boa resolução! Continue praticando.',
        strengths: ['Método correto'],
        areasToImprove: ['Velocidade'],
        nextSteps: ['Mais exercícios']
      },
      voice: {
        score: 80,
        feedback: 'Pronúncia clara e bem articulada.',
        strengths: ['Clareza'],
        areasToImprove: ['Fluência'],
        nextSteps: ['Mais prática']
      },
      image: {
        score: 70,
        feedback: 'Boa interpretação visual.',
        strengths: ['Observação'],
        areasToImprove: ['Análise'],
        nextSteps: ['Mais exemplos']
      },
      text: {
        score: 85,
        feedback: 'Excelente compreensão textual.',
        strengths: ['Interpretação'],
        areasToImprove: ['Síntese'],
        nextSteps: ['Textos complexos']
      }
    };

    return quickFeedback[mode];
  };

  // Função para retry em caso de erro
  const retryAnalysis = async (): Promise<void> => {
    if (error) {
      setError(null);
      // Re-executar a última análise se houver dados
      // Por simplicidade, apenas limpar o erro
      console.log('Tentando novamente...');
    }
  };

  return {
    feedback,
    isLoading,
    error,
    requestAnalysis,
    clearFeedback,
    getQuickFeedback,
    retryAnalysis
  };
}

// Hook especializado para feedback de equações
export function useEquationFeedback() {
  const { 
    feedback, 
    isLoading, 
    error, 
    requestAnalysis, 
    clearFeedback 
  } = useAiFeedback();

  const analyzeMathSolution = async (
    equation: string, 
    solution: string,
    steps?: string[]
  ): Promise<void> => {
    const contentId = `equation-${Date.now()}`;
    const userResponse = `Equação: ${equation}, Solução: ${solution}`;
    
    await requestAnalysis(contentId, userResponse, 'equation', {
      equation,
      solution,
      steps,
      timeSpent: Date.now()
    });
  };

  return {
    feedback,
    isAnalyzing: isLoading,
    error,
    analyzeMathSolution,
    clearFeedback
  };
}

// Hook especializado para feedback de voz
export function useVoiceFeedback() {
  const { 
    feedback, 
    isLoading, 
    error, 
    requestAnalysis, 
    clearFeedback 
  } = useAiFeedback();

  const analyzeVoiceRecording = async (
    audioData: string,
    transcription?: string,
    duration?: number
  ): Promise<void> => {
    const contentId = `voice-${Date.now()}`;
    const userResponse = transcription || 'Gravação de áudio';
    
    await requestAnalysis(contentId, userResponse, 'voice', {
      audioData,
      transcription,
      duration,
      timestamp: new Date().toISOString()
    });
  };

  return {
    feedback,
    isAnalyzing: isLoading,
    error,
    analyzeVoiceRecording,
    clearFeedback
  };
}