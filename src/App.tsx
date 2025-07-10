// src// src/App.tsx
// src/App.tsx

import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AppProvider } from './context/AppContext';
import { ChatProvider } from './context/ChatContext';
import { ProgressProvider } from './context/ProgressContext';
import Layout from './components/layout/Layout';
import Home from './pages/Home';
import TextPage from './pages/TextPage';
import VoicePage from './pages/VoicePage';
import EquationPage from './pages/EquationPage';
import ImagePage from './pages/ImagePage';
import DocsPage from './pages/DocsPage';

export default function App() {
  return (
    <BrowserRouter>
      <AppProvider>
        <ChatProvider>
          <ProgressProvider>
            <Routes>
              <Route path="/" element={<Layout><Home /></Layout>} />
              <Route path="/text" element={<Layout><TextPage /></Layout>} />
              <Route path="/voice" element={<Layout><VoicePage /></Layout>} />
              <Route path="/equation" element={<Layout><EquationPage /></Layout>} />
              <Route path="/image" element={<Layout><ImagePage /></Layout>} />
               <Route path="/docs" element={<DocsPage />} />
            </Routes>
          </ProgressProvider>
        </ChatProvider>
      </AppProvider>
    </BrowserRouter>
  );
}

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
