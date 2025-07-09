// src/components/tutoring/TutorButtons.tsx
// Define um componente funcional React que exibe um painel de botões interativos para acessar 
// diferentes modos de tutoria no sistema Vibe Learning Studio: 
// Texto, Voz, Equação e Imagem.
// Cada botão é estilizado com classes Tailwind CSS e ícones do react-icons,
// e ao clicar em um botão, o usuário é redirecionado para a rota correspondente 
// usando o hook useNavigate do react-router-dom.
// Este componente é projetado para ser usado em um layout de tutorias,
// permitindo que os usuários escolham rapidamente o tipo de interação desejada.

import React from 'react';
import { FiEdit, FiMic, FiDivide, FiPieChart } from "react-icons/fi";   
import { useNavigate } from 'react-router-dom';
import { useAppContext } from '../../context/AppContext';

const TutorButtons: React.FC = () => {
  const navigate = useNavigate();
  const { currentMode } = useAppContext();

  const handleNavigation = (path: string) => {
    navigate(path);
  };

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      <button 
        onClick={() => handleNavigation('/text')}
        className="flex flex-col items-center p-4 bg-blue-100 rounded-lg hover:bg-blue-200 transition-colors text-black dark:text-black"
      >
        <FiEdit className="text-2xl mb-2 text-blue-600 dark:text-blue-600" />
        <span className="text-sm font-medium">Texto</span>
      </button>
      
      <button 
        onClick={() => handleNavigation('/voice')}
        className="flex flex-col items-center p-4 bg-green-100 rounded-lg hover:bg-green-200 transition-colors text-black dark:text-black"
      >
        <FiMic className="text-2xl mb-2 text-green-600 dark:text-green-600" />
        <span className="text-sm font-medium">Voz</span>
      </button>
      
      <button 
        onClick={() => handleNavigation('/equation')}
        className="flex flex-col items-center p-4 bg-purple-100 rounded-lg hover:bg-purple-200 transition-colors text-black dark:text-black"
      >
        <FiDivide className="text-2xl mb-2 text-purple-600 dark:text-purple-600" />
        <span className="text-sm font-medium">Equação</span>
      </button>
      
      <button 
        onClick={() => handleNavigation('/image')}
        className="flex flex-col items-center p-4 bg-orange-100 rounded-lg hover:bg-orange-200 transition-colors text-black dark:text-black"
      >
        <FiPieChart className="text-2xl mb-2 text-orange-600 dark:text-orange-600" />
        <span className="text-sm font-medium">Imagem</span>
      </button>
    </div>
  );
};

export default TutorButtons;

// EXTENSÕES
// - Adicionar animações de transição ao passar o mouse sobre os botões.
// - Implementar um submenu para configurações avançadas de cada modo.
// - Permitir que o logotipo seja dinâmico, recebendo props para personalização.
// - Adicionar suporte a temas (claro/escuro) nos botões.
// - Implementar um sistema de notificações que exiba alertas nos botões.
// - Permitir que os botões sejam personalizados via props (ex: cores, ícones).
// - Adicionar suporte a múltiplos modos de interação (ex: vídeo, chat).
// - Implementar um sistema de feedback que permita ao usuário avaliar cada modo.
// - Adicionar suporte a botões de ação rápida (ex: "Iniciar Tutoria", "Parar Tutoria").
