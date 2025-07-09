// src/components/SideBar.tsx
// define o componente de barra lateral de navegação da aplicação V-LABS,
//  construído em React com ícones, 
// roteamento via react-router-dom e estilização com TailwindCSS.
//  Ele exibe um logotipo, três itens de menu (Chat, Ajustes e Histórico)
//  e utiliza o NavLink para navegação,
//  destacando o item ativo com uma classe CSS específica.

import React from 'react';
import { NavLink } from 'react-router-dom';
import { FaRegCommentDots, FaSlidersH, FaHistory } from "react-icons/fa";

// Componente principal da barra lateral
export default function SideBar() {
  return (
    <aside className="fixed left-0 top-0 h-full w-44 bg-gray-400 text-white flex flex-col gap-8 p-6 shadow-lg z-50">
      {/* Logotipo ou ícone de marca no topo */}
      <div className="text-primary text-4xl">
        ◢
      </div>

      {/* Menu com os itens navegáveis */}
      <nav className="flex flex-col gap-6 mt-8">
        <MenuItem to="/chat" icon={<FaRegCommentDots size={20} />} label="Chat" />
        <MenuItem to="/ajustes" icon={<FaSlidersH size={20} />} label="Ajustes" />
        <MenuItem to="/historico" icon={<FaHistory size={20} />} label="Histórico" />
      </nav>
    </aside>
  );
}

// Interface que define as props de um item do menu
interface MenuItemProps {
  to: string; // Rota de destino
  icon: React.ReactNode; // Ícone a ser exibido
  label: string; // Texto do menu
}

// Componente reutilizável para cada item de menu
function MenuItem({ to, icon, label }: MenuItemProps) {
  return (
    <NavLink
      to={to}
      className={({ isActive }) =>
        `flex items-center gap-3 p-2 rounded-lg cursor-pointer transition-colors duration-200
         ${isActive ? 'bg-gray-800 font-semibold' : 'hover:bg-gray-800'}`
      }
    >
      <div className="text-primary">{icon}</div>
      <span>{label}</span>
    </NavLink>
  );
}

//EXTENSÕES
// - Adicionar animações de transição ao passar o mouse sobre os itens do menu.
// - Implementar um submenu para configurações avançadas.
// - Permitir que o logotipo seja dinâmico, recebendo props para personalização.
// - Adicionar suporte a temas (claro/escuro) na barra lateral.
// - Implementar um sistema de notificações que exiba alertas na barra lateral.
// - Permitir que a barra lateral seja recolhida/expandida com um botão.
// - Adicionar suporte a links externos (ex: Documentação, Suporte).
// - Implementar um sistema de breadcrumbs para navegação hierárquica.
// - Adicionar um botão de pesquisa que abra uma barra de pesquisa na barra lateral.
// - Implementar um menu dropdown para ações rápidas (ex: Perfil, Configurações).
// - Adicionar suporte a múltiplos idiomas, permitindo que os rótulos sejam traduzidos.