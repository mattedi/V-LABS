// src/pages/EquationPage.tsx

/**
 * Página dedicada ao modo de equação da aplicação
 * 
 * Esta página permite aos usuários trabalhar com equações matemáticas,
 * fornecendo uma interface específica para entrada, resolução e visualização
 * de equações.
 * 
 * @returns {JSX.Element} Componente da página de equação
 */

// Importa o layout principal que fornece estrutura comum (header, footer, navegação)
import MainLayout from '../components/layout/MainLayout';

/**
 * Componente principal da página de equação
 * 
 * Renderiza a interface do modo de equação, incluindo título e área
 * para componentes específicos de manipulação de equações.
 */
export default function EquationPage() {
  return (
    <MainLayout>
      {/* Título principal da página - centralizado e com espaçamento superior */}
      <h2 className="text-center text-2xl mt-8">Modo de Equação</h2>
      
      {/* 
        Área reservada para componentes específicos do modo equação:
        - Editor de equações
        - Calculadora
        - Visualizador de gráficos
        - Histórico de equações
        - Etc.
      */}
      {/* Componentes específicos */}
    </MainLayout>
  );
}