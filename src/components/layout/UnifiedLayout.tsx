// src/components/layout/UnifiedLayout.tsx
// Layout principal unificado que consolida as funcionalidades dos layouts existentes
// Combina SideBar, TopBar e área de conteúdo principal em uma estrutura coesa
// Suporta tema escuro/claro, responsividade e diferentes tipos de conteúdo

// src/components/layout/UnifiedLayout.tsx
// Layout principal unificado com autenticação funcional
// Integra SideBar, TopBar e área de conteúdo com logout operacional

import React, { ReactNode, useState, useRef, useEffect } from 'react';
import { FiSun, FiMoon, FiFile } from 'react-icons/fi';
import { useAppContext } from '../../context/AppContext';
import { useAuth } from '../../context/AuthContext';
import SideBar from './SideBar';

/* ======================================
   TopBar Integrada com Autenticação
   ====================================== */
interface TopBarProps {
  pageTitle?: string;
}

const TopBarIntegrated: React.FC<TopBarProps> = ({ pageTitle = 'VIBE LEARNING STUDIO' }) => {
  const { isDarkMode, toggleDarkMode } = useAppContext();
  const { user, logout, isLoading, isAuthenticated } = useAuth();
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Fecha dropdown clicando fora
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsDropdownOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const handleLogout = async () => {
    try {
      setIsDropdownOpen(false);
      await logout();
      // Navegação será tratada por componentes de rota protegida
    } catch (error) {
      console.error('Erro ao fazer logout:', error);
      alert('Erro ao fazer logout. Tente novamente.');
    }
  };

  // Extrair iniciais do usuário
  const getUserInitials = (username?: string): string => {
    if (!username) return 'U';
    return username
      .split(' ')
      .map(word => word.charAt(0).toUpperCase())
      .slice(0, 2)
      .join('');
  };

  return (
    <header className="flex justify-between items-center px-4 py-2 bg-white dark:bg-gray-800 shadow">
      {/* Título da Página */}
      <div className="flex items-center gap-2 text-lg font-semibold text-gray-900 dark:text-white">
        <FiFile className="text-2xl shrink-0 text-blue-600 dark:text-blue-400" />
        <span>{pageTitle}</span>
      </div>

      {/* Ações do Usuário */}
      <div className="flex items-center gap-4 relative" ref={dropdownRef}>
        <a
          href="/docs"
          className="text-sm font-medium text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
        >
          Documentação
        </a>

        <button
          onClick={toggleDarkMode}
          className="p-2 rounded-full bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-100 hover:bg-gray-300 dark:hover:bg-gray-600 transition"
          aria-label="Alternar tema claro/escuro"
          title={isDarkMode ? 'Ativar tema claro' : 'Ativar tema escuro'}
        >
          {isDarkMode ? <FiSun /> : <FiMoon />}
        </button>

        {/* Avatar com Estado Condicional */}
        {isAuthenticated ? (
          // Usuário Logado - Avatar com Dropdown
          <>
            <button
              onClick={() => setIsDropdownOpen(!isDropdownOpen)}
              className="flex items-center justify-center w-8 h-8 bg-blue-600 text-white rounded-full text-sm font-semibold hover:bg-blue-700 transition-colors"
              aria-label="Menu do usuário"
              title={user ? `Logado como ${user.username}` : 'Menu do usuário'}
            >
              {getUserInitials(user?.username)}
            </button>

            {/* Dropdown para Usuário Logado */}
            {isDropdownOpen && (
              <div className="absolute right-0 top-12 mt-1 w-48 bg-white dark:bg-gray-700 rounded-md shadow-lg border border-gray-200 dark:border-gray-600 z-50">
                <div className="py-1">
                  {/* Informações do Usuário */}
                  {user && (
                    <div className="px-4 py-2 border-b border-gray-200 dark:border-gray-600">
                      <p className="text-sm font-medium text-gray-900 dark:text-white">
                        {user.username}
                      </p>
                      <p className="text-xs text-gray-500 dark:text-gray-400">
                        {user.email}
                      </p>
                    </div>
                  )}

                  {/* Links do Menu */}
                  <a 
                    href="/dashboard" 
                    className="block px-4 py-2 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors"
                    onClick={() => setIsDropdownOpen(false)}
                  >
                    Dashboard
                  </a>
                  <a 
                    href="/perfil" 
                    className="block px-4 py-2 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors"
                    onClick={() => setIsDropdownOpen(false)}
                  >
                    Meu Perfil
                  </a>
                  <a 
                    href="/ajustes" 
                    className="block px-4 py-2 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors"
                    onClick={() => setIsDropdownOpen(false)}
                  >
                    Configurações
                  </a>

                  <hr className="border-gray-200 dark:border-gray-600" />

                  {/* Logout Funcional */}
                  <button
                    onClick={handleLogout}
                    disabled={isLoading}
                    className="block w-full text-left px-4 py-2 text-sm text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {isLoading ? 'Saindo...' : 'Sair'}
                  </button>
                </div>
              </div>
            )}
          </>
        ) : (
          // Usuário Não Logado - Botão de Login
          <div className="flex items-center gap-2">
            <a
              href="/register"
              className="px-3 py-1.5 text-sm text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
            >
              Cadastrar
            </a>
            <a
              href="/login"
              className="px-4 py-1.5 bg-blue-600 text-white text-sm rounded-md hover:bg-blue-700 transition-colors"
            >
              Entrar
            </a>
          </div>
        )}
      </div>
    </header>
  );
};

/* ======================================
   UnifiedLayout Principal
   ====================================== */
interface UnifiedLayoutProps {
  children: ReactNode;
  pageTitle?: string;
  showTopBar?: boolean;
  showChatBar?: boolean;
  showTutorButtons?: boolean;
  className?: string;
}

const UnifiedLayout: React.FC<UnifiedLayoutProps> = ({
  children,
  pageTitle = 'Documentos',
  showTopBar = true,
  showChatBar = false,
  showTutorButtons = false,
  className = '',
}) => {
  const { isDarkMode, fontSize } = useAppContext();
  // Removida verificação de autenticação do layout - deve ser feita nas rotas

  return (
    <div className={isDarkMode ? 'dark' : ''}>
      <div
        className={`flex min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white transition-all duration-300 ${fontSize} ${className}`}
      >
        {/* Barra Lateral - Props condicionais para compatibilidade */}
        <SideBar 
          {...(showChatBar !== undefined && { showChatBar })}
          {...(showTutorButtons !== undefined && { showTutorButtons })}
        />

        {/* Área de Conteúdo */}
        <div className="flex flex-col flex-1 ml-48">
          {showTopBar && <TopBarIntegrated pageTitle={pageTitle} />}
          <main className="flex-1 p-6 overflow-y-auto">
            <div className="max-w-6xl mx-auto space-y-6">
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