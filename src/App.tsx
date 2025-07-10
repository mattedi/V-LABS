// src// src/App.tsx
// src/App.tsx

// src/components/layout/UnifiedLayout.tsx
// Layout principal unificado que consolida as funcionalidades dos layouts existentes
// Combina SideBar, TopBar e área de conteúdo principal em uma estrutura coesa
// Suporta tema escuro/claro, responsividade e diferentes tipos de conteúdo

// types/App.tsx

import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AppProvider } from '../src/context/AppContext';           // ✅ CORRIGIDO: ../src/ para sair de types/
import { ChatProvider } from '../src/context/ChatContext';         // ✅ CORRIGIDO: ../src/ para sair de types/
import { ProgressProvider } from '../src/context/ProgressContext'; // ✅ CORRIGIDO: ../src/ para sair de types/
import UnifiedLayout from '../src/components/layout/UnifiedLayout'; // ✅ CORRIGIDO: ../src/ para sair de types/
import Home from '../src/pages/Home';
import TextPage from '../src/pages/TextPage';
import VoicePage from '../src/pages/VoicePage';
import EquationPage from '../src/pages/EquationPage';
import ImagePage from '../src/pages/ImagePage';
import DocsPage from '../src/pages/DocsPage';
import SettingsPanel from '../src/components/layout/SettingsPanel';

export default function App() {
  return (
    <BrowserRouter>
      <AppProvider>
        <ChatProvider>
          <ProgressProvider>
              <Routes>
                {/* ✅ REFATORADO: Todas as rotas usando UnifiedLayout com títulos específicos */}
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
                  path="/text" 
                  element={
                    <UnifiedLayout 
                      pageTitle="Tutoria por Texto"
                      showChatBar={true}
                    >
                      <TextPage />
                    </UnifiedLayout>
                  } 
                />
                
                <Route 
                  path="/voice" 
                  element={
                    <UnifiedLayout 
                      pageTitle="Tutoria por Voz"
                      showChatBar={true}
                    >
                      <VoicePage />
                    </UnifiedLayout>
                  } 
                />
                
                <Route 
                  path="/equation" 
                  element={
                    <UnifiedLayout 
                      pageTitle="Tutoria de Equações"
                      showChatBar={true}
                    >
                      <EquationPage />
                    </UnifiedLayout>
                  } 
                />
                
                <Route 
                  path="/image" 
                  element={
                    <UnifiedLayout 
                      pageTitle="Tutoria por Imagem"
                      showChatBar={true}
                    >
                      <ImagePage />
                    </UnifiedLayout>
                  } 
                />

                <Route 
                  path="/docs" 
                  element={<DocsPage />} 
                />
                
                <Route 
                  path="/settings" 
                  element={
                    <UnifiedLayout 
                      pageTitle="Configurações"
                      showChatBar={false}
                      showTutorButtons={false}
                    >
                      <SettingsPanel />
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
                
                <Route 
                  path="/ajustes" 
                  element={
                    <UnifiedLayout 
                      pageTitle="Ajustes"
                      showChatBar={false}
                      showTutorButtons={false}
                    >
                      <SettingsPanel />
                    </UnifiedLayout>
                  } 
                />
                
                <Route 
                  path="/historico" 
                  element={
                    <UnifiedLayout 
                      pageTitle="Histórico de Conversas"
                      showChatBar={false}
                      showTutorButtons={false}
                    >
                      <div className="text-center py-12">
                        <h2 className="text-2xl font-semibold text-gray-600 dark:text-gray-400">
                          Histórico em desenvolvimento
                        </h2>
                        <p className="text-gray-500 dark:text-gray-500 mt-4">
                          Esta funcionalidade será implementada em breve.
                        </p>
                      </div>
                    </UnifiedLayout>
                  } 
                />
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
