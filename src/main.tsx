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
