import React from 'react';
import UnifiedLayout from '../components/layout/UnifiedLayout';
import VoiceInput from '../components/multimodal/VoiceInput';

/**
 * Página de interação por voz no V-LABS.
 *
 * Renderiza uma interface para captura de perguntas via voz,
 * integrando botões de navegação e contexto de tutoria.
 *
 * @returns {JSX.Element} Página de interação por voz
 */
export default function VoicePage(): JSX.Element {
  return (
    <UnifiedLayout pageTitle="Modo de Voz" showTutorButtons={true}>
      <VoiceInput />
    </UnifiedLayout>
  );
}
