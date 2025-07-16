// src/main.tsx
// Este arquivo é o ponto de entrada da aplicação React.
// Ele renderiza o componente principal `App` dentro do elemento com id `root`
// e envolve a aplicação com o `ThemeProvider` para gerenciar o tema (claro/escuro).

import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.tsx';
import './index.css';
import { ThemeProvider } from './context/ThemeContext.tsx'; // ← ajuste conforme o path

ReactDOM.createRoot(document.getElementById('root')!).render(
  React.createElement(React.StrictMode, null,
    React.createElement(ThemeProvider, null,
      React.createElement(App)
    )
  )
);