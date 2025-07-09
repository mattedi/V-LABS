// src/components/collaboration/CollaborationPanel.tsx
//  Implementa um painel interativo de colaboração em tempo real
//  para uma aplicação educacional como o Vibe Learning Studio. 
// Trata-se de um componente React com estado interno. 
// Permitir que o(a) usuário(a)
//  inicie ou encerre uma sessão de colaboração
//  com outros participantes (por exemplo,
//  tutores ou colegas), exibindo quem está conectado com avatares, 
// nomes e status online.


import React, { useState } from 'react';

// Componente Avatar local
const Avatar = ({ src, alt, size = 'sm', role, isOnline }: any) => (
  <div className="relative inline-block">
    <img
      src={src || '/avatars/default.png'}
      alt={alt}
      className={`w-8 h-8 rounded-full object-cover`}
    />
    {isOnline && (
      <div className="absolute bottom-0 right-0 w-2 h-2 bg-green-500 rounded-full"></div>
    )}
  </div>
);

// Componente Button local
const Button = ({ onClick, children, className = '', variant = 'primary' }: any) => {
  const baseClass = variant === 'danger' 
    ? 'bg-red-600 hover:bg-red-700' 
    : 'bg-blue-600 hover:bg-blue-700';
    
  return (
    <button
      onClick={onClick}
      className={`px-4 py-2 text-white rounded-md ${baseClass} ${className}`}
    >
      {children}
    </button>
  );
};

export function CollaborationPanel() {
  const [isCollaborating, setIsCollaborating] = useState(false);
  const [collaborators] = useState([
    {
      id: '1',
      name: 'Ana Silva',
      avatar: '/avatars/ana.png',
      role: 'student',
      isOnline: true,
    },
    {
      id: '2',
      name: 'Prof. Carlos',
      avatar: '/avatars/carlos.png',
      role: 'tutor',
      isOnline: true,
    },
  ]);

  const startCollaboration = () => {
    setIsCollaborating(true);
  };

  const endCollaboration = () => {
    setIsCollaborating(false);
  };

  if (!isCollaborating) {
    return (
      <div className="mt-6 text-center">
        <Button onClick={startCollaboration}>
          Iniciar Sessão Colaborativa
        </Button>
      </div>
    );
  }

  return (
    <div className="mt-6 p-4 bg-gray-800 rounded-lg">
      <div className="flex justify-between items-center">
        <h3 className="text-xl font-semibold text-[#B0D2FF]">
          Colaboração em Tempo Real
        </h3>
        <Button onClick={endCollaboration} variant="danger">
          Encerrar
        </Button>
      </div>
      
      <div className="mt-3">
        <p className="text-sm text-gray-300">Participantes: {collaborators.length + 1}</p>
        <div className="flex mt-2 space-x-2">
          <div className="text-center">
            <Avatar src="/avatars/current-user.png" alt="Você" isOnline={true} />
            <p className="text-xs mt-1 text-white">Você</p>
          </div>
          
          {collaborators.map(user => (
            <div key={user.id} className="text-center">
              <Avatar 
                src={user.avatar} 
                alt={user.name}
                role={user.role}
                isOnline={user.isOnline}
              />
              <p className="text-xs mt-1 text-white">{user.name}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
// EXTENSÕES:
// - Adicionar suporte a chat em tempo real entre os participantes.
// - Implementar notificações quando novos usuários entrarem ou saírem da sessão.
// - Permitir compartilhamento de arquivos ou links dentro da sessão. 