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

import React, { createContext, useContext, useState, ReactNode } from 'react';
import useLocalStorage from '../hooks/useLocalStorage';

/**
 * Tipos de tutoria disponíveis na aplicação
 * Usado para trocar entre diferentes modos
 */
type TutorMode = 'text' | 'voice' | 'equation' | 'image';

/**
 * Define o que o contexto vai compartilhar com todos os componentes
 * Como um "contrato" do que está disponível globalmente
 */
interface AppContextType {
  currentMode: TutorMode;                    // Modo atual selecionado
  setCurrentMode: (mode: TutorMode) => void; // Função para trocar modo
  isDarkMode: boolean;                       // Se está no tema escuro
  toggleDarkMode: () => void;                // Função para trocar tema
}

/**
 * Cria o contexto (ainda vazio)
 * undefined = valor inicial (será preenchido pelo Provider)
 */
const AppContext = createContext<AppContextType | undefined>(undefined);

/**
 * Provider - componente que fornece os dados para toda a aplicação
 * Deve envolver toda a aplicação no App.tsx
 */
export function AppProvider({ children }: { children: ReactNode }) {
  // Estado do modo de tutoria (salva no localStorage automaticamente)
  const [currentMode, setCurrentMode] = useLocalStorage<TutorMode>('tutor-mode', 'text');
  // Parâmetros: chave no localStorage, valor padrão
  
  // Estado do tema escuro (salva no localStorage automaticamente)  
  const [isDarkMode, setIsDarkMode] = useLocalStorage<boolean>('dark-mode', true);
  // Parâmetros: chave no localStorage, valor padrão (true = escuro por padrão)
  
  /**
   * Função para alternar entre tema claro e escuro
   * Troca o valor atual: true vira false, false vira true
   */
  const toggleDarkMode = () => setIsDarkMode(!isDarkMode);

  // Comentário original: A navegação foi removida daqui
  // O contexto só guarda dados, não navega entre páginas
  // Cada componente decide o que fazer quando o modo muda

  return (
    <AppContext.Provider 
      value={{ 
        currentMode,      // Estado atual
        setCurrentMode,   // Função para mudar modo
        isDarkMode,       // Estado do tema
        toggleDarkMode    // Função para mudar tema
      }}
    >
      {children}
      {/* Renderiza todos os componentes filhos */}
    </AppContext.Provider>
  );
}

/**
 * Hook personalizado para usar o contexto
 * Facilita o uso e adiciona verificação de erro
 */
export function useAppContext() {
  // Pega o contexto atual
  const context = useContext(AppContext);
  
  // Verifica se está sendo usado dentro de um Provider
  if (context === undefined) {
    throw new Error('useAppContext must be used within an AppProvider');
    // Erro claro se esquecer de envolver a app com AppProvider
  }
  
  return context; // Retorna os dados do contexto
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