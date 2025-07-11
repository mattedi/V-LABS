// src/pages/DocsPage.tsx
// src/pages/DocsPage.tsx
// Documentação do V-LABS
// Esta página fornece uma visão geral do projeto V-LABS, suas funcionalidades e 
// tecnologias utilizadas.
// A documentação é construída com React e Tailwind, e inclui suporte a IA multimodal.
// src/pages/DocsPage.tsx

// src/pages/DocsPage.tsx
import React from 'react';

export default function DocsPage() {
  return (
    <div className="max-w-4xl mx-auto p-8 text-gray-900 dark:text-gray-100">
      <h1 className="text-3xl font-bold mb-4">📘 Documentação do V-LABS</h1>

      <p className="mb-6">
        Bem-vindo à documentação oficial do V-LABS. Esta interface foi construída com React, TailwindCSS, Vite e suporte a IA multimodal.
      </p>

      {/* 🔗 Link para download da documentação PDF */}
      <div className="mb-8">
        <a
          href="/Vibe_Learning_Studio_doc_1.pdf"
          target="_blank"
          rel="noopener noreferrer"
          download
          className="inline-block bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded transition"
        >
          📄 Baixar Documentação Expandida (PDF)
        </a>
      </div>

      <h2 className="text-2xl font-semibold mt-6 mb-2">🎯 Objetivo</h2>
      <p className="mb-4">
        Fornecer suporte interativo, adaptável e inteligente ao processo de aprendizagem multimodal por meio de texto, voz, imagem e equações.
      </p>

      <h2 className="text-2xl font-semibold mt-6 mb-2">🚀 Funcionalidades</h2>
      <ul className="list-disc list-inside mb-4 space-y-1">
        <li>Entradas multimodais: texto, voz, imagem e equações</li>
        <li>Modo escuro/claro com persistência local</li>
        <li>Configurações de idioma, tamanho da fonte e avatar</li>
        <li>Integração com IA baseada em LLM</li>
        <li>Layout responsivo com navegação unificada</li>
      </ul>

      <h2 className="text-2xl font-semibold mt-6 mb-2">🧱 Stack Tecnológico</h2>
      <ul className="list-disc list-inside mb-4 space-y-1">
        <li>React + Vite para front-end modular e rápido</li>
        <li>TailwindCSS para estilização utilitária</li>
        <li>Context API com LocalStorage para persistência</li>
        <li>TypeScript para segurança e escalabilidade</li>
      </ul>
    </div>
  );
}


//EXTENSÕES:
// - Adicionar links para tutoriais ou vídeos explicativos sobre o uso do V-LABS.
// - Implementar uma seção de perguntas frequentes (FAQ) para ajudar novos usuários.
// - Incluir exemplos de código para cada funcionalidade principal.
// - Adicionar uma seção de "Começando" com instruções passo a passo para novos
//   usuários.
// - Implementar um sistema de feedback onde os usuários podem sugerir melhorias na documentação.
// - Adicionar uma seção de "Contribuindo" com diretrizes para desenvolvedores que
//   desejam contribuir com o projeto.
// - Incluir uma seção de "Roadmap" para mostrar futuras funcionalidades planejadas.
// - Implementar um sistema de busca para facilitar a navegação na documentação.
// - Adicionar uma seção de "Recursos" com links para artigos, livros e cursos relacionados ao V-LABS.
