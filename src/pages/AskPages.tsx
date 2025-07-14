import React, { useState } from 'react';
import UnifiedLayout from '../components/layout/UnifiedLayout';
import TextInput from '../components/multimodal/TextInput';
import VoiceInput from '../components/multimodal/VoiceInput';
import ImageInput from '../components/multimodal/ImageInput';
import EquationInput from '../components/multimodal/EquationInput';

export default function AskPage() {
  const [mode, setMode] = useState<'text' | 'voice' | 'image' | 'equation'>('text');

  const renderInputComponent = () => {
    switch (mode) {
      case 'text':
        return <TextInput />;
      case 'voice':
        return <VoiceInput />;
      case 'image':
        return <ImageInput />;
      case 'equation':
        return <EquationInput />;
      default:
        return null;
    }
  };

  return (
    <UnifiedLayout pageTitle="Perguntas Multimodais" showTutorButtons={true}>
      <div className="max-w-4xl mx-auto">
        <h2 className="text-2xl font-bold text-center mb-6 text-blue-700">
          Escolha o modo de entrada para sua pergunta:
        </h2>

        <div className="flex justify-center gap-4 mb-6">
          <button onClick={() => setMode('text')} className={`px-4 py-2 rounded ${mode === 'text' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}>Texto</button>
          <button onClick={() => setMode('voice')} className={`px-4 py-2 rounded ${mode === 'voice' ? 'bg-green-500 text-white' : 'bg-gray-200'}`}>Voz</button>
          <button onClick={() => setMode('image')} className={`px-4 py-2 rounded ${mode === 'image' ? 'bg-yellow-500 text-white' : 'bg-gray-200'}`}>Imagem</button>
          <button onClick={() => setMode('equation')} className={`px-4 py-2 rounded ${mode === 'equation' ? 'bg-purple-500 text-white' : 'bg-gray-200'}`}>Equação</button>
        </div>

        <div className="p-4 bg-white dark:bg-gray-800 rounded shadow">
          {renderInputComponent()}
        </div>
      </div>
    </UnifiedLayout>
  );
}

