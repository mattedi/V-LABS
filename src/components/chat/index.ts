

// src/components/chat/index.ts
// Arquivo de "Barrel Export" - Ponto de entrada centralizado para componentes de chat

/**
 * ================================================
 * CONCEITO: BARREL EXPORT (Exportação em Barril)
 * ================================================
 * 
 * Este arquivo serve como um "barril" que coleta todos os componentes
 * da pasta 'chat' e os re-exporta de forma organizada.
 * 
 * BENEFÍCIOS:
 * 1. Simplifica imports externos
 * 2. Cria API pública limpa
 * 3. Facilita refatoração interna
 * 4. Melhora organização do projeto
 * 
 * ANTES (sem index.ts):
 * import ChatBar from '../components/chat/ChatBar';
 * import MessageList from '../components/chat/MessageList';
 * 
 * DEPOIS (com index.ts):
 * import { ChatBar, MessageList } from '../components/chat';
 */

// ================================================
// IMPORTAÇÕES DOS COMPONENTES LOCAIS
// ================================================

/**
 * Importa o componente ChatBar do arquivo local
 * 
 * - './ChatBar' = caminho relativo para ChatBar.tsx na mesma pasta
 * - import padrão (default import) = importa a exportação padrão
 * - ChatBar deve ter 'export default ChatBar' no final do arquivo
 */
import ChatBar from './ChatBar';

// ================================================
// FUTURAS IMPORTAÇÕES (quando criar mais componentes)
// ================================================

// Exemplos de outros componentes de chat que podem ser adicionados:
// import MessageList from './MessageList';     // Lista de mensagens
// import ChatInput from './ChatInput';         // Input específico
// import ChatHeader from './ChatHeader';       // Cabeçalho do chat
// import EmojiPicker from './EmojiPicker';     // Seletor de emojis

// ================================================
// RE-EXPORTAÇÕES (EXPORTS)
// ================================================

/**
 * Re-exporta ChatBar como "named export"
 * 
 * TRANSFORMAÇÃO:
 * - ENTRADA: default export (import ChatBar from './ChatBar')
 * - SAÍDA: named export (export { ChatBar })
 * 
 * RESULTADO: Permite fazer import { ChatBar } from './components/chat'
 */
export { ChatBar };

// ================================================
// FUTURAS RE-EXPORTAÇÕES
// ================================================

// Quando criar mais componentes, adicione aqui:
// export { MessageList };    // Re-exporta MessageList
// export { ChatInput };      // Re-exporta ChatInput
// export { ChatHeader };     // Re-exporta ChatHeader
// export { EmojiPicker };    // Re-exporta EmojiPicker

// ================================================
// EXPORTAÇÃO DE TIPOS (opcional)
// ================================================

/**
 * Se o ChatBar exportar tipos/interfaces, podemos re-exportá-los também
 * 
 * Exemplo:
 * export type { ChatBarProps } from './ChatBar';
 * 
 * Isso permite: import { ChatBar, type ChatBarProps } from './components/chat';
 */

// ================================================
// EXEMPLO DE USO DESTE ARQUIVO
// ================================================

/**
 * COMO USAR EM OUTROS ARQUIVOS:
 * 
 * // Em VoicePage.tsx ou qualquer outro arquivo:
 * import { ChatBar } from '../components/chat';
 * 
 * // Em vez de:
 * import ChatBar from '../components/chat/ChatBar';
 * 
 * VANTAGENS:
 * 1. ✅ Import mais limpo e conciso
 * 2. ✅ Se movermos ChatBar.tsx, só precisamos atualizar este arquivo
 * 3. ✅ Melhor autocomplete no VS Code
 * 4. ✅ Estrutura mais profissional
 * 5. ✅ Facilita trabalho em equipe
 */