// src/components/layout/SettingsPanel.tsx
// Este componente exibe um painel de configurações para o usuário,
// permitindo que ele alterne entre temas claro e escuro, visualize suas informações de usuário
// e faça logout da conta. Ele utiliza o contexto de tema e autenticação para gerenciar
// o estado do tema e as informações do usuário. O painel é responsivo e estilizado
// para se adaptar ao tema selecionado, garantindo uma experiência de usuário consistente e moderna.

import React from 'react';
import { useAppContext } from '../../context/AppContext';

export default function SettingsPanel() {
  const {
    isDarkMode,
    toggleDarkMode,
    fontSize,
    setFontSize,
    language,
    setLanguage,
    avatarInitials,
    setAvatarInitials,
    avatarRole,
    setAvatarRole,
  } = useAppContext();

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Ajustes</h1>

      {/* Tema */}
      <div className="mb-6">
        <label className="block mb-2 font-medium">Tema</label>
        <button
          onClick={toggleDarkMode}
          className="px-4 py-2 bg-gray-200 dark:bg-gray-700 rounded text-gray-800 dark:text-white"
        >
          {isDarkMode ? 'Modo Escuro' : 'Modo Claro'}
        </button>
      </div>

      {/* Tamanho da Fonte */}
      <div className="mb-6">
        <label className="block mb-2 font-medium">Tamanho da Fonte</label>
        <select
          value={fontSize}
          onChange={(e) => setFontSize(e.target.value)}
          className="px-4 py-2 border border-gray-300 rounded bg-white text-gray-900 dark:bg-gray-700 dark:text-white"
        >
          <option value="text-sm">Pequena</option>
          <option value="text-base">Média</option>
          <option value="text-lg">Grande</option>
          <option value="text-xl">Muito Grande</option>
        </select>
      </div>

      {/* Idioma */}
      <div className="mb-6">
        <label className="block mb-2 font-medium">Idioma</label>
        <select
          value={language}
          onChange={(e) => setLanguage(e.target.value as 'pt' | 'en')}
          className="px-4 py-2 border border-gray-300 rounded bg-white text-gray-900 dark:bg-gray-700 dark:text-white"
        >
          <option value="pt">Português</option>
          <option value="en">English</option>
        </select>
      </div>

      {/* Iniciais do Avatar */}
      <div className="mb-6">
        <label className="block mb-2 font-medium">Iniciais do Avatar</label>
        <input
          type="text"
          maxLength={3}
          value={avatarInitials}
          onChange={(e) => setAvatarInitials(e.target.value.toUpperCase())}
          className="px-4 py-2 border border-gray-300 rounded w-32 bg-white text-gray-900 dark:bg-gray-700 dark:text-white"
        />
      </div>

      {/* Papel do Usuário */}
      <div className="mb-6">
        <label className="block mb-2 font-medium">Papel do Usuário</label>
        <select
          value={avatarRole}
          onChange={(e) => setAvatarRole(e.target.value as 'student' | 'tutor' | 'teacher')}
          className="px-4 py-2 border border-gray-300 rounded bg-white text-gray-900 dark:bg-gray-700 dark:text-white"
        >
          <option value="student">Estudante</option>
          <option value="tutor">Tutor</option>
          <option value="teacher">Professor</option>
        </select>
      </div>
    </div>
  );
}



// Extensões:
// - Adicionar opções de personalização de perfil (ex: foto, biografia).
// - Implementar um sistema de notificações para alertas de segurança (ex: login suspeito).
// - Permitir que o usuário altere sua senha diretamente no painel.
// - Adicionar suporte a autenticação de dois fatores (2FA) para maior segurança.
// - Implementar um histórico de atividades do usuário (ex: últimos logins, alterações de perfil).
// - Adicionar uma seção de preferências de comunicação (ex: notificações por e-mail).
// - Permitir que o usuário escolha entre diferentes temas pré-definidos (ex: claro, escuro, colorido).
// - Implementar um sistema de feedback onde o usuário pode enviar sugestões ou relatar problemas.
// - Adicionar uma seção de ajuda com links para documentação e suporte.
// - Implementar um sistema de backup e restauração de configurações do usuário.
