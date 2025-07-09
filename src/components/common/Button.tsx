// src/components/common/Button.tsx
//  Define um componente de botão reutilizável e 
// estilizado para a interface do projeto V-LABS. 
// Ele encapsula a lógica de variações visuais 
// (tema, tamanho, estado de carregamento) e
//  promove consistência visual e reutilização de código.
//  O botão pode ser usado em diferentes contextos,
// como formulários, ações de usuário e feedback visual.
//  Suporta temas (primário, secundário, perigo, sucesso),
// tamanhos (pequeno, médio, grande) e estado de carregamento.



import React, { ButtonHTMLAttributes } from 'react';
import clsx from 'clsx';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger' | 'success';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  children: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  isLoading = false,
  className = '',
  children,
  disabled,
  ...props
}) => {
  const baseClasses =
    'inline-flex items-center justify-center font-semibold rounded-md focus:outline-none transition-colors duration-200';

  const variantClasses: Record<string, string> = {
    primary: 'bg-blue-600 hover:bg-blue-700 text-white',
    secondary: 'bg-gray-600 hover:bg-gray-700 text-white',
    danger: 'bg-red-600 hover:bg-red-700 text-white',
    success: 'bg-green-600 hover:bg-green-700 text-white',
  };

  const sizeClasses: Record<string, string> = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg',
  };

  const computedClass = clsx(
    baseClasses,
    variantClasses[variant],
    sizeClasses[size],
    {
      'opacity-50 cursor-not-allowed': disabled || isLoading,
    },
    className
  );

  return (
    <button
      className={computedClass}
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading ? (
        <div className="flex items-center gap-2">
          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white" />
          <span>Carregando...</span>
        </div>
      ) : (
        children
      )}
    </button>
  );
};

// EXTENSÕES:
// - Adicionar suporte a ícones dentro do botão.
// - Implementar variantes de botão com ícones pré-definidos.
// - Permitir customização de cores via props.  
// - Implementar suporte a botões de ação (ex: "Sim", "Não").
// - Adicionar suporte a botões com tooltip de ajuda.
// - Implementar animações de clique ou hover.
// - Permitir que o botão receba props adicionais para personalização.
// - Adicionar suporte a botões de carregamento com progresso.
// - Implementar suporte a botões de grupo (ex: botões de ação múltip
//  - Adicionar suporte a botões de alternância (toggle).