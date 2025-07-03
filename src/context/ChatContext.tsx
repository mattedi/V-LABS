// src/context/ChatContext.tsx
// Contexto do chat - gerencia todas as mensagens da conversa
// Permite adicionar, listar e limpar mensagens de qualquer componente

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

// =====================================
// COMO USAR ESTE CONTEXTO:
// =====================================

/**
 * 1. No App.tsx ou página principal - Envolver com Provider:
 * 
 * function App() {
 *   return (
 *     <AppProvider>
 *       <ChatProvider>
 *         <MainLayout />
 *       </ChatProvider>
 *     </AppProvider>
 *   );
 * }
 */

/**
 * 2. No ChatBar - Para enviar mensagens:
 * 
 * function ChatBar() {
 *   const { addMessage } = useChatContext();
 *   const [inputText, setInputText] = useState('');
 * 
 *   const handleSend = () => {
 *     if (inputText.trim()) {
 *       addMessage(inputText, 'user');  // Adiciona mensagem do usuário
 *       setInputText('');               // Limpa input
 *       
 *       // Simular resposta da IA (exemplo)
 *       setTimeout(() => {
 *         addMessage('Resposta da IA aqui', 'assistant');
 *       }, 1000);
 *     }
 *   };
 * 
 *   return (
 *     <div>
 *       <input 
 *         value={inputText}
 *         onChange={(e) => setInputText(e.target.value)}
 *       />
 *       <button onClick={handleSend}>Enviar</button>
 *     </div>
 *   );
 * }
 */

/**
 * 3. No MessageList - Para exibir mensagens:
 * 
 * function MessageList() {
 *   const { messages } = useChatContext();
 * 
 *   if (messages.length === 0) {
 *     return <p>Nenhuma mensagem ainda...</p>;
 *   }
 * 
 *   return (
 *     <div>
 *       {messages.map(message => (
 *         <div key={message.id} className={message.sender}>
 *           <p>{message.text}</p>
 *           <small>{message.timestamp.toLocaleTimeString()}</small>
 *         </div>
 *       ))}
 *     </div>
 *   );
 * }
 */

/**
 * 4. Em qualquer componente - Para limpar chat:
 * 
 * function ChatHeader() {
 *   const { clearChat, messages } = useChatContext();
 * 
 *   return (
 *     <div>
 *       <h2>Chat ({messages.length} mensagens)</h2>
 *       <button onClick={clearChat}>
 *         Nova Conversa
 *       </button>
 *     </div>
 *   );
 * }
 */

/**
 * 5. Exemplo completo de integração:
 * 
 * function ChatPage() {
 *   const { messages, addMessage } = useChatContext();
 * 
 *   // Mensagem automática de boas-vindas
 *   useEffect(() => {
 *     if (messages.length === 0) {
 *       addMessage('Olá! Como posso ajudar?', 'assistant');
 *     }
 *   }, []);
 * 
 *   return (
 *     <div>
 *       <MessageList />
 *       <ChatBar />
 *     </div>
 *   );
 * }
 */

// =====================================
// VANTAGENS DESTE CONTEXTO:
// =====================================

/**
 * ✅ CENTRALIZADO: Todas as mensagens em um lugar só
 * ✅ REATIVO: Quando adiciona mensagem, MessageList atualiza automaticamente
 * ✅ SIMPLES: Apenas 3 funções (messages, addMessage, clearChat)
 * ✅ FLEXÍVEL: Qualquer componente pode enviar/receber mensagens
 * ✅ CONSISTENTE: Estado único, sem duplicação
 * 
 * SEM CONTEXTO (problemático):
 * - Passar mensagens por props em vários níveis
 * - Estado duplicado entre ChatBar e MessageList
 * - Sincronização manual entre componentes
 * 
 * COM CONTEXTO (melhor):
 * - Acesso direto em qualquer componente
 * - Sincronização automática
 * - Código mais limpo
 */

// =====================================
// POSSÍVEIS MELHORIAS FUTURAS:
// =====================================

/**
 * 💡 FUNCIONALIDADES QUE PODEM SER ADICIONADAS:
 * 
 * - editMessage(id, newText): Editar mensagens
 * - deleteMessage(id): Apagar mensagens específicas
 * - markAsRead(id): Marcar como lida
 * - saveToLocalStorage(): Persistir conversa
 * - loadFromLocalStorage(): Carregar conversa salva
 * - addTypingIndicator(): Mostrar "digitando..."
 * - addMessageStatus(): Status de envio (enviando/enviado/erro)
 */