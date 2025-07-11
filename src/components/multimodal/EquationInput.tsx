import React, { useState } from 'react';

export default function EquationInput() {
  const [equation, setEquation] = useState('');

  const handleSubmit = () => {
    console.log('Equação enviada:', equation);
    // Aqui: processar via LaTeX, MathML ou IA
  };

  return (
    <div>
      <input
        className="w-full p-2 border rounded"
        type="text"
        placeholder="Digite a equação (ex: x^2 + 2x + 1 = 0)"
        value={equation}
        onChange={(e) => setEquation(e.target.value)}
      />
      <button onClick={handleSubmit} className="mt-2 bg-purple-500 text-white px-4 py-2 rounded">
        Enviar Equação
      </button>
    </div>
  );
}
