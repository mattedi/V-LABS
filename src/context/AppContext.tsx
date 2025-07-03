// src/context/AppContext.tsx
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

// =====================================
// COMO USAR ESTE CONTEXTO:
// =====================================

/**
 * 1. No App.tsx - Envolver toda a aplicação:
 * 
 * function App() {
 *   return (
 *     <AppProvider>
 *       <Router>
 *         <Routes>
 *           // suas rotas aqui
 *         </Routes>
 *       </Router>
 *     </AppProvider>
 *   );
 * }
 */

/**
 * 2. Em qualquer componente - Usar o contexto:
 * 
 * function MeuComponente() {
 *   const { currentMode, setCurrentMode, isDarkMode, toggleDarkMode } = useAppContext();
 * 
 *   return (
 *     <div>
 *       <p>Modo atual: {currentMode}</p>
 *       <button onClick={() => setCurrentMode('voice')}>
 *         Mudar para Voz
 *       </button>
 *       
 *       <p>Tema: {isDarkMode ? 'Escuro' : 'Claro'}</p>
 *       <button onClick={toggleDarkMode}>
 *         Trocar Tema
 *       </button>
 *     </div>
 *   );
 * }
 */

/**
 * 3. Exemplo real no TutorButtons:
 * 
 * function TutorButtons() {
 *   const { setCurrentMode } = useAppContext();
 * 
 *   return (
 *     <div>
 *       <button onClick={() => setCurrentMode('text')}>
 *         Texto
 *       </button>
 *       <button onClick={() => setCurrentMode('voice')}>
 *         Voz
 *       </button>
 *     </div>
 *   );
 * }
 */

/**
 * 4. Exemplo no Header para trocar tema:
 * 
 * function Header() {
 *   const { isDarkMode, toggleDarkMode } = useAppContext();
 * 
 *   return (
 *     <header className={isDarkMode ? 'bg-dark' : 'bg-light'}>
 *       <button onClick={toggleDarkMode}>
 *         {isDarkMode ? '🌙' : '☀️'}
 *       </button>
 *     </header>
 *   );
 * }
 */

// =====================================
// VANTAGENS DESTE CONTEXTO:
// =====================================

/**
 * ✅ PERSISTÊNCIA: Dados salvos no localStorage (não perde ao recarregar)
 * ✅ GLOBAL: Qualquer componente pode acessar e modificar
 * ✅ REATIVO: Quando muda, todos os componentes que usam são atualizados
 * ✅ TIPADO: TypeScript garante que você use corretamente
 * ✅ SEGURO: Erro claro se usar fora do Provider
 * 
 * SEM CONTEXTO (problemático):
 * - Passar props por 10 níveis de componentes
 * - Estado duplicado em vários lugares
 * - Perda de dados ao recarregar
 * 
 * COM CONTEXTO (melhor):
 * - Acesso direto em qualquer componente
 * - Estado único e consistente
 * - Persistência automática
 */