// src/components/layout/Layout.tsx
// Serve como estrutura visual principal da interface do projeto V-LABS. 
// Ele organiza os elementos centrais da aplicação — 
// como a barra lateral (Sidebar), o cabeçalho superior (Header) 
// e a área principal de conteúdo (children) — 
// dentro de um container com suporte a tema escuro
//  (dark mode) e responsividade básica.

import React from 'react';
import Sidebar from './SideBar';
import Header from './Header';

interface LayoutProps {
  children: React.ReactNode;
}

export default function Layout({ children }: LayoutProps): React.JSX.Element {
  return (
    <div className="min-h-screen bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 transition-colors duration-300">
      <Sidebar />
      <main className="ml-44 p-4"> {/* ← Agora inclui o Header */}
        <Header />
        {children}
      </main>
    </div>
  );
}

//EXTENSÕES:
// - Adicionar suporte a breadcrumbs para navegação hierárquica.
// - Implementar um menu dropdown no Header para ações rápidas.
// - Incluir um botão de ajuda que abra um modal com informações sobre o uso do sistema.
// - Implementar um sistema de notificações que exiba alertas no Header.
// - Permitir que o Header receba props para personalização do título.
// - Adicionar suporte a links de navegação adicionais (ex: Perfil, Configurações).
// - Implementar um menu lateral responsivo que se adapte a telas menores.
// - Adicionar animações sutis ao alternar entre temas.
// - Implementar um sistema de breadcrumbs para navegação hierárquica.
// - Adicionar um botão de pesquisa que abra uma barra de pesquisa no Header.