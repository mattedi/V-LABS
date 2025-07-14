// src/pages/DashboardPage.tsx
import React from 'react';
import CompetencyChart from '../components/dashboard/CompetencyChart';
import StudentTable from '../components/dashboard/StudentTable';

export default function DashboardPage() {
  const dummyCompetencies = [
    { label: 'Texto', value: 85 },
    { label: 'Voz', value: 70 },
    { label: 'Imagem', value: 65 },
    { label: 'Equação', value: 50 },
  ];

  const dummyStudents = [
    { name: 'Ana Souza', questionsAsked: 15, avgComplexity: 76, lastActive: '2025-07-12' },
    { name: 'João Lima', questionsAsked: 22, avgComplexity: 61, lastActive: '2025-07-11' },
    { name: 'Carlos Menezes', questionsAsked: 8, avgComplexity: 84, lastActive: '2025-07-10' },
  ];

  return (
    <div className="space-y-6">
      <CompetencyChart data={dummyCompetencies} />
      <StudentTable students={dummyStudents} />
    </div>
  );
}
