// src/pages/TextPage.tsx
import React from 'react';
import UnifiedLayout from '../components/layout/UnifiedLayout';
import TextInput from '../components/multimodal/TextInput';

export default function TextPage() {
  return (
    <UnifiedLayout pageTitle="Texto" showTutorButtons={true}>
      <TextInput />
    </UnifiedLayout>
  );
}
