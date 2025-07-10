// src/context/ThemeContext.tsx
// Contexto de tema - gerencia o tema claro/escuro da aplicação
// Permite alternar entre temas e aplica classes CSS correspondentes
// Este arquivo define o contexto de tema, que é usado para gerenciar o tema claro/escuro
// de uma aplicação React. Ele permite que qualquer componente envolvido pelo `ThemeProvider`
// acesse e manipule o tema atual, além de aplicar classes CSS correspondentes
// para estilização. O tema é armazenado no `localStorage` para persistência entre recarregamentos.

// ThemeContext.tsx

import React, { createContext, useContext, useState, ReactNode } from 'react';

interface ThemeContextType {
  isDarkMode: boolean;
  toggleDarkMode: () => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export const ThemeProvider = ({ children }: { children: ReactNode }) => {
  const [isDarkMode, setIsDarkMode] = useState(true);

  const toggleDarkMode = () => setIsDarkMode(prev => !prev);

  return (
    <ThemeContext.Provider value={{ isDarkMode, toggleDarkMode }}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useThemeContext = (): ThemeContextType => {
  const context = useContext(ThemeContext);
  if (!context) throw new Error('useThemeContext must be used within a ThemeProvider');
  return context;
};

//EXTENSÕES
// - Adicionar animação de transição suave ao alternar entre temas.
// - Implementar um sistema de preferências do usuário para salvar o tema selecionado.
// - Permitir que o usuário escolha entre mais de dois temas (ex: tema claro, escuro e colorido).
// - Adicionar suporte a temas personalizados via props.
// - Implementar um sistema de notificações que informe o usuário sobre a mudança de tema.
// - Adicionar um tooltip que exiba o nome do tema atual ao passar o mouse sobre o botão.
// - Implementar um sistema de temas dinâmicos que mude automaticamente com base na hora do dia.
// - Permitir que o tema seja alterado via configuração global da aplicação.
// - Adicionar suporte a temas com cores personalizadas definidas pelo usuário.
