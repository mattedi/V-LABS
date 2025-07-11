// src/context/AppContext.tsx
// Armazena o estado global do app
// Fornece o contexto aos componentes da aplicação
// Define um Contexto Global para uma aplicação React. 
// Define o tipo de tutoria em uso (texto, voz, etc.)
// Ele permite compartilhar informações globais 
// (como o modo de tutoria e o tema visual) entre todos os componentes da aplicação, 
// sem a necessidade de passar essas informações manualmente por props.
// Contexto global da aplicação - compartilha dados entre todos os componentes
// Guarda: modo atual de tutoria (texto/voz/etc) e tema (claro/escuro)

// src/context/AppContext.tsx

import React, { createContext, useContext, useState, ReactNode } from 'react';
import useLocalStorage from '../hooks/useLocalStorage';

type TutorMode = 'text' | 'voice' | 'equation' | 'image';
type Role = 'student' | 'tutor' | 'teacher';
type Language = 'pt' | 'en';

interface AppContextType {
  currentMode: TutorMode;
  setCurrentMode: (mode: TutorMode) => void;
  isDarkMode: boolean;
  toggleDarkMode: () => void;
  fontSize: string;
  setFontSize: (size: string) => void;
  language: Language;
  setLanguage: (lang: Language) => void;
  avatarInitials: string;
  setAvatarInitials: (val: string) => void;
  avatarRole: Role;
  setAvatarRole: (val: Role) => void;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export function AppProvider({ children }: { children: ReactNode }) {
  const [currentMode, setCurrentMode] = useLocalStorage<TutorMode>('tutor-mode', 'text');
  const [isDarkMode, setIsDarkMode] = useLocalStorage<boolean>('dark-mode', true);
  const [fontSize, setFontSize] = useLocalStorage<string>('font-size', 'text-base');
  const [language, setLanguage] = useLocalStorage<Language>('language', 'pt');

  const [avatarInitials, setAvatarInitials] = useLocalStorage<string>('avatar-initials', 'MM');
  const [avatarRole, setAvatarRole] = useLocalStorage<Role>('avatar-role', 'student');

  const toggleDarkMode = () => setIsDarkMode(!isDarkMode);

  return (
    <AppContext.Provider
      value={{
        currentMode,
        setCurrentMode,
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
      }}
    >
      {children}
    </AppContext.Provider>
  );
}

export function useAppContext(): AppContextType {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useAppContext must be used within an AppProvider');
  }
  return context;
}





// EXTENSÕES
// - Adicionar suporte a múltiplos modos de tutoria (ex: matemática, ciências, etc.).
// - Implementar um sistema de temas dinâmico que mude automaticamente com base na hora do dia.
// - Permitir que o usuário personalize o tema (cores, fontes, etc.).
// - Implementar um sistema de notificações que informe o usuário sobre mudanças de modo ou tema.
// - Adicionar suporte a múltiplos idiomas, permitindo que o usuário escolha o idioma da interface.
// - Implementar um sistema de feedback que permita ao usuário avaliar cada modo de tutoria.
// - Adicionar suporte a perfis de usuário, permitindo que cada usuário tenha suas próprias preferências de modo e tema.
// - Implementar um sistema de histórico que registre as mudanças de modo e tema do usuário.
// - Adicionar suporte a temas personalizados via props, permitindo que o usuário escolha entre diferentes estilos visuais.
// - Implementar um sistema de autenticação que permita ao usuário salvar suas preferências de modo e tema em um servidor.  
// - Adicionar suporte a temas com cores personalizadas definidas pelo usuário.