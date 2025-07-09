// src/components/layout/MainLayout.tsx
// O MainLayout é um layout principal que envolve o conteúdo da aplicação,
// incluindo uma barra de chat e botões de tutoria,
// além de gerenciar a navegação automática baseada no modo selecionado pelo usuário.
// Ele é projetado para ser usado em páginas principais,
// garantindo que a interface seja consistente e responsiva.


import React, { ReactNode } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAppContext } from '../../context/AppContext';
import ChatBar from '../chat/ChatBar';
import TutorButtons from '../tutoring/TutorButtons';

interface MainLayoutProps {
  children: ReactNode;
  showChatBar?: boolean;
  showTutorButtons?: boolean;
}

const MainLayout: React.FC<MainLayoutProps> = ({ 
  children, 
  showChatBar = true,
  showTutorButtons = true
}) => {
  const navigate = useNavigate();
  const { currentMode } = useAppContext();

  // Navegar para a página de tutoria correspondente quando o modo mudar
  React.useEffect(() => {
    if (currentMode === 'equation') {
      navigate('/equation');
    } else if (currentMode === 'voice') {
      navigate('/voice');
    } else if (currentMode === 'image') {
      navigate('/image');
    }
  }, [currentMode, navigate]);

  return (
    <div className="main-layout min-h-screen bg-gray-50">
      {/* Área principal de conteúdo - sem margem left para não interferir com sidebar */}
      <div className="ml-56 p-8"> {/* ml-56 = width do sidebar */}
        <div className="max-w-4xl mx-auto">
          
          {/* REMOVIDO QUALQUER HEADER DAQUI - apenas o Header.tsx global será usado */}
          
          {/* Main Content */}
          <main className="space-y-6">
            {children}
            
            {/* Barra de chat */}
            {showChatBar && (
              <div className="bg-white rounded-lg shadow-md p-6">
                <div className="flex items-center gap-4">
                  <div className="flex-1">
                    <ChatBar compact={true} />
                  </div>
                </div>
              </div>
            )}

            {/* Botões de tutoria */}
            {showTutorButtons && (
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-center text-lg font-semibold text-gray-800 mb-4">
                  Escolha sua tutoria
                </h3>
                <TutorButtons />
              </div>
            )}
          </main>
        </div>
      </div>
    </div>
  );
};

export default MainLayout;

// EXTENSÕES:
// - Adicionar suporte a temas escuros e claros.
// - Implementar um sistema de notificações para mensagens novas.
// - Permitir personalização de layout via props (ex: largura do sidebar, visibilidade de elementos).
// - Implementar breadcrumbs para navegação hierárquica.
// - Adicionar animações sutis ao alternar entre modos de tutoria.
// - Implementar um sistema de feedback para as sessões de tutoria.
// - Permitir que o layout receba props para personalização do título e ícones.
// - Adicionar suporte a links de navegação adicionais (ex: Perfil, Configurações).
// - Implementar um menu dropdown no Header para ações rápidas.
// - Adicionar um botão de ajuda que abra um modal com informações sobre o uso do sistema.