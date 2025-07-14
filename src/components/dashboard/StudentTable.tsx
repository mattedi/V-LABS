// Mostra uma tabela detalhada com métricas por estudante, 
// como acertos, complexidade média das perguntas e 
// evolução por data ou por tipo.
//  Ideal para diagnóstico mais granular.

import React from 'react';

// Tipagem explícita
interface Student {
  name: string;
  score: number;
}

const mockStudents: Student[] = [
  { name: 'João Silva', score: 85 },
  { name: 'Maria Souza', score: 90 },
  { name: 'Carlos Lima', score: 78 },
];

const StudentTable: React.FC = () => {
  return (
    <div className="overflow-x-auto bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mt-8">
      <h3 className="text-xl font-bold text-gray-800 dark:text-white mb-4">Tabela de Estudantes</h3>

      <table className="min-w-full divide-y divide-gray-300 dark:divide-gray-700">
        <thead className="bg-gray-100 dark:bg-gray-700">
          <tr>
            <th className="text-left px-6 py-3 text-sm font-semibold text-gray-800 dark:text-gray-100">
              Nome
            </th>
            <th className="text-left px-6 py-3 text-sm font-semibold text-gray-800 dark:text-gray-100">
              Pontuação
            </th>
          </tr>
        </thead>

        <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
          {mockStudents.map((student, index) => (
            <tr key={index}>
              <td className="px-6 py-4 text-gray-900 dark:text-gray-100">{student.name}</td>
              <td className="px-6 py-4 text-gray-700 dark:text-gray-300">{student.score}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default StudentTable;

