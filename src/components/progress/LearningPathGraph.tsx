import React from 'react';
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';

ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement, Tooltip, Legend);

interface LearningPathGraphProps {
  data: {
    date: string;
    text: number;
    voice: number;
    image: number;
    equation: number;
  }[];
}

export default function LearningPathGraph({ data }: LearningPathGraphProps): JSX.Element {
  const labels = data.map(entry => entry.date);

  const datasetTemplate = (label: string, color: string, accessor: keyof typeof data[0]) => ({
    label,
    data: data.map(entry => entry[accessor]),
    borderColor: color,
    backgroundColor: color,
    tension: 0.3,
    fill: false,
  });

  const chartData = {
    labels,
    datasets: [
      datasetTemplate('Texto', '#3B82F6', 'text'),
      datasetTemplate('Voz', '#10B981', 'voice'),
      datasetTemplate('Imagem', '#F59E0B', 'image'),
      datasetTemplate('Equação', '#8B5CF6', 'equation'),
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'bottom' as const,
        labels: {
          color: '#374151',
          font: {
            size: 14,
          },
        },
      },
      tooltip: {
        mode: 'index' as const,
        intersect: false,
      },
    },
    scales: {
      x: {
        ticks: { color: '#6B7280' },
        grid: { display: false },
      },
      y: {
        beginAtZero: true,
        ticks: { color: '#6B7280' },
      },
    },
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-md">
      <h3 className="text-xl font-semibold text-gray-800 dark:text-gray-100 mb-4">
        Trajetória de Aprendizagem
      </h3>
      <Line data={chartData} options={chartOptions} />
    </div>
  );
}
