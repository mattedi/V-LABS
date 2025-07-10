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

# 📘 Vibe Learning – Plataforma Educacional Multimodal com IA

**Vibe Learning** é uma aplicação educacional interativa desenvolvida em **React + TypeScript**, voltada para o ensino adaptativo por meio de tutoria orientada à pergunta. O sistema integra **modelos de IA**, **módulos colaborativos**, **rastreamento de progresso**, e um conjunto completo de interfaces para tutoria textual, visual, por voz e por equações.

---

## 🧱 Estrutura do Projeto

```bash
V-LABS/
│
├── src/
│   ├── components/              # Componentes UI organizados por domínio funcional
│   │   ├── ai/                  # Painéis e retornos do módulo de IA
│   │   ├── chat/                # ChatBar, mensagens, lista
│   │   ├── collaboration/       # Painel de colaboração em tempo real
│   │   ├── common/              # Componentes reutilizáveis (Avatar, Button, etc.)
│   │   ├── layout/              # Header, Sidebar, Menu, Layout principal
│   │   └── tutoring/            # Botões e ações de tutoria
│   │
│   ├── context/                 # Contextos globais da aplicação (Theme, Auth, Progress, etc.)
│   ├── hooks/                   # Hooks personalizados
│   ├── pages/                   # Páginas principais (rotas)
│   ├── services/                # Acesso à API e funções de backend
│   ├── setupTest/              # Configuração e arquivos de teste unitário com Jest
│   ├── types/                  # Tipos TypeScript globais
│   ├── App.tsx                 # Componente raiz da aplicação
│   ├── main.tsx                # Ponto de entrada com ReactDOM
│   └── index.css               # Estilos globais
│
├── public/
│   └── index.html              # HTML base
│
├── tailwind.config.js         # Configuração TailwindCSS
├── vite.config.js             # Configuração do Vite (build tool)
├── postcss.config.cjs         # Configuração PostCSS
├── jest.config.js             # Configuração Jest para testes
├── package.json               # Dependências e scripts
└── README.md                  # Documentação (este arquivo)


| Tecnologia                 | Função Principal                                    |
| -------------------------- | --------------------------------------------------- |
| **React + TypeScript**     | Framework principal com tipagem estática            |
| **Vite**                   | Bundler e dev server rápido                         |
| **TailwindCSS**            | Estilização utilitária responsiva                   |
| **Context API**            | Gerenciamento de estado local/global                |
| **Jest + Testing Library** | Testes unitários dos componentes                    |
| **Axios/Fetch**            | Comunicação com API (camada `services/`)            |
| **IA Backend**             | Módulo de inferência via APIs externas (modelo LLM) |
| **PostgreSQL** (esperado)  | Persistência dos dados de usuários e interações     |


🧠 Funcionalidades Principais
🟢 Tutoria Multimodal
Tutoria via texto, voz, imagem e equações.

Componente: TutorButtons.tsx

🧠 Módulo de IA
Comunicação com modelo inteligente para gerar feedback e respostas.

Componente: AIFeedbackPanel.tsx

💬 Chat Integrado
Comunicação dinâmica entre usuário e IA com histórico.

Componentes: ChatBar.tsx, MessageList.tsx

🧩 Progresso e Avaliação
Rastreamento de domínio e nível de domínio por contexto.

Contexto: ProgressContext.tsx

🧾 Autenticação
Simulação de login, autenticação e roles de acesso.

Contexto: AuthContext.tsx

🛠️ Testes
Testes unitários com Jest (Button.test.tsx)

Configuração em jest.config.js e setupTests.ts

🚀 Como Executar Localmente
Pré-requisitos
Node.js >= 18.x

npm >= 9.x

🔷 1. Node.js como Ambiente de Desenvolvimento
No contexto do frontend em React, o Node.js serve como plataforma de suporte para:

Função	Ferramentas associadas
Gerenciamento de pacotes	npm, package.json, package-lock.json
Transpilação e bundling (dev/build)	vite (executado via Node)
Processamento de CSS	postcss, tailwind (Node executa a toolchain)
Testes automatizados	jest (executado em ambiente Node)
Rodar scripts utilitários	Comandos em scripts no package.json

✅ Resumo: no frontend, o Node.js não executa o React, mas fornece o ambiente de ferramentas necessário para transpilar, empacotar, servir e testar sua aplicação.

🔷 2. Node.js como Backend (Orquestração / Middleware)
Na arquitetura exibida (com a camada de orquestração e a camada de segurança/middleware), o Node.js pode ser usado também como servidor backend, em um ou mais dos seguintes papéis:

📌 a) API REST
Criar e expor endpoints via frameworks como:

Express.js

NestJS

Comunicação entre Interface ⇄ Orquestração ⇄ Módulo IA

📌 b) Middleware de Segurança
Verificação de tokens JWT

Proteção de rotas

Gestão de sessões

Cross-Origin Resource Sharing (CORS)

📌 c) Gateway para IA
Receber requisição do frontend, encaminhar ao modelo (ex.: FastAPI, OpenAI, Hugging Face), e retornar resposta.

📌 d) Camada de Integração com o Banco de Dados
Intermediar acesso ao PostgreSQL, MongoDB etc. via ORMs como Prisma, Sequelize ou TypeORM.

