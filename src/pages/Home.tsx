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
 // src/pages/Home.tsx
/**
 * Página inicial (Chat + Tutorias + Recomendações)
 * - Mantém a lógica existente de feedback/redirects
 * - Adiciona:
 *   (1) Lista de mensagens com rolagem vertical própria
 *   (2) Barra de memória da interação (rolagem horizontal) acima do input
 */

// src/pages/Home.tsx
/**
 * Página inicial (Chat + Tutorias + Recomendações)
 * - Mantém a lógica existente de feedback/redirects
 * - Adiciona:
 *   (1) Barra de memória da interação (rolagem horizontal) logo abaixo do título
 *   (2) Disparo de evento para alimentar a memória ao enviar mensagem
 */
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ChatBar } from '../components/chat';
import MessageList from '../components/chat/MessageList';
import { TutorButtons } from '../components/tutoring';
import { useAppContext } from '../context/AppContext';
import { useProgressContext } from '../context/ProgressContext';
import { useAiFeedback } from '../hooks/useAiFeedback';
import { AiFeedbackPanel } from '../components/ai/AiFeedbackPanel';

export default function Home(): JSX.Element {
  const navigate = useNavigate();
  const { currentMode } = useAppContext();
  const { recommendedContent } = useProgressContext();

  const [lastQuestion, setLastQuestion] = useState('');
  const [lastContentId, setLastContentId] = useState('');
  const { feedback, isLoading, requestAnalysis } = useAiFeedback();

  // Memória simulada de interações
  const [memory, setMemory] = useState<string[]>([
    'Como que é um denominador?',
    'O que são frações?'
  ]);

  const handleSend = async (message: string) => {
    const trimmed = message.trim();
    if (!trimmed) return;
    setMemory(prev => [trimmed, ...prev]); // adiciona na memória
    const contentId = `home-${Date.now()}`;
    setLastQuestion(trimmed);
    setLastContentId(contentId);
    await requestAnalysis(contentId, trimmed, 'text');
  };

  useEffect(() => {
    if (currentMode === 'equation') navigate('/equation');
    else if (currentMode === 'voice') navigate('/voice');
    else if (currentMode === 'image') navigate('/image');
  }, [currentMode, navigate]);

  return (
    <div className="flex flex-col items-center">
      <h2 className="mt-9 text-center text-4xl font-bold text-[#B0D2FF]">
        Bem vindo Vibe Learning Studio
      </h2>

      {/* Memória da interação com scroll */}
      <div className="w-full max-w-4xl mt-4">
        <h4 className="text-sm font-semibold text-gray-300 mb-2">Memória da interação</h4>
        <div className="bg-gray-800 rounded-lg p-2 max-h-28 overflow-y-auto">
          {memory.map((item, idx) => (
            <div
              key={idx}
              className="bg-gray-700 p-2 rounded mb-1 cursor-pointer hover:bg-gray-600"
              onClick={() => handleSend(item)}
            >
              {item}
            </div>
          ))}
        </div>
      </div>

      {/* Lista de mensagens */}
      <div className="w-full max-w-4xl flex-1 overflow-y-auto my-4">
        <MessageList />
      </div>

      {/* Barra de entrada */}
      <div className="w-full max-w-4xl">
        <ChatBar
          onSend={handleSend}
          placeholder="Ex. Como eu faço para calcular uma fração..."
        />
      </div>

      {/* Feedback */}
      {feedback && (
        <div className="mt-6 max-w-4xl mx-auto">
          <AiFeedbackPanel
            analysisResult={feedback}
            isLoading={isLoading}
            onRetry={() => requestAnalysis(lastContentId, lastQuestion, 'text')}
          />
        </div>
      )}

      {/* Botões de tutoria */}
      <h3 className="mt-9 text-center text-3xl">
        <span className="text-[#B0D2FF]">Escolha sua tutoria</span>
      </h3>
      <TutorButtons />

      {/* Recomendações */}
      {recommendedContent.length > 0 && (
        <div className="mt-8 p-4 bg-gray-400 rounded-lg w-full max-w-4xl">
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
      )}
    </div>
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
