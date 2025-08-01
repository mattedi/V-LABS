/**
 * Página inicial da aplicação VL Studio
 * Esta é a página principal que serve como hub central da aplicação,
 * fornecendo acesso aos diferentes modos de tutoria (equação, voz, imagem)
 * e interface de chat para interação com o usuário.
 * Funcionalidades principais:
 * - Navegação automática baseada no modo selecionado
 * - Interface de chat integrada
 * - Seleção de tipos de tutoria
 * 
 * @returns {JSX.Element} Componente da página inicial
 */

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

// Componentes de chat
import { ChatBar } from '../components/chat';
import MessageList from '../components/chat/MessageList';

// Componentes de tutoria
import { TutorButtons } from '../components/tutoring';

// Contextos
import { useAppContext } from '../context/AppContext';
import { useProgressContext } from '../context/ProgressContext';
import { useAiFeedback } from '../hooks/useAiFeedback';
import { AiFeedbackPanel } from '../components/ai/AiFeedbackPanel';

export default function Home(): JSX.Element {
  const navigate = useNavigate();
  const { currentMode } = useAppContext();
  const { recommendedContent } = useProgressContext();

  // Estado e lógica de envio de mensagens
  const [lastQuestion, setLastQuestion] = useState('');
  const [lastContentId, setLastContentId] = useState('');
  const { feedback, isLoading, requestAnalysis } = useAiFeedback();

  const handleSend = async (message: string) => {
    const trimmed = message.trim();
    if (!trimmed) return;

    const contentId = `home-${Date.now()}`;
    setLastQuestion(trimmed);
    setLastContentId(contentId);
    await requestAnalysis(contentId, trimmed, 'text');
  };

  // Redirecionamento automático conforme o modo selecionado
  useEffect(() => {
    if (currentMode === 'equation') navigate('/equation');
    else if (currentMode === 'voice') navigate('/voice');
    else if (currentMode === 'image') navigate('/image');
  }, [currentMode, navigate]);

  // Renderização das recomendações
  const renderRecommendations = () => {
    if (recommendedContent.length === 0) return null;

    return (
      <div className="mt-8 p-4 bg-gray-400 rounded-lg">
        <h3 className="text-xl font-semibold text-[#B0D2FF]">Recomendado para você</h3>
        <ul className="mt-2">
          {recommendedContent.map(item => (
            <li
              key={item.id}
              className="py-2 cursor-pointer hover:bg-gray-700 px-3 rounded-md"
              onClick={() => navigate(`/${item.mode}`)}
            >
              {item.title}
              <span className="text-xs bg-blue-500 px-2 py-1 rounded-full ml-2">
                {item.difficulty}
              </span>
            </li>
          ))}
        </ul>
      </div>
    );
  };

  return (
    <>
      {/* Título principal */}
      <h2 className="mt-9 text-center text-4xl font-bold text-[#B0D2FF]">
        Bem vindo Vibe Learning Studio
      </h2>

      {/* Lista de mensagens simuladas */}
      <MessageList />

      {/* Barra de entrada com envio funcional */}
      <ChatBar
        onSend={handleSend}
        placeholder="Ex. Como eu faço para calcular uma fração..."
      />

      {/* Feedback gerado (opcional) */}
      {feedback && (
        <div className="mt-6 max-w-4xl mx-auto">
          <AiFeedbackPanel
            analysisResult={feedback}
            isLoading={isLoading}
            onRetry={() => requestAnalysis(lastContentId, lastQuestion, 'text')}
          />
        </div>
      )}

      {/* Botões de seleção de tutoria */}
      <h3 className="mt-9 text-center text-3xl">
        <span className="text-[#B0D2FF]">Escolha sua tutoria</span>
      </h3>
      <TutorButtons />

      {/* Recomendações personalizadas */}
      {renderRecommendations()}
    </>
  );
}

// EXTENSÕES:
// - Adicionar animações de transição ao navegar entre modos de tutoria.
// - Implementar um sistema de notificações para alertar o usuário sobre novas mensagens no chat.
// - Permitir que o usuário personalize a interface do chat (ex: temas, fontes).
// - Implementar um sistema de badges ou conquistas baseado no uso dos modos de tutoria.
// - Adicionar suporte a múltiplos chats simultâneos com diferentes usuários.
// - Implementar um sistema de feedback para o usuário avaliar a eficácia dos modos de tutoria.
// - Adicionar um histórico de chat que permita ao usuário revisar conversas anteriores.
// - Implementar um sistema de recomendações personalizadas baseado no histórico de chat e progresso do usuário.
// - Adicionar suporte a emojis e reações nas mensagens do chat.
// - Implementar um sistema de pesquisa para encontrar mensagens específicas no chat.
// - Adicionar suporte a anexos (imagens, arquivos) nas mensagens do chat.
// - Implementar um sistema de integração com redes sociais para compartilhar conquistas ou progresso.
// - Adicionar um modo escuro/ claro para a interface do chat.
// - Implementar um sistema de ajuda ou FAQ integrado ao chat para responder perguntas comuns.
//
