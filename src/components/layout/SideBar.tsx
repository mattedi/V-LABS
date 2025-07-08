// src/components/SideBar.tsx

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
