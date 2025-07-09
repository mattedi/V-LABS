// src/context/ChatContext.tsx
// Contexto do chat - gerencia todas as mensagens da conversa
// Permite adicionar, listar e limpar mensagens de qualquer componente.
// Este arquivo define o contexto do chat, que é usado para gerenciar as mensagens
// de uma conversa em uma aplicação React. Ele permite que qualquer componente
// envolvido pelo `ChatProvider` acesse e manipule as mensagens do chat.


import React, { createContext, useContext, useState, ReactNode } from 'react';

/**
 * Estrutura de uma mensagem do chat
 * Define como cada mensagem é organizada
 */
interface ChatMessage {
  id: string;                        // ID único (para o React identificar)
  text: string;                      // Conteúdo da mensagem
  sender: 'user' | 'assistant';      // Quem enviou (usuário ou IA)
  timestamp: Date;                   // Quando foi enviada
}

/**
 * Define o que o contexto de chat disponibiliza
 * Funcionalidades que qualquer componente pode usar
 */
interface ChatContextType {
  messages: ChatMessage[];                                    // Lista de todas as mensagens
  addMessage: (text: string, sender: 'user' | 'assistant') => void;  // Adicionar nova mensagem
  clearChat: () => void;                                      // Limpar conversa
}

/**
 * Cria o contexto (ainda vazio)
 * Será preenchido pelo Provider
 */
const ChatContext = createContext<ChatContextType | undefined>(undefined);

/**
 * Provider - componente que gerencia o estado das mensagens
 * Deve envolver os componentes que precisam do chat
 */
export function ChatProvider({ children }: { children: ReactNode }) {
  // Estado que guarda todas as mensagens da conversa
  const [messages, setMessages] = useState<ChatMessage[]>([]);

  /**
   * Função para adicionar uma nova mensagem ao chat
   * Usada quando usuário envia ou IA responde
   */
  const addMessage = (text: string, sender: 'user' | 'assistant') => {
    const newMessage: ChatMessage = {
      id: Date.now().toString(),    // ID baseado no timestamp (simples e único)
      text,                         // Texto da mensagem
      sender,                       // Quem enviou
      timestamp: new Date(),        // Hora atual
    };
    
    // Adiciona a nova mensagem no final da lista
    setMessages(prevMessages => [...prevMessages, newMessage]);
  };

  /**
   * Função para limpar todas as mensagens
   * Útil para "Nova Conversa" ou reset
   */
  const clearChat = () => {
    setMessages([]); // Volta para array vazio
  };

  return (
    <ChatContext.Provider
      value={{
        messages,    // Lista atual de mensagens
        addMessage,  // Função para adicionar
        clearChat,   // Função para limpar
      }}
    >
      {children}
      {/* Todos os componentes filhos podem usar o chat */}
    </ChatContext.Provider>
  );
}

/**
 * Hook personalizado para usar o contexto do chat
 * Facilita o uso e adiciona verificação de erro
 */
export function useChatContext() {
  const context = useContext(ChatContext);
  
  // Verifica se está sendo usado dentro do ChatProvider
  if (context === undefined) {
    throw new Error('useChatContext must be used within a ChatProvider');
    // Erro claro se esquecer de envolver com ChatProvider
  }
  
  return context; // Retorna as funções e dados do chat
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