// src// src/App.tsx
// src/App.tsx

// src/components/layout/UnifiedLayout.tsx
// Layout principal unificado que consolida as funcionalidades dos layouts existentes
// Combina SideBar, TopBar e área de conteúdo principal em uma estrutura coesa
// Suporta tema escuro/claro, responsividade e diferentes tipos de conteúdo

// types/App.tsx
// src/App.tsx
import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

import { AppProvider } from './context/AppContext';
import { ChatProvider } from './context/ChatContext';
import { ProgressProvider } from './context/ProgressContext';

import UnifiedLayout from './components/layout/UnifiedLayout';

import Home from './pages/Home';
import TextPage from './pages/TextPage';
import VoicePage from './pages/VoicePage';
import EquationPage from './pages/EquationPage';
import ImagePage from './pages/ImagePage';
import DocsPage from './pages/DocsPage';
import SettingsPanel from './components/layout/SettingsPanel';
import DashboardPage from './pages/DashBoard';
import HistoricoPage from './pages/HistoricoPage';
import CompetencyChartPage from './pages/CompetencyChartPage';
import StudentTablePage from './pages/StudentTablePage';
import LearningPathGraph from './components/progress/LearningPathGraph';
import UsuariosPage from './pages/UsuariosPage'; // ✅ Certifique-se de que este arquivo exista

import SwaggerDocsPage from './pages/SwaggerDocsPage';

export default function App() {
  return (
    <BrowserRouter>
      <AppProvider>
        <ChatProvider>
          <ProgressProvider>
            <Routes>

              {/* Home/Chat */}
              <Route
                path="/"
                element={
                  <UnifiedLayout
                    pageTitle="VIBE LEARNING STUDIO"
                    showChatBar={true}
                    showTutorButtons={true}
                  >
                    <Home />
                  </UnifiedLayout>
                }
              />

              <Route
                path="/chat"
                element={
                  <UnifiedLayout
                    pageTitle="Chat IA"
                    showChatBar={true}
                    showTutorButtons={true}
                  >
                    <Home />
                  </UnifiedLayout>
                }
              />

              {/* Tutorias */}
              <Route
                path="/text"
                element={
                  <UnifiedLayout pageTitle="Tutoria por Texto" showChatBar={true}>
                    <TextPage />
                  </UnifiedLayout>
                }
              />

              <Route
                path="/voice"
                element={
                  <UnifiedLayout pageTitle="Tutoria por Voz" showChatBar={true}>
                    <VoicePage />
                  </UnifiedLayout>
                }
              />

              <Route
                path="/equation"
                element={
                  <UnifiedLayout pageTitle="Tutoria de Equações" showChatBar={true}>
                    <EquationPage />
                  </UnifiedLayout>
                }
              />

              <Route
                path="/image"
                element={
                  <UnifiedLayout pageTitle="Tutoria por Imagem" showChatBar={true}>
                    <ImagePage />
                  </UnifiedLayout>
                }
              />

              {/* Documentos */}
              <Route path="/docs" element={<DocsPage />} />

              {/* API - Usuários */}
              <Route
                path="/usuarios"
                element={
                  <UnifiedLayout pageTitle="Usuários" showChatBar={false} showTutorButtons={false}>
                    <UsuariosPage />
                  </UnifiedLayout>
                }
              />

              {/* Ajustes */}
              <Route
                path="/ajustes"
                element={
                  <UnifiedLayout pageTitle="Ajustes" showChatBar={false} showTutorButtons={false}>
                    <SettingsPanel />
                  </UnifiedLayout>
                }
              />

              {/* Dashboard */}
              <Route
                path="/dashboard"
                element={
                  <UnifiedLayout pageTitle="Painel de Desempenho" showChatBar={false} showTutorButtons={false}>
                    <DashboardPage />
                  </UnifiedLayout>
                }
              />

              {/* Progresso */}
              <Route
                path="/progresso"
                element={
                  <UnifiedLayout pageTitle="Trajetória de Aprendizagem" showChatBar={false} showTutorButtons={false}>
                    <LearningPathGraph data={[
                      { date: '2025-07-01', text: 3, voice: 1, image: 2, equation: 0 },
                      { date: '2025-07-02', text: 5, voice: 0, image: 1, equation: 1 },
                      { date: '2025-07-03', text: 2, voice: 3, image: 0, equation: 2 },
                      { date: '2025-07-04', text: 4, voice: 1, image: 3, equation: 1 },
                    ]} />
                  </UnifiedLayout>
                }
              />
<Route
  path="/api-docs"
  element={
    <UnifiedLayout pageTitle="Documentação da API">
      <SwaggerDocsPage />
    </UnifiedLayout>
  }
/>
              {/* Histórico com rotas aninhadas */}
              <Route
                path="/historico"
                element={
                  <UnifiedLayout
                    pageTitle="Histórico de Desempenho"
                    showChatBar={false}
                    showTutorButtons={false}
                  >
                    <HistoricoPage />
                  </UnifiedLayout>
                }
              >
                <Route index element={<CompetencyChartPage />} />
                <Route path="competencias" element={<CompetencyChartPage />} />
                <Route path="estudantes" element={<StudentTablePage />} />
              </Route>

            </Routes>
          </ProgressProvider>
        </ChatProvider>
      </AppProvider>
    </BrowserRouter>
  );
}



// EXTENSÕES FUTURAS:
// - Sistema de breadcrumbs dinâmico
// - Menu dropdown para avatar com perfil/logout
// - Notificações em tempo real
// - Pesquisa global integrada
// - Suporte a múltiplos idiomas
// - Sistema de ajuda contextual
// - Atalhos de teclado
// - Modo de alto contraste
// - Layout adaptativo para tablets
// - Sistema de favoritos/bookmarks

//EXTENSÕES:
// - Adicionar suporte a autenticação de usuário com rotas protegidas.
// - Implementar um sistema de notificações para alertas e mensagens do sistema.
// - Adicionar uma página de perfil do usuário com configurações personalizáveis.
// - Implementar um sistema de feedback para usuários reportarem bugs ou sugerirem melhorias.
// - Adicionar suporte a temas personalizados com base nas preferências do usuário.
// - Implementar um sistema de histórico de navegação para fácil retorno às páginas visitadas.
// - Adicionar uma página de ajuda com FAQs e tutoriais para novos usuários.
// - Implementar um sistema de análise de uso para coletar dados sobre como os usuários interagem com a aplicação.
// - Adicionar suporte a múltiplos idiomas com tradução dinâmica de conteúdo.
// - Implementar um sistema de comentários para usuários discutirem conteúdos específicos.
// - Adicionar uma página de recursos com links úteis e documentação externa.
// - Implementar um sistema de pesquisa global para encontrar conteúdos e páginas rapidamente.
// - Adicionar uma página de contato para suporte ao usuário.
