// src/components/multimodal/TextInput.tsx
import React, { useState } from 'react';

interface TextInputProps {
  onSubmit?: (question: string) => void;
}

const TextInput: React.FC<TextInputProps> = ({ onSubmit }) => {
  const [input, setInput] = useState('');

  const handleSend = () => {
    const trimmed = input.trim();
    if (!trimmed) return;

    onSubmit?.(trimmed); // chama o callback se fornecido
    setInput('');
  };

  return (
    <div>
      <input
        className="w-full border rounded px-3 py-2"
        placeholder="Digite sua pergunta..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
      />
      <button
        onClick={handleSend}
        className="bg-blue-600 text-white px-4 py-2 mt-2 rounded hover:bg-blue-700"
      >
        Enviar
      </button>
    </div>
  );
};

export default TextInput;

