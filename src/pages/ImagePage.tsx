import React from 'react';
import UnifiedLayout from '../components/layout/UnifiedLayout';
import ImageInput from '../components/multimodal/ImageInput';

export default function ImagePage() {
  return (
    <UnifiedLayout pageTitle="Imagem" showTutorButtons={true}>
      <ImageInput />
    </UnifiedLayout>
  );
}

