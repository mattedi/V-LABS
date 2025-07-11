import React, { useState } from 'react';

export default function VoiceInput() {
  const [transcript, setTranscript] = useState('');

  const handleStart = async () => {
    // Simulação (substituir por Web Speech API ou outro mecanismo)
    setTranscript('Simulação: "Qual é a fórmula de Bhaskara?"');
  };

  return (
    <div>
      <button onClick={handleStart} className="bg-green-500 text-white px-4 py-2 rounded">
        🎤 Iniciar Gravação
      </button>
      <p className="mt-4">Transcrição: {transcript}</p>
    </div>
  );
}
