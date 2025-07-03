// src/App.tsx
import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AppProvider } from './context/AppContext';
import { ChatProvider } from './context/ChatContext';
import Layout from './components/layout/Layout';
import Home from './pages/Home';
import TextPage from './pages/TextPage';
import VoicePage from './pages/VoicePage';
import EquationPage from './pages/EquationPage';
import ImagePage from './pages/ImagePage';

export default function App() {
  return (
    <BrowserRouter>
      <AppProvider>
        <ChatProvider>
          <Routes>
            <Route path="/" element={<Layout><Home /></Layout>} />
            <Route path="/text" element={<Layout><TextPage /></Layout>} />
            <Route path="/voice" element={<Layout><VoicePage /></Layout>} />
            <Route path="/equation" element={<Layout><EquationPage /></Layout>} />
            <Route path="/image" element={<Layout><ImagePage /></Layout>} />
          </Routes>
        </ChatProvider>
      </AppProvider>
    </BrowserRouter>
  );
}