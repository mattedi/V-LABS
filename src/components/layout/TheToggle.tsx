// src/components/layout/TheToggle.tsx
// Define um componente funcional em React 
// que permite alternar entre tema claro e escuro da aplicação. 
// Ele utiliza o contexto de tema para acessar o estado atual do tema e a função de alternância.


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

// EXTENSÕES:
// - Adicionar animação de transição suave ao alternar entre temas.
// - Implementar um sistema de preferências do usuário para salvar o tema selecionado.
// - Permitir que o usuário escolha entre mais de dois temas (ex: tema claro, escuro e colorido).
// - Adicionar suporte a temas personalizados via props.
// - Implementar um sistema de notificações que informe o usuário sobre a mudança de tema.
// - Adicionar um tooltip que exiba o nome do tema atual ao passar o mouse sobre o botão.
// - Implementar um sistema de temas dinâmicos que mude automaticamente com base na hora do dia.
// - Permitir que o tema seja alterado via configuração global da aplicação.
// - Adicionar suporte a temas com cores personalizadas definidas pelo usuário.
// - Implementar um sistema de temas que se adapte ao modo de alto contraste do sistema operacional
