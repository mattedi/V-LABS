import React, { useState } from 'react';

interface TextInputProps {
  onSubmit?: (question: string) => void;
}

const TextInput: React.FC<TextInputProps> = ({ onSubmit }) => {
  const [input, setInput] = useState('');

  const handleSend = () => {
    const trimmed = input.trim();
    if (!trimmed) return;

    onSubmit?.(trimmed);
    setInput('');
  };

  return (
    <div>
      <input
        className="w-full border rounded px-3 py-2 
                   bg-white text-black 
                   dark:bg-gray-900 dark:text-white
                   focus:outline-none focus:ring-2 focus:ring-blue-500"
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


