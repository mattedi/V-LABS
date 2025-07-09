// src/components/common/Avatar.tsx
// serve para exibir identidade visual de um usuário na interface 
// da aplicação V-LABS. Ele foi desenvolvido com flexibilidade para aceitar imagem, 
// iniciais, estados de presença (online) e papéis funcionais (ex: tutor). 
// Renderiza um avatar circular com: Imagem do usuário (se houver src válido),
//Iniciais (caso a imagem não seja fornecida),
//Sinalização se o usuário está online (isOnline),
//Ícone de função específica (por exemplo, "T" para tutor).

import React from 'react';

interface AvatarProps {
  src?: string;
  alt?: string;                 // agora opcional
  initials?: string;            // nova prop
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl';
  className?: string;
  isOnline?: boolean;
  role?: 'student' | 'tutor' | 'teacher';
}

export const Avatar: React.FC<AvatarProps> = ({
  src,
  alt = '',
  initials,
  size = 'md',
  className = '',
  isOnline = false,
  role,
}) => {
  const sizeClasses = {
    xs: 'w-6 h-6',
    sm: 'w-8 h-8',
    md: 'w-10 h-10',
    lg: 'w-12 h-12',
    xl: 'w-16 h-16',
  };

  const hasImage = Boolean(src);

  return (
    <div className={`relative inline-block ${className}`}>
      {hasImage ? (
        <img
          src={src!}
          alt={alt}
          className={`${sizeClasses[size]} rounded-full object-cover`}
          onError={(e) => {
            e.currentTarget.src = '/avatars/default.png';
          }}
        />
      ) : (
        /* círculo com iniciais */
        <div
          className={`${sizeClasses[size]} rounded-full bg-blue-600 flex items-center justify-center text-white font-semibold`}
        >
          {initials?.toUpperCase() || '??'}

        </div>
      )}

      {isOnline && (
        <div className="absolute bottom-0 right-0 w-3 h-3 rounded-full border-2 border-white dark:border-gray-800 bg-green-400" />

      )}

      {role === 'tutor' && (
        <div className="absolute -top-1 -right-1 w-4 h-4 bg-yellow-400 rounded-full flex items-center justify-center">
          <span className="text-xs font-bold text-yellow-900">T</span>
        </div>
      )}
    </div>
  );
};

// Extensões: Aceitar status mais complexos (busy, away, etc.).
// Tooltip com nome ao passar o mouse.
// Suporte a bordas temáticas por role.
// Lazy loading da imagem via loading="lazy".
// Implementar fallback para imagem quebrada.
// Adicionar animação de transição ao trocar o estado online/offline.
// Permitir customização de cores via props.
// Implementar suporte a múltiplos papéis (ex: estudante, professor).
// Permitir que o componente receba props adicionais para personalização.