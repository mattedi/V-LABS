/**
 * Página inicial da aplicação VL Studio
 * 
 * Esta é a página principal que serve como hub central da aplicação,
 * fornecendo acesso aos diferentes modos de tutoria (equação, voz, imagem)
 * e interface de chat para interação com o usuário.
 * 
 * Funcionalidades principais:
 * - Navegação automática baseada no modo selecionado
 * - Interface de chat integrada
 * - Seleção de tipos de tutoria
 * 
 * @returns {JSX.Element} Componente da página inicial
 */

// Importações do React e roteamento
import React from 'react';
import { useNavigate } from 'react-router-dom';

// Importações dos componentes de chat
import { ChatBar } from '../components/chat';
import MessageList from '../components/chat/MessageList';

// Importações dos componentes de tutoria
import { TutorButtons } from '../components/tutoring';

// Importação do contexto global da aplicação
import { useAppContext } from '../context/AppContext';

/**
 * Componente principal da página inicial
 * 
 * Gerencia a navegação automática entre diferentes modos de tutoria
 * e renderiza a interface principal com chat e opções de tutoria.
 */
export default function Home() {
  // Hook para navegação programática entre páginas
  const navigate = useNavigate();
  
  // Obtém o modo atual selecionado pelo usuário do contexto global
  const { currentMode } = useAppContext();
  
  /**
   * Efeito para navegação automática baseada no modo selecionado
   * 
   * Monitora mudanças no currentMode e redireciona automaticamente
   * para a página correspondente quando um modo específico é selecionado.
   * 
   * Modos disponíveis:
   * - 'equation': Redireciona para /equation
   * - 'voice': Redireciona para /voice  
   * - 'image': Redireciona para /image
   */
  React.useEffect(() => {
    if (currentMode === 'equation') {
      navigate('/equation');
    } else if (currentMode === 'voice') {
      navigate('/voice');
    } else if (currentMode === 'image') {
      navigate('/image');
    }
  }, [currentMode, navigate]); // Dependências: executa quando currentMode ou navigate mudarem

  return (
    <>
      {/* Título principal da aplicação - destaque em azul claro */}
      <h2 className="mt-6 text-center text-4xl font-bold text-[#B0D2FF]">
        Bem vindo VL Studio
      </h2>

      {/* Área de chat - lista de mensagens e barra de entrada */}
      <MessageList />
      <ChatBar />

      {/* Seção de seleção de tutoria */}
      <h3 className="mt-10 text-center text-3xl">
        Escolha <span className="text-[#B0D2FF]">sua tutoria</span>
      </h3>

      {/* Botões para seleção dos diferentes tipos de tutoria */}
      <TutorButtons />
    </>
  );
}