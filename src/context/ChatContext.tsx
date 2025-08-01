// src/context/ChatContext.tsx
// Contexto do chat - gerencia todas as mensagens da conversa
// Permite adicionar, listar e limpar mensagens de qualquer componente.
// Este arquivo define o contexto do chat, que é usado para gerenciar as mensagens
// de uma conversa em uma aplicação React. Ele permite que qualquer componente
// envolvido pelo `ChatProvider` acesse e manipule as mensagens do chat.

import React, { createContext, useContext, useState, ReactNode } from 'react';

/**
 * Estrutura de uma mensagem do chat
 */
export interface ChatMessage {
  id: string;
  text: string;
  sender: 'user' | 'assistant';
  timestamp: Date;
}

/**
 * Tipo do contexto do Chat
 */
interface ChatContextType {
  messages: ChatMessage[];
  addMessage: (text: string, sender: 'user' | 'assistant') => void;
  clearChat: () => void;

  // ✅ Novo: histórico de perguntas do usuário
  userHistory: ChatMessage[];
}

/**
 * Criação do contexto
 */
const ChatContext = createContext<ChatContextType | undefined>(undefined);

/**
 * Provider do Chat
 */
export function ChatProvider({ children }: { children: ReactNode }) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);

  const addMessage = (text: string, sender: 'user' | 'assistant') => {
    const newMessage: ChatMessage = {
      id: Date.now().toString(),
      text,
      sender,
      timestamp: new Date(),
    };
    setMessages(prevMessages => [...prevMessages, newMessage]);
  };

  const clearChat = () => {
    setMessages([]);
  };

  // ✅ Histórico: apenas mensagens do usuário
  const userHistory = messages.filter(msg => msg.sender === 'user');

  return (
    <ChatContext.Provider
      value={{
        messages,
        addMessage,
        clearChat,
        userHistory, // <- novo dado disponível no contexto
      }}
    >
      {children}
    </ChatContext.Provider>
  );
}

/**
 * Hook para acessar o contexto
 */
export function useChatContext() {
  const context = useContext(ChatContext);
  if (context === undefined) {
    throw new Error('useChatContext must be used within a ChatProvider');
  }
  return context;
}

// EXTENSÕES:
// - Adicionar suporte a mensagens de erro ou status (ex: "Carregando...").
// - Implementar persistência de chat (salvar no localStorage).
// - Adicionar suporte a formatação de texto (negrito, itálico, etc.).
// - Implementar envio de arquivos (imagens, documentos).
// - Adicionar suporte a emojis ou stickers.
// - Implementar um sistema de notificações para novas mensagens.
// - Adicionar suporte a mensagens de áudio ou vídeo.
// - Implementar um sistema de busca dentro do chat.
// - Adicionar suporte a respostas rápidas ou sugestões de mensagens.
// - Implementar um sistema de reações às mensagens (curtir, reagir, etc.).