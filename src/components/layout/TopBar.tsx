// src/components/layout/TopBar.tsx
import React, { useState, useRef, useEffect } from 'react';
import { FiSun, FiMoon, FiFile } from 'react-icons/fi';
import { useAppContext } from '../../context/AppContext';
import { useAuth } from '../../context/AuthContext';
import { Avatar } from '../common/Avatar';

const TopBar: React.FC = () => {
  const { isDarkMode, toggleDarkMode } = useAppContext();
  const { user, isAuthenticated, logout } = useAuth();

  const [showDropdown, setShowDropdown] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Fecha o dropdown ao clicar fora
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setShowDropdown(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const getInitials = (name: string): string =>
    name
      .split(' ')
      .map((n) => n[0])
      .join('')
      .slice(0, 2)
      .toUpperCase();

  return (
    <header className="flex justify-between items-center px-4 py-2 bg-white dark:bg-gray-800 shadow">
      {/* Logo e título */}
      <div className="flex items-center gap-2 text-lg font-semibold text-gray-900 dark:text-white">
        <FiFile className="text-2xl shrink-0 text-blue-600 dark:text-blue-400" />
        <span>VIBE LEARNING STUDIO</span>
      </div>

      {/* Botões: alternar tema e avatar */}
      <div className="flex items-center gap-4">
        {/* Alternância de tema */}
        <button
          onClick={toggleDarkMode}
          className="p-2 rounded-full bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-100 hover:bg-gray-300 dark:hover:bg-gray-600 transition"
          aria-label="Alternar tema claro/escuro"
        >
          {isDarkMode ? <FiSun /> : <FiMoon />}
        </button>

        {/* Avatar com menu dropdown */}
        {isAuthenticated && user && (
          <div className="relative z-50" ref={dropdownRef}>
            <button
              onClick={() => {
                console.log('[TopBar] Avatar clicado');
                setShowDropdown((prev) => !prev);
              }}
              className="focus:outline-none rounded-full"
              aria-label="Menu do usuário"
            >
              <Avatar
                initials={getInitials(user.username)}
                alt={user.username}
                size="md"
                isOnline={true}
                role={user.role}
              />
            </button>

            {/* Dropdown visível */}
            {showDropdown && (
              <div className="absolute right-0 mt-2 w-48 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded shadow-lg z-50">
                <button
                  onClick={() => {
                    setShowDropdown(false);
                    window.location.href = '/perfil';
                  }}
                  className="block w-full px-4 py-2 text-left text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700"
                >
                  Perfil
                </button>
                <button
                  onClick={async () => {
                    await logout();
                    window.location.href = '/login';
                  }}
                  className="block w-full px-4 py-2 text-left text-sm text-red-600 hover:bg-red-100 dark:hover:bg-red-700"
                >
                  Sair
                </button>
              </div>
            )}
          </div>
        )}
      </div>
    </header>
  );
};

export default TopBar;




