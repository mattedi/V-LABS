// src/components/Header.tsx
import React from 'react';
import { Link } from 'react-router-dom';
import ThemeToggle from './TheToggle'; // Verifique se o nome do arquivo está correto
import { Avatar } from '../common';

interface HeaderProps {
  showTitle?: boolean;
}

export default function Header({ showTitle = true }: HeaderProps) {
  return (
    <header className="flex justify-between items-center p-4 bg-white dark:bg-gray-800 shadow-sm transition-colors duration-300 z-40 relative">
      
      {/* Logotipo e Título */}
      <div className="flex items-center gap-3">
        <div className="text-blue-600 dark:text-blue-400 text-3xl font-bold select-none">◢</div>
        {showTitle && (
          <h1 className="text-gray-900 dark:text-gray-100 text-2xl font-semibold whitespace-nowrap">
            Vibe Learning Studio
          </h1>
        )}
      </div>

      {/* Ações */}
      <div className="flex items-center gap-4">
        <Link
          to="/docs"
          className="text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors text-sm font-medium"
        >
          Documentação
        </Link>
        <ThemeToggle />
        <Avatar initials="ID" isOnline role="student" />
      </div>
    </header>
  );
}
