// src/components/Header.tsx
// O componente Header exibe o logotipo, título, 
// links de navegação e ações como alternar tema e exibir avatar do usuário.
// Ele é responsivo e se adapta ao tema claro e escuro,
// mantendo uma aparência consistente e moderna.
//

// src/components/Header.tsx
// O componente Header exibe o logotipo, título, 
// links de navegação e ações como alternar tema e exibir avatar do usuário.
// Ele é responsivo e se adapta ao tema claro e escuro,
// mantendo uma aparência consistente e moderna.
//

import React from 'react';
import { Link } from 'react-router-dom';
import ThemeToggle from './TheToggle'; // ✅ CORRIGIDO: Nome do arquivo estava incorreto
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

//EXTENSÕES:
// - Adicionar suporte a links de navegação adicionais (ex: Perfil, Configurações).
// - Implementar um menu dropdown para o avatar do usuário com opções de logout e perfil.
// - Incluir um botão de ajuda que abra um modal com informações sobre o uso do sistema
// - Adicionar animações sutis ao alternar entre temas.
// - Implementar um sistema de notificações que exiba alertas no header.  
// - Permitir que o título seja dinâmico, recebendo props para personalização.
// - Adicionar suporte a múltiplos idiomas, permitindo que o título seja traduzido.
// - Implementar um sistema de breadcrumbs para navegação hierárquica.
// - Adicionar um botão de pesquisa que abra uma barra de pesquisa no header.
// - Implementar um sistema de breadcrumbs para navegação hierárquica.
//EXTENSÕES:
// - Adicionar suporte a links de navegação adicionais (ex: Perfil, Configurações).
// - Implementar um menu dropdown para o avatar do usuário com opções de logout e perfil.
// - Incluir um botão de ajuda que abra um modal com informações sobre o uso do sistema
// - Adicionar animações sutis ao alternar entre temas.
// - Implementar um sistema de notificações que exiba alertas no header.  
// - Permitir que o título seja dinâmico, recebendo props para personalização.
// - Adicionar suporte a múltiplos idiomas, permitindo que o título seja traduzido.
// - Implementar um sistema de breadcrumbs para navegação hierárquica.
// - Adicionar um botão de pesquisa que abra uma barra de pesquisa no header.
// - Implementar um sistema de breadcrumbs para navegação hierárquica.