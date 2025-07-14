// src/pages/CompetencyChartPage.tsx
import React from 'react';
import CompetencyChart from '../components/dashboard/CompetencyChart';

const mockCompetencies = [
  { label: 'Álgebra', value: 80 },
  { label: 'Geometria', value: 65 },
  { label: 'Cálculo', value: 70 },
  { label: 'Estatística', value: 60 },
  { label: 'Trigonometria', value: 75 },
];

const CompetencyChartPage: React.FC = () => {
  return (
    <div>
      <CompetencyChart data={mockCompetencies} />
    </div>
  );
};

export default CompetencyChartPage;
