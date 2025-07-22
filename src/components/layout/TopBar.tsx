// src/components/layout/TopBar.tsx
// src/components/layout/TopBar.tsx

// src/components/layout/TopBar.tsx
// src/components/layout/TopBar.tsx
// src/components/layout/TopBar.tsx
import React, { useState, useRef, useEffect } from 'react';
import { FiSun, FiMoon, FiFile } from 'react-icons/fi';
import { useAppContext } from '../../context/AppContext';

interface TopBarProps {
  pageTitle?: string;
}

const TopBarIntegrated: React.FC<TopBarProps> = ({ pageTitle = "VIBE LEARNING STUDIO" }) => {
  const { isDarkMode, toggleDarkMode } = useAppContext();
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Fecha dropdown clicando fora
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsDropdownOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <header className="flex justify-between items-center px-4 py-2 bg-white dark:bg-gray-800 shadow z-40 relative">
      {/* Título da Página */}
      <div className="flex items-center gap-2 text-lg font-semibold text-gray-900 dark:text-white">
        <FiFile className="text-2xl shrink-0 text-blue-600 dark:text-blue-400" />
        <span>{pageTitle}</span>
      </div>

      {/* Ações à Direita */}
      <div className="flex items-center gap-4">
        {/* Link para documentação */}
        <a
          href="/docs"
          className="text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors text-sm font-medium"
        >
          Documentação
        </a>

        {/* Botão de alternância de tema */}
        <button
          onClick={toggleDarkMode}
          className="p-2 rounded-full bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-100 hover:bg-gray-300 dark:hover:bg-gray-600 transition"
          aria-label="Alternar tema"
          title={isDarkMode ? 'Ativar tema claro' : 'Ativar tema escuro'}
        >
          {isDarkMode ? <FiSun /> : <FiMoon />}
        </button>

        {/* Botão MM com Dropdown */}
        <div className="relative" ref={dropdownRef}>
          <button
            onClick={() => setIsDropdownOpen((prev) => !prev)}
            className="flex items-center justify-center w-8 h-8 bg-blue-600 text-white rounded-full text-sm font-semibold focus:outline-none"
            aria-haspopup="true"
            aria-expanded={isDropdownOpen}
            aria-label="Menu do usuário"
          >
            MM
          </button>

          {isDropdownOpen && (
            <div
              className="absolute right-0 top-10 mt-1 w-44 bg-white dark:bg-gray-700 rounded-md shadow-lg z-50"
              role="menu"
              aria-label="Menu do usuário"
            >
              <ul className="py-1 text-sm text-gray-700 dark:text-gray-200">
                <li>
                  <a
                    href="/perfil"
                    className="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600"
                    role="menuitem"
                  >
                    Meu Perfil
                  </a>
                </li>
                <li>
                  <a
                    href="/ajustes"
                    className="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600"
                    role="menuitem"
                  >
                    Ajustes
                  </a>
                </li>
                <li>
                  <button
                    onClick={() => alert('Logout acionado')} // Substituir por lógica real
                    className="block w-full text-left px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600"
                    role="menuitem"
                  >
                    Sair
                  </button>
                </li>
              </ul>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};

export default TopBarIntegrated;




