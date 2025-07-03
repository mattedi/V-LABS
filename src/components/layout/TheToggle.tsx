import React from 'react';
import { FiSun, FiMoon } from 'react-icons/fi';
import { useAppContext } from '../../context/AppContext';
import { Button } from '../common';

export default function ThemeToggle() {
  const { isDarkMode, toggleDarkMode } = useAppContext();

  return (
    <Button
      variant="icon"
      icon={isDarkMode ? <FiSun size={20} /> : <FiMoon size={20} />}
      onClick={toggleDarkMode}
      className="bg-darkgray hover:bg-[#3b3b3b]"
      aria-label={isDarkMode ? 'Mudar para tema claro' : 'Mudar para tema escuro'}
    />
  );
}