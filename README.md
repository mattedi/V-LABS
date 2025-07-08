1 - ESTRUTURA 

🧭 Estrutura e Componentes da Interface
A interface do V-LABS foi projetada com foco na usabilidade, acessibilidade e modularidade, utilizando a biblioteca React com suporte a tema claro/escuro (dark mode) e estilo visual baseado em TailwindCSS.

🎯 Objetivo da Interface
A interface visa fornecer um ambiente intuitivo para estudantes e professores interagirem com diferentes modalidades de tutoria (Texto, Voz, Equações e Imagens), integrando ferramentas de IA e visualização em tempo real. A experiência é adaptativa, responsiva e otimizada para uso em navegadores modernos.

🧩 Componentes e Organização
A estrutura segue uma organização modular dividida por responsabilidades:

📁 components/
Contém os blocos reutilizáveis da interface:

layout/

Layout.tsx: Estrutura geral da página com Sidebar, Header e <main>.

Header.tsx: Contém o logotipo, título “Vibe Learning Studio”, botão de documentação, ThemeToggle e Avatar.

Sidebar.tsx: Navegação lateral com atalhos para as seções: Chat, Ajustes, Histórico.

common/

Button.tsx: Componente genérico para botões, com suporte a variantes e tamanhos.

Avatar.tsx: Ícone de usuário com indicador de status (online), adaptável por tipo de usuário (student, tutor, teacher).

tutoring/

TutorButtons.tsx: Exibe os quatro modos de tutoria (Texto, Voz, Equação, Imagem), cada um com ícone e navegação.

📁 pages/
Cada página representa uma seção funcional da aplicação:

TextPage.tsx

VoicePage.tsx

EquationPage.tsx

ImagePage.tsx

Essas páginas são carregadas dinamicamente via react-router.

📁 context/
Gerencia estados globais com React Context API:

AppContext.tsx: Controle do modo escuro, autenticação e estado geral.

ThemeContext.tsx: Ativa e alterna o tema dark/light.

ChatContext.tsx, ProgressContext.tsx: Estados específicos de tutoria e progresso.

📁 hooks/
Custom Hooks que encapsulam lógicas reutilizáveis:

useLocalStorage.ts

useAIAnalysis.ts

useAIFeedback.ts

📁 services/
api.ts: Cliente de API (fetch/axios).

progress.ts: Endpoints relacionados ao progresso do usuário.

🎨 Estilo Visual
Utiliza TailwindCSS com configurações customizadas em tailwind.config.js.

Modo escuro habilitado via classe dark no body (controlado por AppContext e ThemeToggle).

Ícones provenientes da biblioteca react-icons/fi.

⚙️ Integração
Roteamento feito com react-router-dom.

Análise de progresso com IA (via hooks).

A interface está acoplada a um backend via serviços REST e pode ser estendida com sockets/WebSocket.

💡 Interação do Usuário
A navegação lateral (Sidebar) é fixa.

O cabeçalho flutua no topo da página com interações utilitárias.

A escolha de tutoria (cards coloridos com ícones) adapta-se ao tema e guia o usuário de forma visual.


## 🚀 Tecnologias Utilizadas

O projeto **V-LABS** foi desenvolvido com um stack moderno e modular, voltado ao desenvolvimento frontend escalável, com suporte a contexto de Inteligência Artificial e interatividade multimodal. A seguir, detalham-se as principais tecnologias e suas respectivas finalidades:

| **Categoria**           | **Tecnologia / Biblioteca**                    | **Finalidade**                                                               |
|-------------------------|------------------------------------------------|------------------------------------------------------------------------------|
| **Linguagem**           | TypeScript                                     | Tipagem estática e segurança no desenvolvimento em React                    |
| **Biblioteca base**     | React                                          | Estrutura declarativa da interface                                          |
| **Empacotador**         | Vite                                           | Build tool leve, rápido e compatível com ESModules                          |
| **Estilização**         | TailwindCSS                                    | Framework utilitário para design responsivo, dark mode e tipografia         |
| **Ícones**              | `react-icons/fi`                               | Ícones vetoriais para componentes visuais                                   |
| **Estado Global**       | React Context API                              | Gerenciamento de temas, usuário, progresso e dados compartilhados           |
| **Roteamento**          | `react-router-dom`                             | Navegação entre as páginas de tutoria                                       |
| **Animações e Efeitos** | TailwindCSS Transitions                        | Animações de hover, transições e responsividade                             |
| **Testes**              | Jest + React Testing Library *(setup inicial)* | Infraestrutura de testes unitários e de componentes                         |
| **Estilo de Código**    | ESLint + Prettier                              | Padronização de código e formatação automática                              |
| **Persistência Local**  | `localStorage` via custom hooks                | Armazenamento leve de preferências do usuário (ex: tema escuro)             |

