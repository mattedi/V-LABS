// src/components/multimodal/QuestionInputPanel.tsx

import React, { useState } from 'react';
import TextInput from './TextInput.tsx';
import VoiceInput from './VoiceInput.tsx';
import ImageInput from './ImageInput.tsx';
import EquationInput from './EquationInput.tsx';


export default function QuestionInputPanel() {
  const [mode, setMode] = useState<'text' | 'voice' | 'image' | 'equation'>('text');

  return (
    <div className="flex flex-col gap-4">
      <div className="flex gap-2">
        <button onClick={() => setMode('text')}>Texto</button>
        <button onClick={() => setMode('voice')}>Voz</button>
        <button onClick={() => setMode('image')}>Imagem</button>
        <button onClick={() => setMode('equation')}>Equação</button>
      </div>

      <div className="mt-4">
        {mode === 'text' && <TextInput />}
        {mode === 'voice' && <VoiceInput />}
        {mode === 'image' && <ImageInput />}
        {mode === 'equation' && <EquationInput />}
      </div>
    </div>
  );
}
