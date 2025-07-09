// src/config/layoutConfig.ts
// Arquivo que define quem é responsável por renderizar cada parte da interface
// Ajuda a evitar duplicações e manter organização

/**
 * Define qual componente deve renderizar cada elemento da UI
 * Usado para evitar que o mesmo título/elemento apareça em vários lugares
 */
export const LAYOUT_RESPONSIBILITIES = {
  // === TÍTULOS E CABEÇALHOS ===
  MAIN_TITLE: 'Header.tsx',           // Só o Header pode mostrar "Vibe Learning Studio"
  PAGE_TITLES: 'Individual Pages',    // Cada página tem seu próprio título ("Modo de Voz", etc.)
  WELCOME_MESSAGE: 'MainLayout.tsx',  // "Escolha sua tutoria" fica no MainLayout
  
  // === MENUS E NAVEGAÇÃO ===
  SIDEBAR_MENU: 'SideBar.tsx',        // Menu lateral: Chat, Ajustes, Histórico
  TOP_NAVIGATION: 'Header.tsx',       // Botões do topo: Documentação, Avatar, Tema
  
  // === CONTEÚDO PRINCIPAL ===
  CHAT_INTERFACE: 'MainLayout.tsx',   // A barra de chat
  TUTOR_BUTTONS: 'MainLayout.tsx',    // Os botões de tutoria (Texto, Voz, etc.)
  PAGE_CONTENT: 'Individual Pages',   // Conteúdo específico de cada página
} as const;

/**
 * Regras para evitar elementos duplicados na tela
 * Se algo aparece duas vezes, consulte estas regras
 */
export const DUPLICATION_RULES = [
  {
    // Regra 1: Título principal único
    rule: 'NEVER_DUPLICATE_MAIN_TITLE',
    description: 'Apenas Header.tsx deve renderizar "Vibe Learning Studio"',
    components: ['Header.tsx'],          // Quem PODE renderizar
    forbidden: ['SideBar.tsx', 'MainLayout.tsx', 'Pages/*']  // Quem NÃO PODE
  },
  {
    // Regra 2: Uma mensagem de boas-vindas por página
    rule: 'ONE_WELCOME_MESSAGE_PER_PAGE',
    description: 'Apenas uma mensagem de boas-vindas por página',
    components: ['MainLayout.tsx OR Individual Pages'],  // Escolha UM dos dois
    forbidden: ['Multiple components on same page']      // Não ambos na mesma página
  },
  {
    // Regra 3: Títulos de página únicos
    rule: 'UNIQUE_PAGE_TITLES',
    description: 'Cada página deve ter seu próprio título único',
    components: ['Individual Pages'],    // Só as páginas específicas
    forbidden: ['Generic titles in layout components']  // Layouts não devem ter títulos genéricos
  }
] as const;

/**
 * Modelo recomendado para criar novas páginas
 * Copy-paste este exemplo e modifique conforme necessário
 */
export const RECOMMENDED_PAGE_STRUCTURE = `
// Exemplo: VoicePage.tsx
export default function VoicePage() {
  return (
    <MainLayout showChatBar={true} showTutorButtons={true}>
      {/* 1. Título específico da página */}
      <PageTitle>Modo de Voz</PageTitle>
      
      {/* 2. Conteúdo específico da página */}
      <PageContent>
        {/* Suas funcionalidades específicas aqui */}
      </PageContent>
      
      {/* 3. MainLayout já inclui Chat + Botões automaticamente */}
    </MainLayout>
  );
}
`;

/**
 * Lista de verificação antes de criar novos componentes
 * Marque cada item antes de fazer commit
 */
export const COMPONENT_CHECKLIST = [
  '□ Este componente não duplica títulos existentes?',           // Confira LAYOUT_RESPONSIBILITIES
  '□ Este componente tem uma responsabilidade única e clara?',   // Um componente = uma função
  '□ Este componente não renderiza elementos que já existem em outros lugares?',  // Evita duplicação
  '□ Os imports estão corretos e não há circular dependencies?', // ComponenteA não importa ComponenteB que importa ComponenteA
  '□ O componente segue a estrutura recomendada da página?'      // Use RECOMMENDED_PAGE_STRUCTURE
] as const;

// EXTENSÕES
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