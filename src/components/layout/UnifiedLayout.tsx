// src/components/layout/UnifiedLayout.tsx
// Layout principal unificado que consolida as funcionalidades dos layouts existentes
// Combina SideBar, TopBar e área de conteúdo principal em uma estrutura coesa
// Suporta tema escuro/claro, responsividade e diferentes tipos de conteúdo


import React, { ReactNode } from 'react';
import { FiSun, FiMoon, FiFile } from 'react-icons/fi';
import { useAppContext } from '../../context/AppContext';
import SideBar from './SideBar';

// ===== COMPONENTE TopBar INTEGRADO =====
interface TopBarProps {
  pageTitle?: string;
}

const TopBarIntegrated: React.FC<TopBarProps> = ({ pageTitle = "VIBE LEARNING STUDIO" }) => {
  const { isDarkMode, toggleDarkMode } = useAppContext();

  return (
    <header className="flex justify-between items-center px-4 py-2 bg-white dark:bg-gray-800 shadow">
      
      {/* Título com ícone funcional */}
      <div className="flex items-center gap-2 text-lg font-semibold text-gray-900 dark:text-white">
        <FiFile className="text-2xl shrink-0 text-blue-600 dark:text-blue-400" />
        <span>{pageTitle}</span>
      </div>

      {/* Ações à direita */}
      <div className="flex items-center gap-4">
        
        {/* Link para Documentação */}
        <a
          href="/docs"
          className="text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors text-sm font-medium"
        >
          Documentação
        </a>

        {/* Botão de alternância de tema */}
        <button
          onClick={toggleDarkMode}
          className="p-2 rounded-full bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-100 hover:bg-gray-300 dark:hover:bg-gray-600 transition"
          aria-label="Alternar tema claro/escuro"
          title={isDarkMode ? 'Ativar tema claro' : 'Ativar tema escuro'}
        >
          {isDarkMode ? <FiSun /> : <FiMoon />}
        </button>

        {/* Avatar do usuário */}
        <div className="flex items-center justify-center w-8 h-8 bg-blue-600 text-white rounded-full text-sm font-semibold">
          MM
        </div>
      </div>
    </header>
  );
};

// ===== INTERFACE CORRIGIDA =====
interface UnifiedLayoutProps {
  children: ReactNode;
  pageTitle?: string;
  showTopBar?: boolean;
  showChatBar?: boolean;
  showTutorButtons?: boolean;
  className?: string;
}

// ===== COMPONENTE LAYOUT PRINCIPAL =====
const UnifiedLayout: React.FC<UnifiedLayoutProps> = ({
  children,
  pageTitle = "Documentos",
  showTopBar = true,
  showChatBar = false,
  showTutorButtons = false,
  className = ""
}) => {
  const { fontSize, isDarkMode } = useAppContext();

  return (
    <div className={isDarkMode ? 'dark' : ''}>
      <div
        className={`flex min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white transition-all duration-300 ${className}`}
        style={{ fontSize }}
      >
        {/* Barra Lateral Fixa */}
        <SideBar />

        {/* Área Principal com TopBar e Conteúdo */}
        <div className="flex flex-col flex-1 ml-48">
          
          {/* TopBar Condicional */}
          {showTopBar && (
            <TopBarIntegrated pageTitle={pageTitle} />
          )}

          {/* Container Principal de Conteúdo */}
          <main className="flex-1 p-6 overflow-y-auto">
            <div className="max-w-6xl mx-auto space-y-6">
              
              {/* Conteúdo Principal */}
              <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6 transition-colors duration-300">
                {children}
              </div>
              
            </div>
          </main>
        </div>
      </div>
    </div>
  );
};

export default UnifiedLayout;
// EXTENSÕES FUTURAS:
// - Sistema de breadcrumbs dinâmico
// - Menu dropdown para avatar com perfil/logout
// - Notificações em tempo real
// - Pesquisa global integrada
// - Suporte a múltiplos idiomas
// - Sistema de ajuda contextual
// - Atalhos de teclado
// - Modo de alto contraste
// - Layout adaptativo para tablets
// - Sistema de favoritos/bookmarks

// EXTENSÕES FUTURAS:
// - Sistema de breadcrumbs dinâmico
// - Menu dropdown para avatar com perfil/logout
// - Notificações em tempo real
// - Pesquisa global integrada
// - Suporte a múltiplos idiomas
// - Sistema de ajuda contextual
// - Atalhos de teclado
// - Modo de alto contraste
// - Layout adaptativo para tablets
// - Sistema de favoritos/bookmarks

// EXTENSÕES FUTURAS:
// - Sistema de breadcrumbs dinâmico
// - Menu dropdown para avatar com perfil/logout
// - Notificações em tempo real
// - Pesquisa global integrada
// - Suporte a múltiplos idiomas
// - Sistema de ajuda contextual
// - Atalhos de teclado
// - Modo de alto contraste
// - Layout adaptativo para tablets
// - Sistema de favoritos/bookmarks

// EXTENSÕES FUTURAS:
// - Sistema de breadcrumbs dinâmico
// - Menu dropdown para avatar com perfil/logout
// - Notificações em tempo real
// - Pesquisa global integrada
// - Suporte a múltiplos idiomas
// - Sistema de ajuda contextual
// - Atalhos de teclado
// - Modo de alto contraste
// - Layout adaptativo para tablets
// - Sistema de favoritos/bookmarks