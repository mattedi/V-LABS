// Define um componente MobileMenu em React,
// destinado a exibir um menu lateral em 
// dispositivos móveis (escondido em telas médias para cima, 
// visível apenas em telas pequenas). 
// Ele utiliza o estado interno para controlar a visibilidade do menu,
// alternando entre um ícone de menu (hambúrguer) e um í
// cone de fechar (X) quando o menu está aberto ou fechado.
//  O menu é estilizado com classes CSS e transições para uma experiência de usuário suave.   

import { FiMenu, FiX } from 'react-icons/fi';
import React, { useState, ReactNode } from 'react';


interface MobileMenuProps {
  children: ReactNode;
}

export default function MobileMenu({ children }: MobileMenuProps) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="md:hidden">
      <button 
        onClick={() => setIsOpen(!isOpen)}
        className="fixed top-4 left-4 z-50 p-2 rounded-full bg-primary text-white"
      >
        {isOpen ? <FiX size={24} /> : <FiMenu size={24} />}
      </button>

      <div 
        className={`fixed inset-0 bg-dark z-40 transform ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        } transition-transform duration-300 ease-in-out`}
      >
        <div className="pt-16 px-4">
          {children}
        </div>
      </div>
    </div>
  );
}

// EXTENSÕES
// - Adicionar animações de transição mais suaves ao abrir/fechar o menu.
// - Implementar links de navegação dentro do menu.
// - Permitir que o menu seja fechado ao clicar fora dele.
// - Adicionar suporte a temas (claro/escuro) no menu.
// - Implementar um botão de pesquisa dentro do menu.
// - Adicionar um logotipo ou título no topo do menu.
// - Implementar um sistema de breadcrumbs para navegação hierárquica.
// - Permitir que o menu receba props para personalização de estilo.
// - Adicionar suporte a submenus para categorias de links.

