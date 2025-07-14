// src/components/dashboard/CompetencyChart.tsx
// Exibe um gráfico de barras, radar ou pizza com níveis de competência
//  em diferentes modos de entrada (Texto, Voz, Imagem, Equação).
//  Serve como visualização sintética da performance cognitiva.


import React from 'react';
import { Radar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(RadialLinearScale, PointElement, LineElement, Tooltip, Legend);

interface CompetencyData {
  label: string;
  value: number;
}

interface CompetencyChartProps {
  data: CompetencyData[];
}

const options = {
  scales: {
    r: {
      angleLines: {
        color: 'rgba(107, 100, 100, 0.88)', // linhas radiais
      },
      grid: {
        color: 'rgba(61, 53, 53, 0.7)', // linhas circulares
      },
      pointLabels: {
        color: '#111827', // rótulos dos eixos
        font: {
          size: 14,
        },
      },
      ticks: {
        color: '#9CA3AF', // valores numéricos
        backdropColor: 'transparent',
      },
    },
  },
  plugins: {
    legend: {
      labels: {
        color: '#E5E7EB',
      },
    },
  },
};

export default function CompetencyChart({ data }: CompetencyChartProps) {
  const chartData = {
    labels: data.map(d => d.label),
    datasets: [
      {
        label: 'Nível de Competência (%)',
        data: data.map(d => d.value),
        backgroundColor: 'rgba(59,130,246,0.2)',
        borderColor: '#3B82F6',
        borderWidth: 2,
        pointBackgroundColor: '#3B82F6',
      },
    ],
  };

  return (
    <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md">
      <h3 className="text-xl font-bold text-gray-800 dark:text-white mb-4">Distribuição de Competência</h3>
      <Radar data={chartData} options={options} />
    </div>
  );
}

