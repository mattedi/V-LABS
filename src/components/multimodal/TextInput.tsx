// TextInput.tsx
import React, { useState } from 'react';

export default function TextInput() {
  const [text, setText] = useState('');

  const handleSubmit = () => {
    console.log('Texto enviado:', text);
    // Aqui: enviar ao contexto ou backend
  };

  return (
    <div>
      <textarea
        className="w-full p-2 border rounded"
        placeholder="Digite sua pergunta em texto..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <button onClick={handleSubmit} className="mt-2 bg-blue-500 text-white px-4 py-2 rounded">
        Enviar
      </button>
    </div>
  );
}
