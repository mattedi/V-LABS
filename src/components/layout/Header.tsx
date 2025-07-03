// src/components/Header.tsx
import React from 'react';
import { FiSettings, FiUpload } from "react-icons/fi";
import { Button, Avatar } from '../common';
import ThemeToggle from './TheToggle';

interface HeaderProps {
  showTitle?: boolean;
}

export default function Header({ showTitle = true }: HeaderProps) {
  return (
    <header className="flex justify-between items-center p-4 bg-dark">
      <div className="flex items-center">
        <div className="text-blue-accent text-3xl mr-2">◢</div>
        {showTitle && (
          <h1 className="text-white text-2xl">Vibe Learning Studio</h1>
        )}
      </div>
      
      <div className="flex items-center gap-4">
        <button className="text-white hover:text-blue-accent transition-colors">
          Documentação
        </button>
        <ThemeToggle />
        <Avatar initials="ID" />
      </div>
    </header>
  );
}