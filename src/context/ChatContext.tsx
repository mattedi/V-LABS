// src/context/ChatContext.tsx
// Contexto do chat - gerencia todas as mensagens da conversa
// Permite adicionar, listar e limpar mensagens de qualquer componente.
// Este arquivo define o contexto do chat, que é usado para gerenciar as mensagens
// de uma conversa em uma aplicação React. Ele permite que qualquer componente
// envolvido pelo `ChatProvider` acesse e manipule as mensagens do chat.


import React, {
  createContext,
  useContext,
  useState,
  useEffect,
  ReactNode,
} from 'react';
import { useAuth } from './AuthContext';

// Interface de uma mensagem
export interface ChatMessage {
  id: string;
  text: string;
  sender: 'user' | 'assistant';
  timestamp: Date;
}

// Tipo do contexto
interface ChatContextType {
  messages: ChatMessage[];
  addMessage: (text: string, sender: 'user' | 'assistant') => void;
  clearChat: () => void;
  userHistory: ChatMessage[];
}

// Criação do contexto
const ChatContext = createContext<ChatContextType | undefined>(undefined);

// Função para buscar mensagens do backend com user_id
async function fetchInteracoes(userId: string): Promise<ChatMessage[]> {
  try {
    const response = await fetch(`/api/interacoes?user_id=${userId}`);
    if (!response.ok) throw new Error('Erro na resposta da API');

    const data = await response.json();

    return data.map((msg: any) => ({
      id: msg.id ?? Date.now().toString(),
      text: msg.text ?? "[sem conteúdo]",
      sender: msg.sender === 'user' || msg.sender === 'assistant' ? msg.sender : 'assistant',
      timestamp: new Date(msg.timestamp ?? new Date().toISOString()),
    }));
  } catch (error) {
    console.error('💥 Erro ao buscar histórico:', error);
    return [];
  }
}

// Provider do contexto
export function ChatProvider({ children }: { children: ReactNode }) {
  const { user } = useAuth();
  const [messages, setMessages] = useState<ChatMessage[]>([]);

  const addMessage = (text: string, sender: 'user' | 'assistant') => {
    const newMessage: ChatMessage = {
      id: Date.now().toString(),
      text,
      sender,
      timestamp: new Date(),
    };
    setMessages(prev => [...prev, newMessage]);
  };

  const clearChat = () => {
    setMessages([]);
  };

  const userHistory = messages.filter(msg => msg.sender === 'user');

  useEffect(() => {
    const carregar = async () => {
      if (!user?.id) {
        console.warn("⚠️ user.id não disponível.");
        return;
      }

      try {
        console.log("🔄 Carregando mensagens para user.id =", user.id);
        const msgs = await fetchInteracoes(user.id);

        // Filtrar mensagens com timestamp válido
        const msgsFiltradas = msgs.filter(msg => msg.timestamp instanceof Date && !isNaN(msg.timestamp.getTime()));
        console.log("📥 Mensagens carregadas:", msgsFiltradas);

        setMessages(msgsFiltradas);
      } catch (e) {
        console.error("💥 Falha ao carregar mensagens:", e);
      }
    };

    carregar();
  }, [user?.id]);

  return (
    <ChatContext.Provider
      value={{
        messages,
        addMessage,
        clearChat,
        userHistory,
      }}
    >
      {children}
    </ChatContext.Provider>
  );
}

// Hook de acesso ao contexto
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