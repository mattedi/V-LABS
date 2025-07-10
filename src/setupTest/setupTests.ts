// src/setupTests.ts

/**
 * Configurações globais para ambiente de testes Jest
 * Este arquivo é executado automaticamente antes de cada arquivo de teste,
 * fornecendo configurações, mocks e extensões necessárias para testar
 * componentes React que usam APIs do navegador.
 * Configurações incluídas:
 * - Extensões de matchers do Testing Library
 * - Mock para matchMedia (media queries)
 * - Mock para IntersectionObserver (lazy loading, animações)
 * - Configurações de compatibilidade entre jsdom e APIs modernas
 * 
 * Referência: Executado por jest.config.js via setupFilesAfterEnv
 * 
 * @see https://testing-library.com/docs/ecosystem-jest-dom/
 * @see https://jestjs.io/docs/configuration#setupfilesafterenv-array
 */

/**
 * Importa matchers customizados do Testing Library para Jest
 * 
 * Adiciona matchers específicos para DOM como:
 * - toBeInTheDocument(): Verifica se elemento existe no DOM
 * - toHaveClass(): Verifica classes CSS
 * - toBeVisible(): Verifica visibilidade do elemento
 * - toHaveTextContent(): Verifica conteúdo de texto
 * - toBeDisabled(): Verifica se elemento está desabilitado
 * 
 * Permite escrever testes mais expressivos:
 * expect(button).toBeInTheDocument();
 * expect(element).toHaveClass('active');
 */
import '@testing-library/jest-dom';

/**
 * CONFIGURAÇÕES ADICIONAIS PARA TESTES
 * 
 * Mocks de APIs do navegador que não existem no ambiente jsdom
 * mas são necessárias para testar componentes React modernos.
 */

/**
 * Mock para window.matchMedia
 * 
 * A API matchMedia permite detectar media queries CSS no JavaScript.
 * Como jsdom não implementa esta API nativamente, criamos um mock.
 * 
 * Casos de uso comuns:
 * - Componentes responsivos que se adaptam ao tamanho da tela
 * - Detecção de modo escuro/claro (prefers-color-scheme)
 * - Hooks que reagem a mudanças de viewport
 * 
 * Exemplo de uso real:
 * const isMobile = window.matchMedia('(max-width: 768px)').matches;
 */
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: jest.fn().mockImplementation(query => ({
    /**
     * matches: Sempre retorna false por padrão
     * Em testes específicos, você pode sobrescrever:
     * window.matchMedia.mockReturnValue({ matches: true, ... })
     */
    matches: false,
    
    /**
     * media: Retorna a query original passada como parâmetro
     * Útil para debug e verificação nos testes
     */
    media: query,
    
    /**
     * onchange: Handler para mudanças (não usado no mock)
     */
    onchange: null,
    
    /**
     * Métodos legacy (deprecated) - mantidos para compatibilidade
     * addListener/removeListener: APIs antigas do matchMedia
     */
    addListener: jest.fn(), // Deprecated
    removeListener: jest.fn(), // Deprecated
    
    /**
     * Métodos modernos de eventos
     * addEventListener/removeEventListener: APIs atuais
     */
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
    dispatchEvent: jest.fn(),
  })),
});

/**
 * Mock para IntersectionObserver - VERSÃO CORRIGIDA
 * 
 * IntersectionObserver é uma API moderna para detectar quando elementos
 * entram ou saem da viewport, muito usada para:
 * - Lazy loading de imagens
 * - Animações triggered por scroll
 * - Infinite scrolling
 * - Tracking de visibilidade para analytics
 * 
 * Como jsdom não implementa esta API, fornecemos um mock básico.
 */

/**
 * Primeira implementação: Definição direta no global
 * 
 * Define a classe IntersectionObserver no escopo global.
 * Implementação mínima com métodos vazios para evitar erros.
 */
(global as any).IntersectionObserver = class IntersectionObserver {
  constructor() {}
  disconnect() {}
  observe() {}
  unobserve() {}
};

/**
 * Segunda implementação: Definição via Object.defineProperty no window
 * 
 * Configuração mais específica para window.IntersectionObserver
 * com propriedades writable e configurable para maior flexibilidade.
 * 
 * Permite sobrescrever o mock em testes específicos se necessário.
 */
Object.defineProperty(window, 'IntersectionObserver', {
  writable: true,
  configurable: true,
  value: class IntersectionObserver {
    constructor() {}
    disconnect() {}
    observe() {}
    unobserve() {}
  },
});

/**
 * Terceira implementação: Definição via Object.defineProperty no global
 * 
 * Garante compatibilidade máxima definindo tanto em window quanto global.
 * Algumas bibliotecas podem acessar via global em vez de window.
 * 
 * Nota: Esta tripla definição é uma abordagem defensiva para garantir
 * que todos os casos de uso sejam cobertos, embora possa parecer redundante.
 */
Object.defineProperty(global, 'IntersectionObserver', {
  writable: true,
  configurable: true,
  value: class IntersectionObserver {
    constructor() {}
    disconnect() {}
    observe() {}
    unobserve() {}
  },
});

/**
 * COMO CUSTOMIZAR ESTES MOCKS EM TESTES ESPECÍFICOS:
 * 
 * 1. Mock matchMedia para mobile:
 * beforeEach(() => {
 *   window.matchMedia = jest.fn().mockImplementation(query => ({
 *     matches: query === '(max-width: 768px)',
 *     media: query,
 *     // ... outros métodos
 *   }));
 * });
 * 
 * 2. Mock IntersectionObserver com callback:
 * const mockIntersectionObserver = jest.fn();
 * mockIntersectionObserver.mockReturnValue({
 *   observe: () => null,
 *   unobserve: () => null,
 *   disconnect: () => null
 * });
 * window.IntersectionObserver = mockIntersectionObserver;
 * 
 * 3. Simular entrada na viewport:
 * const mockObserve = jest.fn();
 * global.IntersectionObserver = jest.fn().mockImplementation((callback) => ({
 *   observe: mockObserve,
 *   unobserve: jest.fn(),
 *   disconnect: jest.fn(),
 * }));
 */