// src/main.tsx
// Este arquivo é o ponto de entrada da aplicação React.
// Ele renderiza o componente principal `App` dentro do elemento com id `root`
// e envolve a aplicação com o `ThemeProvider` para gerenciar o tema (claro/escuro).

// src/main.tsx

// src/main.tsx

import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.tsx';
import './index.css';

import { ThemeProvider } from './context/ThemeContext.tsx';
import { AuthProvider } from './context/AuthContext.tsx';
import { BrowserRouter } from 'react-router-dom'; // ✅ necessário para navegação

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BrowserRouter>
      <ThemeProvider>
        <AuthProvider>
          <App />
        </AuthProvider>
      </ThemeProvider>
    </BrowserRouter>
  </React.StrictMode>
);

