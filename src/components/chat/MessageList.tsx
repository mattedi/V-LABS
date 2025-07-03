// src/components/chat/MessageList.tsx
// Componente para exibir lista de mensagens do chat - Versão Compatível

// ================================================
// IMPORTAÇÕES
// ================================================
import React, { useEffect, useRef } from 'react'; // React + hooks para efeitos e referências
import { useChatContext } from '../../context/ChatContext'; // Hook customizado do contexto de chat

// ================================================
// INTERFACES E TIPOS
// ================================================

/**
 * Props opcionais do componente MessageList
 * Todas as props são opcionais para manter compatibilidade
 * 
 * @interface MessageListProps
 * @property {boolean} autoScroll - Se deve rolar automaticamente para nova mensagem
 * @property {boolean} showTimestamp - Se deve mostrar timestamp nas mensagens
 * @property {boolean} showAvatar - Se deve mostrar avatar do remetente
 * @property {string} emptyMessage - Mensagem personalizada para estado vazio
 */
interface MessageListProps {
  autoScroll?: boolean; // Padrão: true
  showTimestamp?: boolean; // Padrão: true
  showAvatar?: boolean; // Padrão: false
  emptyMessage?: string; // Mensagem customizada para estado vazio
}

/**
 * ⚠️ IMPORTANTE: Interface Message compatível com seu contexto atual
 * Usando apenas as propriedades que existem na sua implementação
 * Removido 'system' e 'status' que causavam erros
 */
interface CompatibleMessage {
  id: string; // ID único da mensagem
  text: string; // Conteúdo da mensagem
  sender: 'user' | 'assistant'; // ✅ Apenas os tipos que você usa
  timestamp: Date; // Quando foi enviada
  // ❌ Removido: status (não existe na sua interface)
  // ❌ Removido: 'system' do sender (não usado)
}

// ================================================
// COMPONENTES AUXILIARES
// ================================================

/**
 * Componente para exibir avatar do remetente
 * Simplificado para trabalhar apenas com 'user' e 'assistant'
 * 
 * @param {Object} props - Props do avatar
 * @param {'user' | 'assistant'} props.sender - Tipo do remetente
 * @returns {JSX.Element} Avatar renderizado
 */
const MessageAvatar: React.FC<{ sender: CompatibleMessage['sender'] }> = ({ sender }) => {
  /**
   * Função para obter ícone baseado no tipo de remetente
   * Apenas para user e assistant
   */
  const getAvatarIcon = (): string => {
    switch (sender) {
      case 'user':
        return '👤'; // Ícone de usuário
      case 'assistant':
        return '🤖'; // Ícone de bot/assistente
      default:
        return '❓'; // Fallback (não deve acontecer)
    }
  };

  /**
   * Função para obter classes CSS baseadas no remetente
   * Cores diferentes para user e assistant
   */
  const getAvatarClasses = (): string => {
    const baseClasses = 'w-8 h-8 rounded-full flex items-center justify-center text-sm';
    
    switch (sender) {
      case 'user':
        return `${baseClasses} bg-blue-500 text-white`;
      case 'assistant':
        return `${baseClasses} bg-gray-600 text-white`;
      default:
        return `${baseClasses} bg-gray-400 text-white`;
    }
  };

  return (
    <div className={getAvatarClasses()}>
      {getAvatarIcon()}
    </div>
  );
};

/**
 * Componente para formatar e exibir timestamp
 * 
 * @param {Object} props - Props do timestamp
 * @param {Date} props.timestamp - Data/hora da mensagem
 * @param {boolean} props.relative - Se deve mostrar tempo relativo
 * @returns {JSX.Element} Timestamp formatado
 */
const MessageTimestamp: React.FC<{ timestamp: Date; relative?: boolean }> = ({ 
  timestamp, 
  relative = false 
}) => {
  /**
   * Função para calcular tempo relativo (ex: "há 5 minutos")
   * Calcula diferença entre agora e o timestamp da mensagem
   */
  const getRelativeTime = (date: Date): string => {
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMinutes = Math.floor(diffMs / (1000 * 60));
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

    // Retorna formato mais apropriado baseado na diferença
    if (diffMinutes < 1) return 'agora';
    if (diffMinutes < 60) return `há ${diffMinutes} min`;
    if (diffHours < 24) return `há ${diffHours} h`;
    if (diffDays < 7) return `há ${diffDays} dias`;
    
    return date.toLocaleDateString(); // Para datas antigas, mostra data completa
  };

  return (
    <div 
      className="text-xs text-gray-400 mt-1"
      title={timestamp.toLocaleString()} // Tooltip com data/hora completa no hover
    >
      {relative ? getRelativeTime(timestamp) : timestamp.toLocaleTimeString()}
    </div>
  );
};

// ================================================
// COMPONENTE PRINCIPAL
// ================================================

/**
 * Componente MessageList Compatível
 * 
 * ✅ COMPATÍVEL com sua interface Message atual
 * ✅ Funciona apenas com 'user' e 'assistant'
 * ✅ Não usa propriedades inexistentes como 'status'
 * 
 * Funcionalidades:
 * - Scroll automático para novas mensagens
 * - Avatares opcionais para remetentes
 * - Timestamps com formato relativo
 * - Estado vazio customizável
 * - Layout responsivo e acessível
 * 
 * @param {MessageListProps} props - Propriedades do componente
 * @returns {JSX.Element} Lista de mensagens melhorada
 */
const MessageList: React.FC<MessageListProps> = ({
  autoScroll = true, // Por padrão, faz scroll automático
  showTimestamp = true, // Por padrão, mostra timestamps
  showAvatar = false, // Por padrão, não mostra avatares (para manter visual original)
  emptyMessage = 'Faça uma pergunta para começar a conversa' // Mensagem padrão
}) => {
  
  // ================================================
  // HOOKS E ESTADO
  // ================================================
  
  // Acessa mensagens do contexto global do chat
  const { messages } = useChatContext();
  
  // Referência para o container das mensagens (para scroll automático)
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  // ================================================
  // EFEITOS COLATERAIS
  // ================================================
  
  /**
   * Efeito para scroll automático quando novas mensagens chegam
   * 
   * Executa sempre que:
   * - Array de mensagens muda (nova mensagem)
   * - autoScroll está habilitado
   */
  useEffect(() => {
    if (autoScroll && messagesEndRef.current) {
      // Rola suavemente para o final das mensagens
      messagesEndRef.current.scrollIntoView({ 
        behavior: 'smooth', // Animação suave
        block: 'end' // Alinha com o final
      });
    }
  }, [messages, autoScroll]); // Dependências: re-executa quando mudarem

  // ================================================
  // FUNÇÕES AUXILIARES
  // ================================================

  /**
   * Função para obter classes CSS da mensagem baseada no remetente
   * ✅ Compatível apenas com 'user' e 'assistant'
   * 
   * @param {CompatibleMessage['sender']} sender - Tipo do remetente
   * @returns {string} Classes CSS concatenadas
   */
  const getMessageClasses = (sender: CompatibleMessage['sender']): string => {
    const baseClasses = 'p-4 rounded-lg max-w-[80%] shadow-sm';
    
    switch (sender) {
      case 'user':
        // Mensagem do usuário: azul, alinhada à direita, canto inferior direito menos arredondado
        return `${baseClasses} bg-primary text-white ml-auto rounded-br-sm`;
      case 'assistant':
        // Mensagem do assistente: cinza claro, alinhada à esquerda, canto inferior esquerdo menos arredondado
        return `${baseClasses} bg-gray-100 text-gray-800 mr-auto rounded-bl-sm border`;
      default:
        // Fallback (não deve acontecer com interface compatível)
        return `${baseClasses} bg-gray-50 text-gray-600 mx-auto`;
    }
  };

  /**
   * Função para verificar se deve mostrar avatar
   * (não mostra avatar para mensagens consecutivas do mesmo remetente)
   * 
   * @param {number} index - Índice da mensagem atual
   * @returns {boolean} Se deve mostrar avatar
   */
  const shouldShowAvatar = (index: number): boolean => {
    if (!showAvatar) return false; // Se avatares estão desabilitados
    if (index === 0) return true; // Primeira mensagem sempre mostra
    
    // Mostra avatar se remetente for diferente da mensagem anterior
    return messages[index].sender !== messages[index - 1].sender;
  };

  // ================================================
  // RENDERIZAÇÃO CONDICIONAL - ESTADO VAZIO
  // ================================================

  /**
   * Se não há mensagens, mostra estado vazio melhorado
   * Mantém compatibilidade com layout original
   */
  if (messages.length === 0) {
    return (
      <div className="flex flex-col justify-center items-center h-64 text-gray-400 space-y-4">
        {/* Container com layout vertical e espaçamento entre elementos */}
        
        {/* Ícone decorativo para estado vazio */}
        <div className="text-6xl opacity-50">
          💬
        </div>
        
        {/* Mensagem de estado vazio */}
        <div className="text-center">
          <p className="text-lg font-medium">{emptyMessage}</p>
          <p className="text-sm mt-2">Digite uma mensagem abaixo para começar</p>
        </div>
      </div>
    );
  }

  // ================================================
  // RENDERIZAÇÃO PRINCIPAL
  // ================================================

  return (
    <div 
      className="max-w-5xl mx-auto my-6 space-y-4 px-4"
      role="log" // Papel ARIA para leitores de tela (acessibilidade)
      aria-label="Lista de mensagens do chat"
    >
      {/* Container principal com acessibilidade */}
      
      {/* ============================================== */}
      {/* LISTA DE MENSAGENS */}
      {/* ============================================== */}
      
      {messages.map((message, index) => (
        <div
          key={message.id} // Key única obrigatória para listas no React
          className={`flex items-end space-x-2 ${
            message.sender === 'user' ? 'justify-end' : 'justify-start'
          }`}
        >
          {/* Container de cada mensagem com alinhamento flexível */}
          
          {/* Avatar à esquerda (apenas para assistant) */}
          {shouldShowAvatar(index) && message.sender === 'assistant' && (
            <MessageAvatar sender={message.sender} />
          )}
          
          {/* Container da mensagem */}
          <div className={getMessageClasses(message.sender)}>
            
            {/* ✅ REMOVIDO: Cabeçalho para mensagens do sistema (não usado) */}
            
            {/* Conteúdo da mensagem */}
            <div className="break-words">
              {/* break-words = quebra palavras longas que não cabem */}
              {message.text}
            </div>
            
            {/* Timestamp (se habilitado) */}
            {showTimestamp && (
              <MessageTimestamp 
                timestamp={message.timestamp} 
                relative={true} // Usa formato relativo ("há 5 min")
              />
            )}
            
            {/* ✅ REMOVIDO: Indicador de status (propriedade não existe) */}
            
          </div>
          
          {/* Avatar à direita (apenas para user) */}
          {shouldShowAvatar(index) && message.sender === 'user' && (
            <MessageAvatar sender={message.sender} />
          )}
          
        </div>
      ))}
      
      {/* ============================================== */}
      {/* ELEMENTO PARA SCROLL AUTOMÁTICO */}
      {/* ============================================== */}
      
      {/* Div invisível no final para scroll automático */}
      <div ref={messagesEndRef} />
      
    </div>
  );
};

// ================================================
// EXPORTAÇÃO
// ================================================

// Exporta o componente como padrão
export default MessageList;

// ================================================
// EXEMPLO DE USO COMPATÍVEL
// ================================================

/**
 * 🚀 EXEMPLOS DE USO (compatível com seu código atual):
 * 
 * // Uso exatamente igual ao original:
 * <MessageList />
 * 
 * // Uso com melhorias opcionais:
 * <MessageList 
 *   autoScroll={true}      // Rola automaticamente
 *   showTimestamp={true}   // Mostra horários
 *   showAvatar={true}      // Mostra avatares
 * />
 * 
 * // Em uma página de chat:
 * function ChatPage() {
 *   return (
 *     <div className="flex flex-col h-screen">
 *       <MessageList showAvatar={true} />
 *       <ChatBar />
 *     </div>
 *   );
 * }
 * 
 * ✅ COMPATIBILIDADE GARANTIDA:
 * - Funciona com sua interface Message atual
 * - Não quebra código existente  
 * - Adiciona funcionalidades opcionais
 * - Mantém visual original se não configurar props
 */