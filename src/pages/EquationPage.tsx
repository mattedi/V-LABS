import React from 'react';
import UnifiedLayout from '../components/layout/UnifiedLayout';
import EquationInput from '../components/multimodal/EquationInput';

export default function EquationPage() {
  return (
    <UnifiedLayout pageTitle="Equação" showTutorButtons={true}>
      <EquationInput />
    </UnifiedLayout>
  );
}
