// src/components/Header.tsx
import React from 'react';
import { Button, Avatar } from '../common';
import ThemeToggle from './TheToggle';

interface HeaderProps {
  showTitle?: boolean;
}

export default function Header({ showTitle = true }: HeaderProps) {
  return (
    <header className="flex justify-between items-center p-4 bg-white dark:bg-gray-800 shadow-sm rounded-lg transition-colors duration-300">
      <div className="flex items-center gap-3">
        <div className="text-blue-600 dark:text-blue-400 text-3xl font-bold">◢</div>
        {showTitle && (
          <h1 className="text-gray-900 dark:text-gray-100 text-2xl font-semibold">
            Vibe Learning Studio
          </h1>
        )}
      </div>

      <div className="flex items-center gap-4">
        <button
          className="text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors text-sm font-medium"
          aria-label="Abrir documentação"
        >
          Documentação
        </button>
        <ThemeToggle />
        <Avatar initials="ID" isOnline role="student" />
      </div>
    </header>
  );
}
