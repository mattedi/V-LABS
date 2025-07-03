// src/components/SideBar.tsx
import React from 'react';
import { FaRegCommentDots, FaSlidersH, FaHistory } from "react-icons/fa";

export default function SideBar() {
  return (
    <aside className="fixed left-0 top-0 h-full w-56 bg-dark text-white flex flex-col gap-8 p-6">
      <div className="text-primary text-4xl"> {/* Apenas o ícone, SEM o título */}
        ◢
      </div>
      
      {/* REMOVIDO: <h1 className="text-xl font-bold text-primary">Vibe Learning Studio</h1> */}
      
      <nav className="flex flex-col gap-6 mt-8">
        <MenuItem icon={<FaRegCommentDots size={24} />} label="Chat" />
        <MenuItem icon={<FaSlidersH size={24} />} label="Ajustes" />
        <MenuItem icon={<FaHistory size={24} />} label="Histórico" />
      </nav>
    </aside>
  );
}

interface MenuItemProps {
  icon: React.ReactNode;
  label: string;
}

function MenuItem({ icon, label }: MenuItemProps) {
  return (
    <div className="flex items-center gap-3 p-2 rounded-lg hover:bg-[#333] cursor-pointer transition">
      <div className="text-primary">{icon}</div>
      <span>{label}</span>
    </div>
  );
}