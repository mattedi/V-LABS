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

# 🧩 Quadro das Tecnologias por Camada — Vibe Learning Studio

## 1. Interface (Frontend)

| Tecnologia            | Função Principal                                                      |
|------------------------|------------------------------------------------------------------------|
| React (v18), Vite, TypeScript | Estrutura da interface SPA com componentes funcionais              |
| TailwindCSS, PostCSS  | Estilização utilitária e responsiva                                    |
| Axios                 | Comunicação HTTP com a API                                              |
| React Router DOM      | Roteamento de páginas                                                   |
| Context API, Hooks    | Gerenciamento de estado local                                           |
| Jest, React Testing Library | Testes unitários de componentes                                      |
| Vite Plugin Tailwind, Lucide | Extensões visuais e ícones                                          |

---

## 2. Aplicação (Backend)

| Tecnologia         | Função Principal                                                        |
|--------------------|--------------------------------------------------------------------------|
| FastAPI            | Framework principal da API RESTful                                      |
| Pydantic           | Validação e modelagem de dados (schemas)                                |
| Uvicorn            | Servidor ASGI para execução da API                                      |
| Python 3.11+       | Linguagem base do backend                                                |
| dotenv             | Variáveis de ambiente                                                    |
| CORS Middleware, APIRouter | Configuração de segurança e rotas modulares                          |

---

## 3. Persistência (Banco de Dados)

| Tecnologia         | Função Principal                                                        |
|--------------------|--------------------------------------------------------------------------|
| MongoDB Atlas      | Armazenamento de dados estruturados em coleções                         |
| PyMongo            | Cliente MongoDB para Python                                              |
| Qdrant Cloud/Server| Armazenamento vetorial para embeddings semânticos                        |
| qdrant-client      | Cliente Python para Qdrant                                               |

---

## 4. Dados Semânticos / IA

| Tecnologia                  | Função Principal                                                  |
|-----------------------------|--------------------------------------------------------------------|
| OpenAI Embeddings ou SentenceTransformers | Geração de embeddings semânticos (texto, imagem, equação)  |
| LangChain (opcional)        | Orquestração e pipelines de IA generativa                         |
| scikit-learn, numpy (opcional) | Cálculo de distâncias, análises vetoriais                         |

---

## 5. Documentação / Observabilidade

| Tecnologia           | Função Principal                                                       |
|----------------------|------------------------------------------------------------------------|
| Swagger UI (FastAPI) | Interface de documentação interativa da API                           |
| ReDoc                | Documentação OpenAPI alternativa                                       |
| SwaggerDocsPage.tsx  | Integração da documentação com o frontend                             |
| logging, logs_interacao | Registro interno de ações dos usuários                                |
"""

# 📘 Vibe Learning – Plataforma Educacional Multimodal com IA

**Vibe Learning** é uma aplicação educacional interativa desenvolvida em **React + TypeScript**, voltada para o ensino adaptativo por meio de tutoria orientada à pergunta. O sistema integra **modelos de IA**, **módulos colaborativos**, **rastreamento de progresso**, e um conjunto completo de interfaces para tutoria textual, visual, por voz e por equações.

---

## 🧱 Estrutura do Projeto

Vibe-Learning-Studio/
│
├── backend_bd/
│   ├── backend/
│   │   ├── run.py                        # Arquivo de execução principal da API
│   │   ├── .env                          # Variáveis de ambiente
│   │   ├── requirements.txt              # Dependências do backend
│   │   ├── bd_mongodb_v1.py              # Script de teste MongoDB
│   │   ├── bd_qdrant_v1.py               # Script de teste Qdrant
│   │   ├── mongodr_qdrant_v1.py          # Integração MongoDB + Qdrant
│   │   └── app/
│   │       ├── main.py                   # Instância FastAPI
│   │       ├── database/
│   │       │   ├── mongo.py              # Conexão MongoDB
│   │       │   └── qdrant.py             # Conexão Qdrant
│   │       ├── models/                   # Modelos (opcional)
│   │       ├── routers/
│   │       │   ├── usuarios.py           # Rotas de usuários
│   │       │   ├── perguntas.py          # Rotas de perguntas
│   │       ├── schemas/
│   │       │   └── main.py               # Schemas Pydantic
│   │       └── __pycache__/              # Cache Python
│
├── frontend/
│   └── src/
│       ├── components/
│       │   ├── ai/
│       │   │   └── AIFeedbackPanel.tsx
│       │   ├── chat/
│       │   ├── collaboration/
│       │   ├── common/
│       │   │   ├── Avatar.tsx
│       │   │   └── Button.tsx
│       │   ├── dashboard/
│       │   ├── layout/
│       │   │   ├── Layout.tsx
│       │   │   ├── SideBar.tsx
│       │   │   ├── TopBar.tsx
│       │   │   ├── UnifiedLayout.tsx
│       │   │   └── MobileMenu.tsx
│       │   └── multimodal/
│       │       ├── TextInput.tsx
│       │       ├── VoiceInput.tsx
│       │       ├── ImageInput.tsx
│       │       ├── EquationInput.tsx
│       │       └── QuestionInputPanel.tsx
│       ├── config/
│       │   └── layoutConfig.ts
│       ├── context/
│       │   ├── AppContext.tsx
│       │   ├── AuthContext.tsx
│       │   └── ChatContext.tsx
│       ├── hooks/
│       │   ├── useAIAnalysis.ts
│       │   └── useAIFeedback.ts
│       ├── pages/
│       │   ├── Home.tsx
│       │   ├── TextPage.tsx
│       │   ├── VoicePage.tsx
│       │   ├── ImagePage.tsx
│       │   ├── EquationPage.tsx
│       │   ├── UsuariosPage.tsx
│       │   ├── DashBoard.tsx
│       │   ├── StudentTablePage.tsx
│       │   ├── CompetencyChartPage.tsx
│       │   ├── HistoricoPage.tsx
│       │   └── SwaggerDocsPage.tsx
│       ├── progress/
│       │   └── LearningPathGraph.tsx
│       ├── tutoring/
│       │   └── TutorButtons.tsx
│       ├── services/
│       │   ├── api.ts
│       │   └── progress.ts
│       ├── setupTest/
│       │   ├── Button.test.tsx
│       │   ├── jest.config.js
│       │   └── setupTests.ts
│       ├── types/
│       │   ├── App.tsx
│       │   ├── main.tsx
│       │   └── index.ts
│       ├── index.css
│       ├── index.html
│       └── Vibe_Learning_Studio_doc_1.pdf
│
├── package.json
├── package-lock.json
├── vite.config.js
├── tailwind.config.js
├── postcss.config.cjs
└── README.md
```"""

