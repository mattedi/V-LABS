import React from 'react';
import { NavLink, Outlet } from 'react-router-dom';

const HistoricoPage: React.FC = () => {
  return (
    <div className="p-6 space-y-6 bg-white dark:bg-gray-900 min-h-screen">
      <h1 className="text-3xl font-bold text-gray-800 dark:text-white">
        Histórico de Desempenho
      </h1>

      <nav className="flex gap-4 border-b border-gray-300 dark:border-gray-700 pb-2">
        <NavLink
          to="competencias"
          className={({ isActive }) =>
            isActive
              ? 'font-semibold text-blue-600'
              : 'text-gray-600 dark:text-gray-300 hover:text-blue-500'
          }
        >
          Competências
        </NavLink>
        <NavLink
          to="estudantes"
          className={({ isActive }) =>
            isActive
              ? 'font-semibold text-blue-600'
              : 'text-gray-600 dark:text-gray-300 hover:text-blue-500'
          }
        >
          Estudantes
        </NavLink>
      </nav>

      <Outlet />
    </div>
  );
};

export default HistoricoPage;



