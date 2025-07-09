// src/components/ai/AiFeedbackPanel.tsx
// O componente AiFeedbackPanel exibe o resultado da análise 
// de desempenho feita por uma IA sobre uma
//  tarefa realizada por um estudante.
// Um painel com: Pontuação, Feedback geral, Pontos fortes, Áreas para melhorar
//Próximos passos, Botão para nova análise


import React from 'react';

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

const Section: React.FC<{ title: string; items: string[]; emptyMessage: string; className?: string }> = ({
  title,
  items,
  emptyMessage,
  className = '',
}) => (
  <div className="mt-3">
    <h4 className={`font-semibold ${className}`}>{title}</h4>
    <ul className="list-disc pl-5 mt-1">
      {items && items.length > 0 ? (
        items.map((item, index) => (
          <li key={index} className="text-gray-600">{item}</li>
        ))
      ) : (
        <li className="text-gray-500 italic">{emptyMessage}</li>
      )}
    </ul>
  </div>
);

export const AiFeedbackPanel: React.FC<AiFeedbackPanelProps> = ({ analysisResult, isLoading = false, onRetry }) => {
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
      <div className="bg-white p-6 rounded-lg shadow-md text-center text-gray-500">
        <p>Nenhuma análise disponível ainda.</p>
        {onRetry && (
          <button onClick={onRetry} className="mt-2 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
            Solicitar Análise
          </button>
        )}
      </div>
    );
  }

  const { score, feedback, strengths, areasToImprove, nextSteps } = analysisResult;

  return (
    <div className="bg-white p-6 rounded-lg shadow-md space-y-6">
      <h3 className="text-xl font-bold text-gray-800 mb-4">Feedback da IA</h3>

      <div className="bg-blue-50 p-4 rounded-lg flex items-center justify-between">
        <span className="text-lg font-semibold text-gray-700">Pontuação:</span>
        <span className="text-2xl font-bold text-blue-600">{score}%</span>
      </div>

      {feedback && (
        <div className="bg-gray-50 p-4 rounded-lg">
          <h4 className="font-semibold text-gray-700 mb-2">Feedback Geral:</h4>
          <p className="text-gray-600">{feedback}</p>
        </div>
      )}

      <Section title="Pontos Fortes:" items={strengths} emptyMessage="Nenhum ponto forte identificado ainda." className="text-green-400" />
      <Section title="Áreas para Melhorar:" items={areasToImprove} emptyMessage="Nenhuma área de melhoria identificada." className="text-yellow-400" />
      <Section title="Próximos Passos:" items={nextSteps} emptyMessage="Aguardando mais dados para sugerir próximos passos." className="text-blue-400" />

      {onRetry && (
        <div className="mt-6 pt-4 border-t border-gray-200">
          <button onClick={onRetry} className="w-full px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors">
            Solicitar Nova Análise
          </button>
        </div>
      )}
    </div>
  );
};
