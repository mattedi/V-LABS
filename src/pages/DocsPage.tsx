// src/pages/DocsPage.tsx

import React from 'react';

export default function DocsPage() {
  return (
    <div className="max-w-4xl mx-auto p-8 text-gray-900 dark:text-gray-100">
      <h1 className="text-3xl font-bold mb-4">📘 Documentação do V-LABS</h1>
      <p className="mb-4">
        Bem-vindo à documentação oficial do V-LABS. Esta interface foi construída com React, Tailwind, Vite e suporte a IA multimodal.
      </p>

      <h2 className="text-2xl font-semibold mt-6 mb-2">🎯 Objetivo</h2>
      <p className="mb-4">
        Fornecer suporte interativo para aprendizado multimodal por meio de texto, voz, imagem e equações.
      </p>

      <h2 className="text-2xl font-semibold mt-6 mb-2">🚀 Funcionalidades</h2>
      <ul className="list-disc list-inside mb-4 space-y-1">
        <li>Suporte a múltiplos modos de entrada</li>
        <li>Modo escuro/claro com persistência local</li>
        <li>Gerenciamento de progresso do aluno</li>
        <li>Componentes reutilizáveis com design responsivo</li>
      </ul>

      <h2 className="text-2xl font-semibold mt-6 mb-2">🧱 Stack Tecnológico</h2>
      <p>Veja detalhes no README.md do projeto.</p>
    </div>
  );
}
