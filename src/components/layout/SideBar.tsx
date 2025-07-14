// src/components/SideBar.tsx
// define o componente de barra lateral de navegação da aplicação V-LABS,
//  construído em React com ícones, 
// roteamento via react-router-dom e estilização com TailwindCSS.
//  Ele exibe um logotipo, três itens de menu (Chat, Ajustes e Histórico)
//  e utiliza o NavLink para navegação,
//  destacando o item ativo com uma classe CSS específica.

// src/components/layout/SideBar.tsx

// src/components/SideBar.tsx
// define o componente de barra lateral de navegação da aplicação V-LABS,
//  construído em React com ícones, 
// roteamento via react-router-dom e estilização com TailwindCSS.
//  Ele exibe um logotipo, três itens de menu (Chat, Ajustes e Histórico)
//  e utiliza o NavLink para navegação,
//  destacando o item ativo com uma classe CSS específica.

// src/components/layout/SideBar.tsx
// src/components/layout/UnifiedLayout.tsx
// Layout principal unificado que consolida as funcionalidades dos layouts existentes
// Combina SideBar, TopBar e área de conteúdo principal em uma estrutura coesa
// Suporta tema escuro/claro, responsividade e diferentes tipos de conteúdo

// src/components/layout/UnifiedLayout.tsx
// Layout principal unificado que consolida as funcionalidades dos layouts existentes
// Combina SideBar, TopBar e área de conteúdo principal em uma estrutura coesa
// Suporta tema escuro/claro, responsividade e diferentes tipos de conteúdo

// src/components/layout/SideBar.tsx
// CORRIGIDO: Contextos padronizados com responsabilidades bem definidas
// useThemeContext para tema, useAppContext para configurações de app

import React, { useState, JSX } from 'react';
import { NavLink } from 'react-router-dom';
import {
  FiMessageCircle,
  FiSliders,
  FiClock,
  FiChevronDown,
  FiChevronUp,
} from 'react-icons/fi';
import { useThemeContext } from '../../context/ThemeContext';
import { useAppContext } from '../../context/AppContext';

interface MenuItemProps {
  to: string;
  icon: React.ReactNode;
  label: string;
}

function MenuItem({ to, icon, label }: MenuItemProps): JSX.Element {
  const { isDarkMode } = useThemeContext();

  return (
    <NavLink
      to={to}
      title={label}
      aria-label={label}
      className={({ isActive }) =>
        `flex items-center gap-3 w-full px-4 py-2 rounded-lg text-sm transition-colors duration-200
         ${isActive
           ? `${isDarkMode ? 'bg-gray-700 text-white' : 'bg-gray-300 text-gray-900'} font-semibold`
           : `${isDarkMode ? 'hover:bg-gray-700' : 'hover:bg-gray-200'}`
         }`
      }
    >
      <span className="text-blue-400">{icon}</span>
      <span>{label}</span>
    </NavLink>
  );
}

export default function SideBar(): JSX.Element {
  const { isDarkMode } = useThemeContext();
  const { fontSize } = useAppContext();
  const [showHistorico, setShowHistorico] = useState(false);

  return (
    <aside
      className={`fixed left-0 top-0 h-full w-48 flex flex-col items-start p-6 shadow-lg z-50 transition-all duration-300
        ${isDarkMode ? 'bg-gray-800 text-white' : 'bg-gray-100 text-gray-900'}`}
      style={{ fontSize }}
      role="navigation"
      aria-label="Barra lateral de navegação"
    >
      <div className="text-3xl text-blue-400 font-bold mb-10" aria-hidden="true">
        ◢
      </div>

      <nav className="flex flex-col gap-4 w-full">
        <MenuItem to="/chat" icon={<FiMessageCircle size={20} />} label="Chat" />
        <MenuItem to="/ajustes" icon={<FiSliders size={20} />} label="Ajustes" />

        {/* Menu expandível - Histórico */}
        <button
          onClick={() => setShowHistorico(!showHistorico)}
          className={`flex items-center justify-between w-full px-4 py-2 rounded-lg text-sm transition-colors duration-200 
            ${isDarkMode ? 'hover:bg-gray-700' : 'hover:bg-gray-200'}`}
        >
          <span className="flex items-center gap-2">
            <FiClock size={20} className="text-blue-400" />
            Histórico
          </span>
          {showHistorico ? <FiChevronUp /> : <FiChevronDown />}
        </button>

        {showHistorico && (
          <div className="ml-6 flex flex-col gap-2">
            <MenuItem
              to="/historico/competencias"
              icon={<span className="w-2 h-2 bg-blue-400 rounded-full" />}
              label="Competências"
            />
            <MenuItem
              to="/historico/estudantes"
              icon={<span className="w-2 h-2 bg-blue-400 rounded-full" />}
              label="Estudantes"
            />
          </div>
        )}
      </nav>
    </aside>
  );
}


// EXTENSÕES:
// - Adicionar animações de transição ao passar o mouse sobre os itens do menu.
// - Implementar um submenu para configurações avançadas.
// - Permitir que o logotipo seja dinâmico, recebendo props para personalização.
// - Implementar um sistema de notificações que exiba alertas na barra lateral.
// - Permitir que a barra lateral seja recolhida/expandida com um botão.
// - Adicionar suporte a links externos (ex: Documentação, Suporte).
// - Implementar um sistema de breadcrumbs para navegação hierárquica.
// - Adicionar um botão de pesquisa que abra uma barra de pesquisa na barra lateral.
// - Implementar um menu dropdown para ações rápidas (ex: Perfil, Configurações).
