// src/pages/EquationPage.tsx 
//  Página de resolução de equações com feedback de IA
//  Permite que o usuário insira uma equação e sua solução,
//  e receba feedback detalhado sobre sua resposta
//  incluindo pontos fortes, áreas de melhoria e próximos passos sugeridos.

import React, { useState } from 'react';
import { useAiFeedback } from '../hooks/useAiFeedback';

// Componente AiFeedbackPanel local (elimina erro de import)
interface AiFeedback {
  score: number;
  feedback: string;
  strengths: string[];
  areasToImprove: string[];
  nextSteps: string[];
}

interface AiFeedbackPanelProps {
  analysisResult: AiFeedback | null;
  isLoading?: boolean;
  onRetry?: () => void;
}

const AiFeedbackPanel: React.FC<AiFeedbackPanelProps> = ({
  analysisResult,
  isLoading = false,
  onRetry
}) => {
  if (isLoading) {
    return (
      <div className="bg-white p-6 rounded-lg shadow-md">
        <div className="flex items-center justify-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <span className="ml-2 text-gray-600">Analisando resposta...</span>
        </div>
      </div>
    );
  }

  if (!analysisResult) {
    return (
      <div className="bg-white p-6 rounded-lg shadow-md">
        <div className="text-center text-gray-500">
          <p>Nenhuma análise disponível ainda.</p>
          {onRetry && (
            <button 
              onClick={onRetry}
              className="mt-2 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              Solicitar Análise
            </button>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow-md space-y-6">
      <h3 className="text-xl font-bold text-gray-800 mb-4">
        Feedback da IA
      </h3>

      {/* Score Section */}
      <div className="bg-blue-50 p-4 rounded-lg">
        <div className="flex items-center justify-between">
          <span className="text-lg font-semibold text-gray-700">Pontuação:</span>
          <span className="text-2xl font-bold text-blue-600">
            {analysisResult.score}%
          </span>
        </div>
      </div>

      {/* Feedback Section */}
      {analysisResult.feedback && (
        <div className="bg-gray-50 p-4 rounded-lg">
          <h4 className="font-semibold text-gray-700 mb-2">Feedback Geral:</h4>
          <p className="text-gray-600">{analysisResult.feedback}</p>
        </div>
      )}

      {/* Pontos Fortes */}
      <div className="mt-3">
        <h4 className="font-semibold text-green-600">Pontos Fortes:</h4>
        <ul className="list-disc pl-5 mt-1">
          {analysisResult.strengths && analysisResult.strengths.length > 0 ? (
            analysisResult.strengths.map((item, index) => (
              <li key={`strength-${index}`} className="text-gray-600">
                {item}
              </li>
            ))
          ) : (
            <li className="text-gray-500 italic">Nenhum ponto forte identificado ainda.</li>
          )}
        </ul>
      </div>

      {/* Áreas para Melhorar */}
      <div className="mt-3">
        <h4 className="font-semibold text-yellow-600">Áreas para Melhorar:</h4>
        <ul className="list-disc pl-5 mt-1">
          {analysisResult.areasToImprove && analysisResult.areasToImprove.length > 0 ? (
            analysisResult.areasToImprove.map((item, index) => (
              <li key={`improvement-${index}`} className="text-gray-600">
                {item}
              </li>
            ))
          ) : (
            <li className="text-gray-500 italic">Nenhuma área de melhoria identificada.</li>
          )}
        </ul>
      </div>

      {/* Próximos Passos */}
      <div className="mt-3">
        <h4 className="font-semibold text-blue-600">Próximos Passos:</h4>
        <ul className="list-disc pl-5 mt-1">
          {analysisResult.nextSteps && analysisResult.nextSteps.length > 0 ? (
            analysisResult.nextSteps.map((item, index) => (
              <li key={`next-step-${index}`} className="text-gray-600">
                {item}
              </li>
            ))
          ) : (
            <li className="text-gray-500 italic">Aguardando mais dados para sugerir próximos passos.</li>
          )}
        </ul>
      </div>

      {/* Botão de Ação */}
      <div className="mt-6 pt-4 border-t border-gray-200">
        <button 
          onClick={onRetry}
          className="w-full px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors"
        >
          Solicitar Nova Análise
        </button>
      </div>
    </div>
  );
};

export default function EquationPage() {
  const [userEquation, setUserEquation] = useState('');
  const [userSolution, setUserSolution] = useState('');
  const [showSolution, setShowSolution] = useState(false);
  const { feedback, isLoading, requestAnalysis, error } = useAiFeedback();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!userEquation.trim() || !userSolution.trim()) {
      alert('Por favor, preencha a equação e sua solução');
      return;
    }

    try {
      // Solicitar análise da IA
      await requestAnalysis(
        `equation-${Date.now()}`, // contentId único
        `Equação: ${userEquation}, Solução: ${userSolution}`, // userResponse
        'equation', // mode
        {
          equation: userEquation,
          solution: userSolution,
          timeSpent: Date.now(),
          timestamp: new Date().toISOString()
        }
      );
      setShowSolution(true);
    } catch (error) {
      console.error('Erro ao solicitar análise:', error);
    }
  };

  const handleReset = () => {
    setUserEquation('');
    setUserSolution('');
    setShowSolution(false);
  };

  const handleRetry = () => {
    if (userEquation && userSolution) {
      handleSubmit(new Event('submit') as any);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-4">
            Resolução de Equações
          </h1>
          <p className="text-lg text-gray-600">
            Digite uma equação e sua solução para receber feedback personalizado da IA
          </p>
        </div>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Formulário de entrada */}
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">
              Sua Equação
            </h2>
            
            {error && (
              <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
                Erro: {error}
              </div>
            )}
            
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label htmlFor="equation" className="block text-sm font-medium text-gray-700 mb-1">
                  Equação:
                </label>
                <input
                  id="equation"
                  type="text"
                  value={userEquation}
                  onChange={(e) => setUserEquation(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Ex: 2x + 5 = 15"
                  disabled={isLoading}
                />
              </div>

              <div>
                <label htmlFor="solution" className="block text-sm font-medium text-gray-700 mb-1">
                  Sua Solução:
                </label>
                <input
                  id="solution"
                  type="text"
                  value={userSolution}
                  onChange={(e) => setUserSolution(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Ex: x = 5"
                  disabled={isLoading}
                />
              </div>

              <div className="flex space-x-3">
                <button
                  type="submit"
                  disabled={isLoading}
                  className="flex-1 px-4 py-2 bg-blue-600 text-white font-semibold rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isLoading ? 'Analisando...' : 'Analisar Solução'}
                </button>
                
                <button
                  type="button"
                  onClick={handleReset}
                  disabled={isLoading}
                  className="px-4 py-2 bg-gray-600 text-white font-semibold rounded-md hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-500 disabled:opacity-50"
                >
                  Limpar
                </button>
              </div>
            </form>

            {/* Exemplos */}
            <div className="mt-6 p-4 bg-blue-50 rounded-lg">
              <h3 className="font-medium text-blue-800 mb-2">Exemplos:</h3>
              <div className="text-sm text-blue-700 space-y-1">
                <p>• Equação: 3x - 7 = 14 | Solução: x = 7</p>
                <p>• Equação: 2(x + 3) = 16 | Solução: x = 5</p>
                <p>• Equação: x² - 9 = 0 | Solução: x = ±3</p>
              </div>
            </div>
          </div>

          {/* Painel de Feedback */}
          <AiFeedbackPanel 
            analysisResult={feedback}
            isLoading={isLoading}
            onRetry={handleRetry}
          />
        </div>

        {/* Seção de estatísticas */}
        {showSolution && feedback && (
          <div className="mt-8 bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold text-gray-800 mb-4">
              Resumo da Análise
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="text-center p-4 bg-blue-50 rounded-lg">
                <div className="text-2xl font-bold text-blue-600">
                  {feedback.score}%
                </div>
                <div className="text-sm text-gray-600">Pontuação</div>
              </div>
              <div className="text-center p-4 bg-green-50 rounded-lg">
                <div className="text-2xl font-bold text-green-600">
                  {feedback.strengths.length}
                </div>
                <div className="text-sm text-gray-600">Pontos Fortes</div>
              </div>
              <div className="text-center p-4 bg-yellow-50 rounded-lg">
                <div className="text-2xl font-bold text-yellow-600">
                  {feedback.areasToImprove.length}
                </div>
                <div className="text-sm text-gray-600">Áreas para Melhorar</div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// EXTENSÕES:
// - Adicionar animações de transição ao exibir o feedback.
// - Implementar validação de entrada para equações e soluções.
// - Permitir que o usuário visualize exemplos de equações e soluções antes de enviar.
// - Adicionar suporte a diferentes tipos de equações (ex: quadráticas, lineares
//   e exponenciais).
// - Implementar um sistema de histórico para que o usuário possa revisar análises anteriores.
// - Permitir que o usuário compartilhe suas soluções e feedback em redes sociais.
// - Adicionar suporte a múltiplas tentativas, onde o usuário pode corrigir sua
//   solução com base no feedback recebido.
// - Implementar um sistema de gamificação, onde o usuário ganha pontos por
//   resolver equações corretamente e melhorar sua pontuação ao longo do tempo.
// - Adicionar suporte a diferentes níveis de dificuldade, permitindo que o usuário
//   escolha o nível de complexidade das equações que deseja resolver.
// - Implementar um sistema de dicas, onde o usuário pode solicitar ajuda para resolver a equação.
// - Adicionar suporte a gráficos para visualizar soluções de equações complexas.