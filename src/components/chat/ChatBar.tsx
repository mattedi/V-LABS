import React, { useRef } from 'react';

interface ChatBarProps {
  compact?: boolean;
  placeholder?: string;
  onSend?: (message: string) => void;
}

const ChatBar: React.FC<ChatBarProps> = ({
  compact = false,
  placeholder = "Exe. Como eu faço para calcular uma fração...",
  onSend
}) => {
  const [message, setMessage] = React.useState<string>('');
  
  // Referência para o input de arquivo invisível
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Envio da mensagem
  const handleSend = (): void => {
    if (message.trim() && onSend) {
      onSend(message);
      setMessage('');
    }
  };

  // Detecção da tecla Enter
  const handleKeyPress = (e: React.KeyboardEvent): void => {
    if (e.key === 'Enter') {
      handleSend();
    }
  };

  // Clique no botão "+"
  const handleAttachmentClick = () => {
    fileInputRef.current?.click();
  };

  // Processamento do arquivo
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      console.log("Arquivo selecionado:", file.name);
      // Aqui você pode fazer upload, ou passar o arquivo a um callback
      // Ex: onFileSelect && onFileSelect(file);
    }
  };

  return (
    <div className={`flex items-center gap-2 ${compact ? 'p-2' : 'p-4'}`}>
      <div className="flex-1 flex items-center border border-gray-300 rounded-lg overflow-hidden">
        
        {/* Botão "+" de anexo */}
        <button
          onClick={handleAttachmentClick}
          className="p-3 text-gray-500 hover:text-gray-700 transition-colors"
          title="Adicionar anexo ou função extra"
        >
          <span className="text-xl">+</span>
        </button>

        {/* Input invisível */}
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileChange}
          className="hidden"
        />

        {/* Campo de texto */}
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder={placeholder}
          className="flex-1 p-3 border-none outline-none focus:ring-2 focus:ring-blue-500"
          aria-label="Campo para digitar mensagem"
        />

        {/* Botão de envio */}
        <button
          onClick={handleSend}
          className="p-3 bg-blue-500 text-white hover:bg-blue-600 transition-colors"
          title="Enviar mensagem"
          disabled={!message.trim()}
        >
          <span className="text-lg">→</span>
        </button>
      </div>
    </div>
  );
};

export default ChatBar;
