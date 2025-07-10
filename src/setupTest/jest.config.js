// jest.config.js

/**
 * Configuração do Jest para testes da aplicação VL Studio
  * Este arquivo define todas as configurações necessárias para executar
 * testes unitários e de integração em um projeto React com TypeScript.
 * Funcionalidades configuradas:
 * - Ambiente de teste simulando browser (jsdom)
 * - Suporte completo a TypeScript e JSX
 * - Mapeamento de arquivos CSS/SCSS para testes
 * - Configuração de cobertura de código
 * - Padrões de busca por arquivos de teste
 * - Transformações para diferentes tipos de arquivo
 * Framework: Jest v29+ (compatível com React Testing Library)
 * Linguagens: TypeScript, JavaScript, JSX, TSX
 * 
 * @see https://jestjs.io/docs/configuration
 */

module.exports = {
  /**
   * Ambiente de execução dos testes
   * 
   * 'jsdom': Simula um ambiente de navegador no Node.js
   * - Fornece APIs do DOM (document, window, etc.)
   * - Necessário para testar componentes React
   * - Permite testar interações com elementos HTML
   * 
   * Alternativa: 'node' (para testes de backend/utils apenas)
   */
  testEnvironment: 'jsdom',

  /**
   * Arquivos de configuração executados após configuração do ambiente
   * 
   * setupTests.ts: Arquivo de configuração global dos testes
   * - Configurações do Testing Library
   * - Mocks globais
   * - Extensões de matchers personalizados
   * - Configurações de limpeza entre testes
   */
  setupFilesAfterEnv: ['<rootDir>/src/setupTests.ts'],

  /**
   * Mapeamento de módulos para mocks
   * 
   * Arquivos CSS/SCSS são substituídos por 'identity-obj-proxy':
   * - Permite importar estilos sem quebrar os testes
   * - Retorna o nome da classe CSS como string
   * - Evita erros de "módulo não encontrado" para estilos
   * 
   * Exemplo: import styles from './Button.module.css'
   * → styles.primary retorna "primary" nos testes
   */
  moduleNameMapping: {
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy',
  },

  /**
   * Configurações de transformação de arquivos
   * 
   * Define como diferentes tipos de arquivo são processados antes dos testes:
   */
  transform: {
    /**
     * Arquivos TypeScript (.ts, .tsx)
     * 
     * 'ts-jest': Transpila TypeScript para JavaScript
     * - Suporte completo a tipos TypeScript
     * - Transformação de JSX/TSX
     * - Verificação de tipos durante os testes
     */
    '^.+\\.(ts|tsx)$': 'ts-jest',
    
    /**
     * Arquivos JavaScript (.js, .jsx)
     * 
     * 'babel-jest': Transpila JavaScript moderno e JSX
     * - Suporte a ES6+ syntax
     * - Transformação de JSX para JavaScript
     * - Compatibilidade com diferentes versões do Node.js
     */
    '^.+\\.(js|jsx)$': 'babel-jest',
  },

  /**
   * Extensões de arquivo reconhecidas pelo Jest
   * 
   * Ordem de prioridade para resolução de módulos:
   * 1. .ts - TypeScript
   * 2. .tsx - TypeScript com JSX  
   * 3. .js - JavaScript
   * 4. .jsx - JavaScript com JSX
   * 5. .json - Arquivos de dados JSON
   * 6. .node - Módulos nativos do Node.js
   */
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json', 'node'],

  /**
   * Padrões para localizar arquivos de teste
   * 
   * O Jest procurará por testes em dois locais:
   */
  testMatch: [
    /**
     * Padrão 1: Pasta __tests__ 
     * Exemplo: src/components/__tests__/Button.test.ts
     * - Organização tradicional com pasta dedicada
     * - Facilita separação entre código e testes
     */
    '<rootDir>/src/**/__tests__/**/*.(ts|tsx|js)',
    
    /**
     * Padrão 2: Arquivos .test.* ou .spec.* ao lado do código
     * Exemplo: src/components/Button.test.ts
     * - Testes próximos ao código testado
     * - Convenção moderna e prática
     * - Facilita manutenção e descoberta
     */
    '<rootDir>/src/**/?(*.)(spec|test).(ts|tsx|js)',
  ],

  /**
   * Configuração de cobertura de código (code coverage)
   * 
   * Define quais arquivos são incluídos no relatório de cobertura:
   */
  collectCoverageFrom: [
    /**
     * Incluir: Todos os arquivos TypeScript na pasta src
     * - Componentes, hooks, utils, pages, etc.
     * - Apenas arquivos .ts e .tsx
     */
    'src/**/*.(ts|tsx)',
    
    /**
     * Excluir: Arquivos de definição de tipos
     * - Arquivos .d.ts não contêm lógica testável
     * - São apenas definições de tipos TypeScript
     */
    '!src/**/*.d.ts',
    
    /**
     * Excluir: Arquivo principal da aplicação
     * - index.tsx geralmente só faz bootstrap da app
     * - Pouca lógica testável, muito específico do React
     */
    '!src/index.tsx',
    
    /**
     * Excluir: Service Worker
     * - serviceWorker.ts contém código específico do browser
     * - Difícil de testar em ambiente jsdom
     * - Funcionalidade independente da lógica da aplicação
     */
    '!src/serviceWorker.ts',
  ],
};

//EXTENSÕES
// Extensão para calcular o nível de maestria
