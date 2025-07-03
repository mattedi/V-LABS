// src/components/chat/ChatBar.tsx
// Componente de barra de chat para interação do usuário

// Importações necessárias
import React from 'react'; // Biblioteca principal do React

/**
 * Interface que define as propriedades (props) do componente ChatBar
 * 
 * @interface ChatBarProps
 * @property {boolean} compact - Se true, aplica padding menor (modo compacto)
 * @property {string} placeholder - Texto de exemplo no input
 * @property {function} onSend - Função callback executada quando usuário envia mensagem
 */
interface ChatBarProps {
  compact?: boolean; // Opcional: modo compacto da barra
  placeholder?: string; // Opcional: texto placeholder do input
  onSend?: (message: string) => void; // Opcional: função para processar mensagem enviada
}

/**
 * Componente ChatBar - Barra de entrada de chat
 * 
 * Este componente renderiza uma interface de chat com:
 * - Campo de input para digitar mensagens
 * - Botão de envio
 * - Botão adicional (+) para anexos/funções extras
 * 
 * @param {ChatBarProps} props - Propriedades do componente
 * @returns {JSX.Element} Elemento JSX da barra de chat
 */
const ChatBar: React.FC<ChatBarProps> = ({ 
  compact = false, // Valor padrão: modo normal (não compacto)
  placeholder = "Como eu faço para calcular uma fração...", // Texto padrão
  onSend // Função opcional para envio de mensagem
}) => {
  // Estado local para controlar o texto digitado no input
  const [message, setMessage] = React.useState<string>('');

  /**
   * Função para processar o envio da mensagem
   * 
   * Verifica se há texto digitado e se a função onSend foi fornecida
   * Se sim, executa o callback e limpa o input
   */
  const handleSend = (): void => {
    // Verifica se há mensagem (removendo espaços) e se callback existe
    if (message.trim() && onSend) {
      onSend(message); // Executa função de callback com a mensagem
      setMessage(''); // Limpa o input após enviar
    }
  };

  /**
   * Função para detectar tecla Enter no input
   * 
   * @param {React.KeyboardEvent} e - Evento de teclado
   */
  const handleKeyPress = (e: React.KeyboardEvent): void => {
    // Se a tecla pressionada for Enter, envia a mensagem
    if (e.key === 'Enter') {
      handleSend();
    }
  };

  // Renderização do componente
  return (
    <div className={`flex items-center gap-2 ${compact ? 'p-2' : 'p-4'}`}>
      {/* Container principal da barra de chat */}
      
      {/* Container do input com botões */}
      <div className="flex-1 flex items-center border border-gray-300 rounded-lg overflow-hidden">
        
        {/* Botão de adicionar/anexar (lado esquerdo) */}
        <button 
          className="p-3 text-gray-500 hover:text-gray-700 transition-colors"
          title="Adicionar anexo ou função extra"
        >
          <span className="text-xl">+</span>
        </button>
        
        {/* Campo de input principal */}
        <input
          type="text"
          value={message} // Valor controlado pelo estado
          onChange={(e) => setMessage(e.target.value)} // Atualiza estado quando usuário digita
          onKeyPress={handleKeyPress} // Detecta Enter para enviar
          placeholder={placeholder} // Texto de exemplo
          className="flex-1 p-3 border-none outline-none focus:ring-2 focus:ring-blue-500"
          aria-label="Campo para digitar mensagem" // Acessibilidade
        />
        
        {/* Botão de envio (lado direito) */}
        <button 
          onClick={handleSend} // Executa envio quando clicado
          className="p-3 bg-blue-500 text-white hover:bg-blue-600 transition-colors"
          title="Enviar mensagem"
          disabled={!message.trim()} // Desabilita se não há texto
        >
          <span className="text-lg">→</span>
        </button>
        
      </div>
    </div>
  );
};

// ✅ EXPORT DEFAULT - Permite importar o componente como padrão
// Exemplo de uso: import ChatBar from './ChatBar';
export default ChatBar;