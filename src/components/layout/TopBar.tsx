import React from 'react';
import { FiSun, FiMoon, FiFile } from 'react-icons/fi';
import { useAppContext } from '../../context/AppContext';
import { Avatar } from '../common/Avatar';

const TopBar: React.FC = () => {
  const { isDarkMode, toggleDarkMode } = useAppContext();

  return (
    <header className="flex justify-between items-center px-4 py-2 bg-white dark:bg-gray-800 shadow">
      
      {/* Título com ícone funcional */}
      <div className="flex items-center gap-2 text-lg font-semibold text-gray-900 dark:text-white">
        <FiFile className="text-2xl shrink-0 text-blue-600 dark:text-blue-400" />
        <span>VIBE LEARNING STUDIO</span>
      </div>

      {/* Ações à direita */}
      <div className="flex items-center gap-4">
        {/* Botão de alternância de tema */}
        <button
          onClick={toggleDarkMode}
          className="p-2 rounded-full bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-100 hover:bg-gray-300 dark:hover:bg-gray-600 transition"
          aria-label="Alternar tema claro/escuro"
        >
          {isDarkMode ? <FiSun /> : <FiMoon />}
        </button>

        {/* Avatar do usuário */}
        <Avatar
          src="/avatars/user01.png"
          alt="Usuário"
          initials="MM"
          size="md"
          isOnline={true}
          role="tutor"
        />
      </div>
    </header>
  );
};

export default TopBar;


