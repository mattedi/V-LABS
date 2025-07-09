// O componente ChatBar, desenvolvido em React com TypeScript,
//  é um campo de entrada de mensagens com suporte a envio de texto e anexos. 
// Ele é um componente de interface gráfica frequentemente
//  usado em aplicações de chat ou assistentes interativos, 
// como no contexto do Vibe Learning Studio.

import React, { useRef, useState } from 'react';
import { FiPlus, FiSend } from 'react-icons/fi';

interface ChatBarProps {
  compact?: boolean;
  placeholder?: string;
  onSend?: (message: string) => Promise<void> | void;
  onFileSelect?: (files: File[]) => void;
  allowedFileTypes?: string[]; // ex: ['image/png', 'application/pdf']
}

const ChatBar: React.FC<ChatBarProps> = ({
  compact = false,
  placeholder = "Ex. Como eu faço para calcular uma fração...",
  onSend,
  onFileSelect,
  allowedFileTypes = ['image/png', 'image/jpeg', 'application/pdf']
}) => {
  const [message, setMessage] = useState('');
  const [isSending, setIsSending] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleSend = async () => {
    if (!message.trim() || !onSend) return;
    try {
      setIsSending(true);
      await onSend(message);
      setMessage('');
    } finally {
      setIsSending(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSend();
    }
  };

  const handleAttachmentClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || []);
    const validFiles = files.filter(file =>
      allowedFileTypes.includes(file.type)
    );

    if (validFiles.length && onFileSelect) {
      onFileSelect(validFiles);
    }

    // Limpa para permitir re-seleção do mesmo arquivo
    e.target.value = '';
  };

  return (
    <div className={`flex items-center gap-2 ${compact ? 'p-2' : 'p-4'}`}>
      <div className="flex-1 flex items-center border border-gray-300 rounded-lg overflow-hidden bg-white dark:bg-gray-800">
        
        {/* Botão "+" */}
        <button
          onClick={handleAttachmentClick}
          className="p-3 text-gray-500 hover:text-gray-700 dark:hover:text-gray-300 transition-colors"
          title="Adicionar anexo"
        >
          <FiPlus className="text-xl" />
        </button>

        <input
          type="file"
          ref={fileInputRef}
          multiple
          onChange={handleFileChange}
          className="hidden"
        />

        {/* Campo de entrada de mensagem */}
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyPress}
          placeholder={placeholder}
          className="flex-1 p-3 border-none outline-none bg-transparent text-gray-800 dark:text-white"
          aria-label="Digite sua mensagem"
        />

        {/* Botão de envio */}
        <button
          onClick={handleSend}
          className={`p-3 transition-colors ${
            isSending ? 'bg-gray-300 cursor-not-allowed' : 'bg-blue-500 hover:bg-blue-600'
          } text-white`}
          title="Enviar mensagem"
          disabled={!message.trim() || isSending}
        >
          {isSending ? (
            <div className="animate-spin h-5 w-5 border-b-2 border-white rounded-full mx-auto" />
          ) : (
            <FiSend className="text-xl" />
          )}
        </button>
      </div>
    </div>
  );
};

export default ChatBar;

//EXTENSÕES:
// - Adicionar suporte a emojis ou formatação de texto (negrito, itálico).
// - Implementar envio de mensagens por voz usando Web Speech API.  
// - Permitir envio de mensagens com botões de ação (ex: "Sim", "Não").
// - Implementar histórico de mensagens com rolagem automática.
// - Adicionar suporte a mensagens de áudio ou vídeo.
// - Implementar detecção automática de links e pré-visualização.
// - Integrar com um backend real para persistência de mensagens.
// - Adicionar suporte a temas personalizados (claro/escuro).
// - Implementar notificações de novas mensagens usando Web Notifications API.
// - Adicionar suporte a atalhos de teclado para envio rápido (ex: Ctrl+Enter).