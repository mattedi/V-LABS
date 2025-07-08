import React from 'react';
import { useTheme } from '../../context/ThemeContext';
import { FiMoon, FiSun } from 'react-icons/fi';
import { Button } from '../common/Button';

export default function ThemeToggle(): React.JSX.Element {
  const { theme, toggleTheme } = useTheme();
  const isDark = theme === 'dark';

  const icon = isDark ? <FiSun size={18} /> : <FiMoon size={18} />;
  const label = isDark ? 'Ativar tema claro' : 'Ativar tema escuro';
  const title = isDark ? 'Tema claro' : 'Tema escuro';

  return (
    <Button
      onClick={toggleTheme}
      variant="secondary"
      size="sm"
      className="p-2 rounded-full"
      aria-label={label}
      title={title}
    >
      <span className="sr-only">{label}</span>
      {icon}
    </Button>
  );
}


