// src/context/ProgressContext.tsx
// Contexto de progresso - gerencia o progresso do usuário em diferentes modos de tutoria
// Permite atualizar progresso, gerar recomendações e calcular progresso geral.
// Este arquivo define o contexto de progresso, que é usado para gerenciar o progresso do usuário
// em diferentes modos de tutoria (equação, voz, imagem, texto) em uma aplicação React.
// Ele permite que qualquer componente envolvido pelo `ProgressProvider` acesse e manipule o progresso do usuário,
// além de gerar recomendações baseadas no progresso atual.

import React, { createContext, useContext, useState, useEffect } from 'react';

// Hook useLocalStorage simplificado (definido localmente)
function useLocalStorage<T>(key: string, initialValue: T): [T, React.Dispatch<React.SetStateAction<T>>] {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.error(`Erro ao ler localStorage para a chave "${key}":`, error);
      return initialValue;
    }
  });

  const setValue: React.Dispatch<React.SetStateAction<T>> = (value) => {
    try {
      const valueToStore = value instanceof Function ? value(storedValue) : value;
      setStoredValue(valueToStore);
      window.localStorage.setItem(key, JSON.stringify(valueToStore));
    } catch (error) {
      console.error(`Erro ao salvar no localStorage para a chave "${key}":`, error);
    }
  };

  return [storedValue, setValue];
}

// Definir tipos para TypeScript
interface ProgressItem {
  completed: number;
  totalAttempts: number;
  masteryLevel: 'iniciante' | 'intermediário' | 'avançado';
}

interface UserProgress {
  equation: ProgressItem;
  voice: ProgressItem;
  image: ProgressItem;
  text: ProgressItem;
}

interface ProgressUpdateResult {
  success: boolean;
  score?: number;
  timeSpent?: number;
}

interface RecommendedContent {
  id: number;
  mode: keyof UserProgress;
  title: string;
  difficulty: string;
}

interface ProgressContextType {
  userProgress: UserProgress;
  updateProgress: (mode: keyof UserProgress, result: ProgressUpdateResult) => void;
  recommendedContent: RecommendedContent[];
  getOverallProgress: () => number;
  resetProgress: () => void;
}

// Criar o contexto
const ProgressContext = createContext<ProgressContextType | null>(null);

const defaultProgress: UserProgress = {
  equation: { completed: 0, totalAttempts: 0, masteryLevel: 'iniciante' },
  voice: { completed: 0, totalAttempts: 0, masteryLevel: 'iniciante' },
  image: { completed: 0, totalAttempts: 0, masteryLevel: 'iniciante' },
  text: { completed: 0, totalAttempts: 0, masteryLevel: 'iniciante' }
};

export function ProgressProvider({ children }: { children: React.ReactNode }) {
  const [userProgress, setUserProgress] = useLocalStorage<UserProgress>('user-progress', defaultProgress);
  const [recommendedContent, setRecommendedContent] = useState<RecommendedContent[]>([]);

  // CORREÇÃO: Função updateProgress com tipagem mais segura
  const updateProgress = (mode: keyof UserProgress, result: ProgressUpdateResult) => {
    setUserProgress((prev: UserProgress) => {
      // CORREÇÃO: Garantir que o modo existe e criar uma cópia segura
      const currentProgress = prev[mode];
      if (!currentProgress) {
        console.warn(`Modo "${mode}" não encontrado no progresso`);
        return prev;
      }

      const newCompleted = result.success ? currentProgress.completed + 1 : currentProgress.completed;
      const newTotalAttempts = currentProgress.totalAttempts + 1;

      // CORREÇÃO: Criar objeto atualizado de forma mais segura
      const updatedProgress: UserProgress = {
        ...prev,
        [mode]: {
          completed: newCompleted,
          totalAttempts: newTotalAttempts,
          masteryLevel: calculateMasteryLevel(newCompleted, newTotalAttempts)
        }
      };

      return updatedProgress;
    });
  };

  // CORREÇÃO: Função com retorno tipado corretamente
  const calculateMasteryLevel = (completed: number, attempts: number): 'iniciante' | 'intermediário' | 'avançado' => {
    if (attempts === 0) return 'iniciante';

    const ratio = completed / attempts;
    if (ratio >= 0.8) return 'avançado';
    if (ratio >= 0.6) return 'intermediário';
    return 'iniciante';
  };

  const generateRecommendations = (): RecommendedContent[] => {
    if (!userProgress) return [];

    // CORREÇÃO: Usar Object.entries com tipagem correta
    const modes: (keyof UserProgress)[] = ['equation', 'voice', 'image', 'text'];
    
    const sortedAreas = modes
      .map((mode) => ({
        mode,
        data: userProgress[mode],
        ratio: userProgress[mode].totalAttempts > 0 
          ? userProgress[mode].completed / userProgress[mode].totalAttempts 
          : 0
      }))
      .sort((a, b) => a.ratio - b.ratio);

    const weakestArea = sortedAreas.length > 0 ? sortedAreas[0] : null;

    if (!weakestArea) return [];

    const modeNames = {
      equation: 'Equações',
      voice: 'Reconhecimento de Voz',
      image: 'Análise de Imagens',
      text: 'Compreensão de Texto'
    };

    return [
      {
        id: 1,
        mode: weakestArea.mode,
        title: `Melhorar em ${modeNames[weakestArea.mode]}`,
        difficulty: weakestArea.data.masteryLevel
      },
      {
        id: 2,
        mode: weakestArea.mode,
        title: `Exercícios de ${modeNames[weakestArea.mode]}`,
        difficulty: weakestArea.data.masteryLevel === 'iniciante' ? 'fácil' : 'médio'
      }
    ];
  };

  const getOverallProgress = (): number => {
    const modes: (keyof UserProgress)[] = ['equation', 'voice', 'image', 'text'];
    
    const totalCompleted = modes.reduce((sum, mode) => sum + userProgress[mode].completed, 0);
    const totalAttempts = modes.reduce((sum, mode) => sum + userProgress[mode].totalAttempts, 0);
    
    return totalAttempts > 0 ? Math.round((totalCompleted / totalAttempts) * 100) : 0;
  };

  const resetProgress = (): void => {
    setUserProgress(defaultProgress);
  };

  useEffect(() => {
    setRecommendedContent(generateRecommendations());
  }, [userProgress]);

  const value: ProgressContextType = {
    userProgress,
    updateProgress,
    recommendedContent,
    getOverallProgress,
    resetProgress
  };

  return (
    <ProgressContext.Provider value={value}>
      {children}
    </ProgressContext.Provider>
  );
}

export const useProgressContext = (): ProgressContextType => {
  const context = useContext(ProgressContext);
  if (!context) {
    throw new Error('useProgressContext deve ser usado dentro de um ProgressProvider');
  }
  return context;
};

// Hook adicional para usar progresso de um modo específico
export const useProgress = (mode: keyof UserProgress) => {
  const { userProgress, updateProgress } = useProgressContext();
  
  return {
    progress: userProgress[mode],
    updateProgress: (result: ProgressUpdateResult) => updateProgress(mode, result),
    completionRate: userProgress[mode].totalAttempts > 0 
      ? Math.round((userProgress[mode].completed / userProgress[mode].totalAttempts) * 100)
      : 0
  };
};

// Componente para exibir progresso
export const ProgressDisplay: React.FC<{ mode: keyof UserProgress }> = ({ mode }) => {
  const { progress, completionRate } = useProgress(mode);
  
  const modeNames = {
    equation: 'Equações',
    voice: 'Voz',
    image: 'Imagem',
    text: 'Texto'
  };

  const levelColors = {
    iniciante: 'text-red-600',
    intermediário: 'text-yellow-600',
    avançado: 'text-green-600'
  };

  return (
    <div className="bg-white p-4 rounded-lg shadow-md">
      <h3 className="font-semibold text-gray-800 mb-2">{modeNames[mode]}</h3>
      
      <div className="space-y-2">
        <div className="flex justify-between text-sm">
          <span>Nível:</span>
          <span className={`font-medium ${levelColors[progress.masteryLevel]}`}>
            {progress.masteryLevel}
          </span>
        </div>
        
        <div className="flex justify-between text-sm">
          <span>Progresso:</span>
          <span>{completionRate}%</span>
        </div>
        
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div 
            className="bg-blue-600 h-2 rounded-full transition-all duration-300"
            style={{ width: `${completionRate}%` }}
          ></div>
        </div>
        
        <div className="flex justify-between text-xs text-gray-500">
          <span>Corretos: {progress.completed}</span>
          <span>Total: {progress.totalAttempts}</span>
        </div>
      </div>
    </div>
  );
};

// EXTENSÕES:
// - Adicionar animações de transição ao atualizar o progresso.
// - Implementar um sistema de badges ou conquistas baseado no progresso.
// - Permitir que o usuário personalize as recomendações de conteúdo.
// - Adicionar suporte a múltiplos usuários com progresso separado.
// - (1) Implementar um gráfico de progresso visual usando uma biblioteca como Chart.js ou D3.js.
// - Adicionar notificações quando o usuário atingir novos níveis de maestria.
// - Implementar um sistema de feedback onde o usuário pode avaliar as recomendações recebidas.
// - Adicionar suporte a exportação de progresso para formatos como CSV ou JSON.
// - Implementar um sistema de gamificação onde o progresso desbloqueia novos conteúdos ou funcionalidades.
// - Adicionar suporte a integração com APIs externas para obter recomendações de conteúdo. 