// src/components/ai/AiFeedbackPanel.tsx - VERSÃO CORRIGIDA
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

export const AiFeedbackPanel: React.FC<AiFeedbackPanelProps> = ({
  analysisResult,
  isLoading = false,
  onRetry
}) => {
  // Verificação de segurança para evitar erros
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
        <h4 className="font-semibold text-green-400">Pontos Fortes:</h4>
        <ul className="list-disc pl-5 mt-1">
          {/* CORREÇÃO: Verificação se strengths existe e é array */}
          {analysisResult.strengths && Array.isArray(analysisResult.strengths) && analysisResult.strengths.length > 0 ? (
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
        <h4 className="font-semibold text-yellow-400">Áreas para Melhorar:</h4>
        <ul className="list-disc pl-5 mt-1">
          {/* CORREÇÃO: Verificação se areasToImprove existe e é array */}
          {analysisResult.areasToImprove && Array.isArray(analysisResult.areasToImprove) && analysisResult.areasToImprove.length > 0 ? (
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
        <h4 className="font-semibold text-blue-400">Próximos Passos:</h4>
        <ul className="list-disc pl-5 mt-1">
          {/* CORREÇÃO: Verificação se nextSteps existe e é array */}
          {analysisResult.nextSteps && Array.isArray(analysisResult.nextSteps) && analysisResult.nextSteps.length > 0 ? (
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