// src// src/App.tsx
// src/App.tsx

// src/components/layout/UnifiedLayout.tsx
// Layout principal unificado que consolida as funcionalidades dos layouts existentes
// Combina SideBar, TopBar e área de conteúdo principal em uma estrutura coesa
// Suporta tema escuro/claro, responsividade e diferentes tipos de conteúdo

// types/App.tsx
// src/App.tsx
// src/App.tsx
// src/App.tsx
// src/App.tsx
import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';

import { AppProvider } from './context/AppContext';
import { AuthProvider } from './context/AuthContext'; // ← ADICIONADO
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
import UsuariosPage from './pages/UsuariosPage';
import SwaggerDocsPage from './pages/SwaggerDocsPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';

// Componente para Rotas Protegidas
import { useAuth } from './context/AuthContext';

const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-50 dark:bg-gray-900">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600 dark:text-gray-400">Carregando...</p>
        </div>
      </div>
    );
  }

  return isAuthenticated ? <>{children}</> : <Navigate to="/login" replace />;
};

export default function App() {
  return (
    <AuthProvider> {/* ← AuthProvider envolvendo toda a aplicação */}
      <AppProvider>
        <ChatProvider>
          <ProgressProvider>
            <Routes>

              {/* Página Principal - PÚBLICA (sem ProtectedRoute) */}
              <Route
                path="/"
                element={
                  <UnifiedLayout pageTitle="VIBE LEARNING STUDIO" showChatBar showTutorButtons>
                    <Home />
                  </UnifiedLayout>
                }
              />

              {/* Autenticação - Rotas Públicas */}
              <Route path="/login" element={<LoginPage />} />
              <Route path="/register" element={<RegisterPage />} />
              <Route path="/docs" element={<DocsPage />} />

              {/* Chat - PROTEGIDA */}
              <Route
                path="/chat"
                element={
                  <ProtectedRoute>
                    <UnifiedLayout pageTitle="Chat IA" showChatBar showTutorButtons>
                      <Home />
                    </UnifiedLayout>
                  </ProtectedRoute>
                }
              />

              {/* Tutorias - Rotas Protegidas */}
              <Route
                path="/text"
                element={
                  <ProtectedRoute>
                    <UnifiedLayout pageTitle="Tutoria por Texto" showChatBar>
                      <TextPage />
                    </UnifiedLayout>
                  </ProtectedRoute>
                }
              />
              <Route
                path="/voice"
                element={
                  <ProtectedRoute>
                    <UnifiedLayout pageTitle="Tutoria por Voz" showChatBar>
                      <VoicePage />
                    </UnifiedLayout>
                  </ProtectedRoute>
                }
              />
              <Route
                path="/equation"
                element={
                  <ProtectedRoute>
                    <UnifiedLayout pageTitle="Tutoria de Equações" showChatBar>
                      <EquationPage />
                    </UnifiedLayout>
                  </ProtectedRoute>
                }
              />
              <Route
                path="/image"
                element={
                  <ProtectedRoute>
                    <UnifiedLayout pageTitle="Tutoria por Imagem" showChatBar>
                      <ImagePage />
                    </UnifiedLayout>
                  </ProtectedRoute>
                }
              />

              {/* Extras - Algumas Públicas, Outras Protegidas */}
              <Route
                path="/usuarios"
                element={
                  <ProtectedRoute>
                    <UnifiedLayout pageTitle="Usuários">
                      <UsuariosPage />
                    </UnifiedLayout>
                  </ProtectedRoute>
                }
              />
              <Route
                path="/perfil"
                element={
                  <ProtectedRoute>
                    <UnifiedLayout pageTitle="Meu Perfil">
                      <div className="text-center py-8">
                        <h2 className="text-2xl font-bold mb-4">Meu Perfil</h2>
                        <p className="text-gray-600 dark:text-gray-400">Página de perfil em desenvolvimento...</p>
                      </div>
                    </UnifiedLayout>
                  </ProtectedRoute>
                }
              />
              <Route
                path="/ajustes"
                element={
                  <ProtectedRoute>
                    <UnifiedLayout pageTitle="Ajustes">
                      <SettingsPanel />
                    </UnifiedLayout>
                  </ProtectedRoute>
                }
              />
              <Route
                path="/dashboard"
                element={
                  <ProtectedRoute>
                    <UnifiedLayout pageTitle="Painel de Desempenho">
                      <DashboardPage />
                    </UnifiedLayout>
                  </ProtectedRoute>
                }
              />
              <Route
                path="/progresso"
                element={
                  <ProtectedRoute>
                    <UnifiedLayout pageTitle="Trajetória de Aprendizagem">
                      <LearningPathGraph
                        data={[
                          { date: '2025-07-01', text: 3, voice: 1, image: 2, equation: 0 },
                          { date: '2025-07-02', text: 5, voice: 0, image: 1, equation: 1 },
                          { date: '2025-07-03', text: 2, voice: 3, image: 0, equation: 2 },
                          { date: '2025-07-04', text: 4, voice: 1, image: 3, equation: 1 },
                        ]}
                      />
                    </UnifiedLayout>
                  </ProtectedRoute>
                }
              />
              <Route
                path="/api-docs"
                element={
                  <ProtectedRoute>
                    <UnifiedLayout pageTitle="Documentação da API">
                      <SwaggerDocsPage />
                    </UnifiedLayout>
                  </ProtectedRoute>
                }
              />

              {/* Histórico com rotas aninhadas - Protegidas */}
              <Route
                path="/historico"
                element={
                  <ProtectedRoute>
                    <UnifiedLayout pageTitle="Histórico de Desempenho">
                      <HistoricoPage />
                    </UnifiedLayout>
                  </ProtectedRoute>
                }
              >
                <Route index element={<CompetencyChartPage />} />
                <Route path="competencias" element={<CompetencyChartPage />} />
                <Route path="estudantes" element={<StudentTablePage />} />
              </Route>

              {/* Rota fallback */}
              <Route path="*" element={<Navigate to="/" replace />} />

            </Routes>
          </ProgressProvider>
        </ChatProvider>
      </AppProvider>
    </AuthProvider>
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
