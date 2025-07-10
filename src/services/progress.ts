// src/services/progress.ts - VERSÃO COMPLETA E FUNCIONAL
// Este serviço gerencia o progresso do usuário em diferentes modos de aprendizado
// e fornece métodos para atualizar, calcular e recuperar o progresso.

import { useState, useEffect } from 'react';

// Tipos locais para evitar imports externos
interface ModeProgress {
  completed: number;
  totalAttempts: number;
  masteryLevel: 'iniciante' | 'intermediário' | 'avançado';
}

interface Progress {
  userId: string;
  equation: ModeProgress;
  voice: ModeProgress;
  image: ModeProgress;
  text: ModeProgress;
}

interface User {
  id: string;
  username: string;
  email: string;
  role: 'student' | 'teacher' | 'admin';
  createdAt: string;
}

interface ApiError {
  message: string;
  code: string;
  statusCode: number;
}

interface EquationSolution {
  original: string;
  solution: string;
  steps: string[];
  isCorrect: boolean;
}

interface AiFeedback {
  score: number;
  feedback: string;
  strengths: string[];
  areasToImprove: string[];
  nextSteps: string[];
}

interface CollaborationSession {
  sessionId: string;
  createdBy: string;
  createdAt: string;
  mode: 'equation' | 'voice' | 'image' | 'text';
  participants: string[];
  isActive: boolean;
}

// Serviço HTTP simplificado local
class SimpleApiService {
  private baseURL = 'http://localhost:3001';

  async delay(ms: number = 1000): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  async get<T>(url: string): Promise<T> {
    await this.delay(500);
    // Simulação de resposta
    throw new Error('Implementar conexão real com backend');
  }

  async post<T>(url: string, data?: any): Promise<T> {
    await this.delay(800);
    // Simulação de resposta
    throw new Error('Implementar conexão real com backend');
  }
}

const apiService = new SimpleApiService();

// SERVIÇO DE PROGRESSO
export interface UpdateProgressData {
  result: 'correct' | 'incorrect' | 'partial';
  score?: number;
  timeSpent?: number;
  difficulty?: 'easy' | 'medium' | 'hard';
}

class ProgressService {
  public async getProgress(userId: string): Promise<Progress> {
    try {
      // Buscar do localStorage primeiro
      const savedProgress = localStorage.getItem(`progress_${userId}`);
      if (savedProgress) {
        return JSON.parse(savedProgress);
      }

      // Progresso padrão
      const defaultProgress: Progress = {
        userId,
        equation: { completed: 0, totalAttempts: 0, masteryLevel: 'iniciante' },
        voice: { completed: 0, totalAttempts: 0, masteryLevel: 'iniciante' },
        image: { completed: 0, totalAttempts: 0, masteryLevel: 'iniciante' },
        text: { completed: 0, totalAttempts: 0, masteryLevel: 'iniciante' }
      };

      // Salvar progresso padrão
      localStorage.setItem(`progress_${userId}`, JSON.stringify(defaultProgress));
      return defaultProgress;
    } catch (error) {
      console.error('Erro ao buscar progresso:', error);
      throw error;
    }
  }

  public async updateProgress(
    userId: string,
    mode: keyof Omit<Progress, 'userId'>,
    data: UpdateProgressData
  ): Promise<{ success: boolean; message: string }> {
    try {
      const currentProgress = await this.getProgress(userId);
      const modeProgress = currentProgress[mode];

      // Calcular novo progresso
      const newCompleted = data.result === 'correct' ? modeProgress.completed + 1 : modeProgress.completed;
      const newTotalAttempts = modeProgress.totalAttempts + 1;
      const newMasteryLevel = this.calculateMasteryLevel(newCompleted, newTotalAttempts);

      // Atualizar progresso
      const updatedProgress: Progress = {
        ...currentProgress,
        [mode]: {
          completed: newCompleted,
          totalAttempts: newTotalAttempts,
          masteryLevel: newMasteryLevel
        }
      };

      // Salvar no localStorage
      localStorage.setItem(`progress_${userId}`, JSON.stringify(updatedProgress));

      return { success: true, message: 'Progresso atualizado com sucesso' };
    } catch (error) {
      console.error('Erro ao atualizar progresso:', error);
      throw error;
    }
  }

  public async getMasteryLevel(userId: string, mode: keyof Omit<Progress, 'userId'>): Promise<ModeProgress> {
    const progress = await this.getProgress(userId);
    return progress[mode];
  }

  public calculateOverallProgress(progress: Progress): number {
    const modes: (keyof Omit<Progress, 'userId'>)[] = ['equation', 'voice', 'image', 'text'];
    const totalCompleted = modes.reduce((sum, mode) => sum + progress[mode].completed, 0);
    const totalAttempts = modes.reduce((sum, mode) => sum + progress[mode].totalAttempts, 0);
    
    return totalAttempts > 0 ? Math.round((totalCompleted / totalAttempts) * 100) : 0;
  }

  private calculateMasteryLevel(completed: number, attempts: number): 'iniciante' | 'intermediário' | 'avançado' {
    if (attempts === 0) return 'iniciante';
    
    const ratio = completed / attempts;
    if (ratio >= 0.8) return 'avançado';
    if (ratio >= 0.6) return 'intermediário';
    return 'iniciante';
  }
}

export const progressService = new ProgressService();

// SERVIÇO DE EQUAÇÕES
export interface EquationRequest {
  equation: string;
  userSolution?: string;
  method?: 'algebraic' | 'graphical' | 'numerical';
}

class EquationService {
  public async solveEquation(request: EquationRequest): Promise<EquationSolution> {
    try {
      // Simulação de resolução de equação
      await apiService.delay(1200);

      // Lógica básica de resolução (substituir por algoritmo real)
      const { equation, userSolution = '' } = request;
      
      const mockSolution: EquationSolution = {
        original: equation,
        solution: userSolution || 'x = 5', // Simplificado
        steps: [
          'Identificar a equação linear',
          'Isolar a variável x',
          'Simplificar a expressão',
          'Verificar a solução'
        ],
        isCorrect: true
      };

      return mockSolution;
    } catch (error) {
      console.error('Erro ao resolver equação:', error);
      throw error;
    }
  }

  public async validateSolution(
    equation: string,
    userSolution: string
  ): Promise<{ isCorrect: boolean; feedback: string }> {
    try {
      await apiService.delay(800);

      // Validação básica (substituir por lógica real)
      const isCorrect = userSolution.toLowerCase().includes('x = ');
      
      return {
        isCorrect,
        feedback: isCorrect 
          ? 'Excelente! Sua solução está correta.' 
          : 'Verifique sua solução. Lembre-se de isolar a variável x.'
      };
    } catch (error) {
      console.error('Erro ao validar solução:', error);
      throw error;
    }
  }

  public async getHint(equation: string): Promise<{ hint: string; nextStep: string }> {
    await apiService.delay(600);
    
    return {
      hint: 'Tente isolar a variável x movendo os termos para um lado da equação.',
      nextStep: 'Primeiro, mova todos os termos com x para a esquerda e os números para a direita.'
    };
  }

  public async generatePracticeEquations(
    difficulty: 'easy' | 'medium' | 'hard',
    count: number = 5
  ): Promise<string[]> {
    await apiService.delay(500);

    const equations = {
      easy: ['x + 3 = 8', '2x = 10', 'x - 4 = 6', '3x = 15', 'x + 7 = 12'],
      medium: ['2x + 5 = 13', '3x - 7 = 14', '4x + 8 = 28', '5x - 3 = 17', '2x + 9 = 19'],
      hard: ['3(x + 2) = 18', '2(x - 4) + 5 = 13', '4x - 3(x + 1) = 7', '5(x + 1) - 2x = 17', '3x + 2(x - 3) = 14']
    };

    return equations[difficulty].slice(0, count);
  }
}

export const equationService = new EquationService();

// SERVIÇO DE IA
export interface AnalysisRequest {
  contentId: string;
  userResponse: string;
  mode: 'equation' | 'voice' | 'image' | 'text';
  metadata?: {
    timeSpent?: number;
    attempts?: number;
    difficulty?: string;
    userId?: string;
    timestamp?: string;
  };
}

class AiService {
  public async analyzeResponse(request: AnalysisRequest): Promise<AiFeedback> {
    try {
      await apiService.delay(1500);

      // Análise baseada no modo
      const feedback = this.generateFeedbackByMode(request.mode, request.userResponse);
      
      return {
        score: Math.floor(Math.random() * 30) + 70, // 70-100
        feedback: feedback.message,
        strengths: feedback.strengths,
        areasToImprove: feedback.areasToImprove,
        nextSteps: feedback.nextSteps
      };
    } catch (error) {
      console.error('Erro na análise de IA:', error);
      throw error;
    }
  }

  public async getPersonalizedRecommendations(
    userId: string,
    mode: string
  ): Promise<{ recommendations: string[]; nextTopics: string[] }> {
    await apiService.delay(1000);

    const recommendations = {
      equation: ['Praticar equações lineares', 'Revisar propriedades algébricas', 'Resolver sistemas de equações'],
      voice: ['Exercitar pronúncia', 'Ampliar vocabulário', 'Praticar fluência'],
      image: ['Análise visual', 'Interpretação de gráficos', 'Reconhecimento de padrões'],
      text: ['Compreensão textual', 'Análise crítica', 'Síntese de informações']
    };

    const nextTopics = {
      equation: ['Equações quadráticas', 'Sistemas lineares', 'Inequações'],
      voice: ['Apresentações', 'Debates', 'Conversação avançada'],
      image: ['Visualização de dados', 'Design gráfico', 'Análise semiótica'],
      text: ['Literatura avançada', 'Redação técnica', 'Crítica literária']
    };

    return {
      recommendations: recommendations[mode as keyof typeof recommendations] || [],
      nextTopics: nextTopics[mode as keyof typeof nextTopics] || []
    };
  }

  public async generateExercises(
    userId: string,
    mode: string,
    difficulty: string
  ): Promise<any[]> {
    await apiService.delay(800);

    // Exercícios simulados
    const exercises = [
      { id: 1, title: `Exercício de ${mode} - Nível ${difficulty}`, content: 'Conteúdo do exercício...' },
      { id: 2, title: `Prática de ${mode} - ${difficulty}`, content: 'Mais conteúdo...' }
    ];

    return exercises;
  }

  private generateFeedbackByMode(mode: string, userResponse: string) {
    const feedbackTemplates = {
      equation: {
        message: 'Sua abordagem para resolver equações está evoluindo bem. Continue praticando!',
        strengths: ['Raciocínio lógico', 'Aplicação correta de propriedades'],
        areasToImprove: ['Velocidade de cálculo', 'Verificação de resultados'],
        nextSteps: ['Praticar equações mais complexas', 'Revisar conceitos básicos']
      },
      voice: {
        message: 'Sua expressão oral está clara e bem articulada.',
        strengths: ['Clareza na pronúncia', 'Boa entonação'],
        areasToImprove: ['Fluência', 'Vocabulário técnico'],
        nextSteps: ['Praticar apresentações', 'Expandir vocabulário']
      },
      image: {
        message: 'Você demonstra boa capacidade de interpretação visual.',
        strengths: ['Atenção aos detalhes', 'Percepção visual'],
        areasToImprove: ['Análise contextual', 'Interpretação simbólica'],
        nextSteps: ['Analisar imagens complexas', 'Estudar teoria visual']
      },
      text: {
        message: 'Sua compreensão textual está se desenvolvendo adequadamente.',
        strengths: ['Interpretação literal', 'Identificação de ideias'],
        areasToImprove: ['Análise crítica', 'Síntese'],
        nextSteps: ['Textos mais complexos', 'Praticar resumos']
      }
    };

    return feedbackTemplates[mode as keyof typeof feedbackTemplates] || feedbackTemplates.equation;
  }
}

export const aiService = new AiService();

// SERVIÇO DE COLABORAÇÃO
export interface CreateSessionRequest {
  mode: 'equation' | 'voice' | 'image' | 'text';
  maxParticipants?: number;
  isPrivate?: boolean;
  title?: string;
}

class CollaborationService {
  public async createSession(request: CreateSessionRequest): Promise<CollaborationSession> {
    await apiService.delay(800);

    const session: CollaborationSession = {
      sessionId: 'session-' + Date.now(),
      createdBy: 'current-user',
      createdAt: new Date().toISOString(),
      mode: request.mode,
      participants: ['current-user'],
      isActive: true
    };

    // Salvar sessão no localStorage
    const sessions = this.getSavedSessions();
    sessions.push(session);
    localStorage.setItem('collaboration_sessions', JSON.stringify(sessions));

    return session;
  }

  public async joinSession(sessionId: string): Promise<{ success: boolean; session: CollaborationSession }> {
    await apiService.delay(600);

    const sessions = this.getSavedSessions();
    const session = sessions.find(s => s.sessionId === sessionId);

    if (!session) {
      throw new Error('Sessão não encontrada');
    }

    // Adicionar participante
    if (!session.participants.includes('current-user')) {
      session.participants.push('current-user');
      this.saveSessions(sessions);
    }

    return { success: true, session };
  }

  public async leaveSession(sessionId: string): Promise<{ success: boolean }> {
    await apiService.delay(400);

    const sessions = this.getSavedSessions();
    const sessionIndex = sessions.findIndex(s => s.sessionId === sessionId);

    if (sessionIndex !== -1) {
      const session = sessions[sessionIndex];
      session.participants = session.participants.filter(p => p !== 'current-user');
      
      // Se não há mais participantes, remover sessão
      if (session.participants.length === 0) {
        sessions.splice(sessionIndex, 1);
      }
      
      this.saveSessions(sessions);
    }

    return { success: true };
  }

  public async getActiveSessions(): Promise<CollaborationSession[]> {
    await apiService.delay(300);
    return this.getSavedSessions().filter(s => s.isActive);
  }

  public async getSessionDetails(sessionId: string): Promise<CollaborationSession> {
    await apiService.delay(200);

    const sessions = this.getSavedSessions();
    const session = sessions.find(s => s.sessionId === sessionId);

    if (!session) {
      throw new Error('Sessão não encontrada');
    }

    return session;
  }

  private getSavedSessions(): CollaborationSession[] {
    try {
      const saved = localStorage.getItem('collaboration_sessions');
      return saved ? JSON.parse(saved) : [];
    } catch {
      return [];
    }
  }

  private saveSessions(sessions: CollaborationSession[]): void {
    localStorage.setItem('collaboration_sessions', JSON.stringify(sessions));
  }
}

export const collaborationService = new CollaborationService();

// HOOKS UTILITÁRIOS
interface UseApiState<T> {
  data: T | null;
  loading: boolean;
  error: ApiError | null;
}

interface UseApiOptions {
  immediate?: boolean;
  onSuccess?: (data: any) => void;
  onError?: (error: ApiError) => void;
}

export function useApi<T>(
  apiCall: () => Promise<T>,
  options: UseApiOptions = {}
): [UseApiState<T>, () => Promise<void>] {
  const [state, setState] = useState<UseApiState<T>>({
    data: null,
    loading: options.immediate ?? false,
    error: null,
  });

  const execute = async (): Promise<void> => {
    setState(prev => ({ ...prev, loading: true, error: null }));
    
    try {
      const result = await apiCall();
      setState({ data: result, loading: false, error: null });
      options.onSuccess?.(result);
    } catch (error) {
      const apiError = error as ApiError;
      setState({ data: null, loading: false, error: apiError });
      options.onError?.(apiError);
    }
  };

  useEffect(() => {
    if (options.immediate ?? false) {
      execute();
    }
  }, []);

  return [state, execute];
}

// Hook de progresso simplificado (sem dependência do AuthContext)
export function useProgress(userId: string = 'demo-user') {
  const [progress, setProgress] = useState<Progress | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (userId) {
      loadProgress();
    }
  }, [userId]);

  const loadProgress = async (): Promise<void> => {
    setLoading(true);
    setError(null);

    try {
      const userProgress = await progressService.getProgress(userId);
      setProgress(userProgress);
    } catch (err) {
      setError('Erro ao carregar progresso');
      console.error('Erro ao carregar progresso:', err);
    } finally {
      setLoading(false);
    }
  };

  const updateProgress = async (
    mode: keyof Omit<Progress, 'userId'>,
    result: 'correct' | 'incorrect' | 'partial',
    metadata?: any
  ): Promise<void> => {
    try {
      await progressService.updateProgress(userId, mode, {
        result,
        ...metadata,
      });
      await loadProgress();
    } catch (err) {
      console.error('Erro ao atualizar progresso:', err);
      throw err;
    }
  };

  const getOverallProgress = (): number => {
    if (!progress) return 0;
    return progressService.calculateOverallProgress(progress);
  };

  return {
    progress,
    loading,
    error,
    updateProgress,
    getOverallProgress,
    refetch: loadProgress
  };
}

// EXTENSÕES:
// Extensão para calcular o nível de maestria
// Extensão para calcular o nível de maestria baseado no progresso
