// src/components/ai/AiFeedbackPanel.tsx
// O componente AiFeedbackPanel exibe o resultado da análise 
// de desempenho feita por uma IA sobre uma
//  tarefa realizada por um estudante.
// Um painel com: Pontuação, Feedback geral, Pontos fortes, Áreas para melhorar
//Próximos passos, Botão para nova análise


// src/components/ai/AiFeedbackPanel.tsx
// Componente de Feedback da IA com suporte a complexidade da pergunta

// src/components/ai/AiFeedbackPanel.tsx

import React from 'react';
import { FiCheckCircle, FiAlertCircle, FiArrowRightCircle, FiCopy, FiDownload } from 'react-icons/fi';
// import { motion } from 'framer-motion'; // descomente se quiser animações
import jsPDF from 'jspdf';

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

const Section: React.FC<{
  title: string;
  items: string[];
  emptyMessage: string;
  icon: React.ReactNode;
  className?: string;
}> = ({ title, items, emptyMessage, icon, className = '' }) => (
  <div className="mt-4">
    <h4 className={`font-semibold mb-1 ${className}`}>{title}</h4>
    <ul className="list-none pl-1 space-y-1">
      {items.length > 0 ? (
        items.map((item, index) => (
          <li key={index} className="flex items-start text-gray-600 gap-2">
            {icon}
            <span>{item}</span>
          </li>
        ))
      ) : (
        <li className="italic text-gray-400 pl-6">{emptyMessage}</li>
      )}
    </ul>
  </div>
);

export const AiFeedbackPanel: React.FC<AiFeedbackPanelProps> = ({ analysisResult, isLoading = false, onRetry }) => {
  const handleCopy = () => {
    if (!analysisResult) return;
    const { feedback, strengths, areasToImprove, nextSteps } = analysisResult;
    const text = `
Resumo da IA:
${feedback}

Pontos Fortes:
${strengths.join('\n')}

Aspectos a Melhorar:
${areasToImprove.join('\n')}

Próximos Passos:
${nextSteps.join('\n')}
    `.trim();
    navigator.clipboard.writeText(text);
    alert('Feedback copiado para a área de transferência.');
  };

  const handleExport = () => {
    if (!analysisResult) return;
    const doc = new jsPDF();
    doc.setFontSize(14);
    doc.text("Análise de Complexidade da Pergunta", 10, 10);
    doc.setFontSize(11);
    doc.text(`Complexidade: ${analysisResult.score}%`, 10, 20);
    doc.text(`\nResumo da IA:\n${analysisResult.feedback}`, 10, 30);
    doc.text(`\nPontos Fortes:\n${analysisResult.strengths.join('\n')}`, 10, 50);
    doc.text(`\nAspectos a Melhorar:\n${analysisResult.areasToImprove.join('\n')}`, 10, 70);
    doc.text(`\nPróximos Passos:\n${analysisResult.nextSteps.join('\n')}`, 10, 90);
    doc.save("analise_feedback.pdf");
  };

  if (isLoading) {
    return (
      <div className="bg-white p-6 rounded-lg shadow text-center" aria-busy="true">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 inline-block mb-2" />
        <p className="text-gray-600">Analisando complexidade da pergunta...</p>
      </div>
    );
  }

  if (!analysisResult) {
    return (
      <div className="bg-white p-6 rounded-lg shadow text-center text-gray-500">
        <p>Aguardando análise da IA.</p>
        {onRetry && (
          <button
            onClick={onRetry}
            className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            aria-label="Iniciar nova análise"
          >
            Iniciar Análise
          </button>
        )}
      </div>
    );
  }

  const { score, feedback, strengths, areasToImprove, nextSteps } = analysisResult;

  return (
    // <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}> {/* opcional */}
    <div className="bg-white p-6 rounded-lg shadow-md space-y-6" aria-live="polite">
      <h3 className="text-xl font-bold text-gray-800 mb-2 flex items-center gap-2">
        Análise de Complexidade da Pergunta
        <span
          className="text-sm text-gray-400 cursor-help"
          title="A complexidade é estimada com base na profundidade, abstração e formulação da pergunta."
        >
          ℹ️
        </span>
      </h3>

      <div className="space-y-2">
        <span className="text-gray-700 font-medium">Complexidade Estimada:</span>
        <div className="w-full bg-gray-200 rounded h-4 relative">
          <div
            className="absolute top-0 left-0 h-4 bg-blue-600 rounded"
            style={{ width: `${score}%` }}
          />
        </div>
        <span className="text-2xl font-bold text-blue-600">{score}%</span>
      </div>

      {feedback && (
        <div className="bg-gray-50 p-4 rounded-lg">
          <h4 className="font-semibold text-gray-700 mb-2">Resumo da IA:</h4>
          <p className="text-gray-600">{feedback}</p>
        </div>
      )}

      <Section
        title="Pontos Fortes da Pergunta:"
        items={strengths}
        emptyMessage="Nenhum ponto forte identificado."
        icon={<FiCheckCircle className="text-green-500 mt-1" />}
        className="text-green-600"
      />

      <Section
        title="Aspectos a Melhorar:"
        items={areasToImprove}
        emptyMessage="Nenhuma recomendação específica encontrada."
        icon={<FiAlertCircle className="text-yellow-500 mt-1" />}
        className="text-yellow-600"
      />

      <Section
        title="Próximos Passos Recomendados:"
        items={nextSteps}
        emptyMessage="Sem sugestões adicionais no momento."
        icon={<FiArrowRightCircle className="text-blue-500 mt-1" />}
        className="text-blue-600"
      />

      <div className="pt-4 flex gap-3 flex-wrap border-t border-gray-200 justify-end">
        <button
          onClick={handleCopy}
          className="flex items-center gap-2 px-4 py-2 bg-gray-100 text-gray-700 rounded hover:bg-gray-200"
        >
          <FiCopy /> Copiar Feedback
        </button>
        <button
          onClick={handleExport}
          className="flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700"
        >
          <FiDownload /> Exportar PDF
        </button>
        {onRetry && (
          <button
            onClick={onRetry}
            className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
          >
            Reanalisar Pergunta
          </button>
        )}
      </div>
    </div>
    // </motion.div> {/* opcional */}
  );
};

