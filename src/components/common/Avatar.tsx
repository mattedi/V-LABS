// src/components/common/Avatar.tsx
// Componente avançado de avatar com múltiplas funcionalidades

// ================================================
// IMPORTAÇÕES
// ================================================
import React from 'react'; // Biblioteca principal do React

// ================================================
// INTERFACES E TIPOS
// ================================================

/**
 * Props do componente Avatar melhorado
 * 
 * Expandido com mais opções de customização:
 * - Suporte a imagem
 * - Múltiplas cores
 * - Indicador de status
 * - Formato quadrado ou circular
 * - Bordas opcionais
 * 
 * @interface AvatarProps
 */
interface AvatarProps {
  initials?: string; // Iniciais quando não há imagem
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl'; // Tamanhos expandidos
  color?: 'gray' | 'blue' | 'green' | 'red' | 'purple' | 'orange'; // Cores temáticas
  shape?: 'circle' | 'square'; // Formato do avatar
  src?: string; // URL da imagem (opcional)
  alt?: string; // Texto alternativo para imagem
  status?: 'online' | 'offline' | 'away' | 'busy'; // Status do usuário
  bordered?: boolean; // Se deve ter borda
  className?: string; // Classes CSS adicionais
  onClick?: () => void; // Callback para clique (avatar clicável)
}

// ================================================
// CONFIGURAÇÕES E CONSTANTES
// ================================================

/**
 * Mapeamento de tamanhos para classes CSS
 * Expandido com mais opções (xs e xl)
 */
const SIZE_CLASSES = {
  xs: 'h-6 w-6 text-xs',      // 24x24px, fonte 12px - para listas compactas
  sm: 'h-8 w-8 text-xs',      // 32x32px, fonte 12px - para barras/headers
  md: 'h-12 w-12 text-base',  // 48x48px, fonte 16px - padrão/uso geral
  lg: 'h-16 w-16 text-xl',    // 64x64px, fonte 20px - perfis/destaque
  xl: 'h-24 w-24 text-3xl'    // 96x96px, fonte 30px - páginas de perfil
} as const;

/**
 * Mapeamento de cores para classes CSS
 * Cada cor inclui fundo e possível cor de texto contrastante
 */
const COLOR_CLASSES = {
  gray: 'bg-gray-500 text-white',           // Padrão neutro
  blue: 'bg-blue-500 text-white',           // Profissional/corporativo
  green: 'bg-green-500 text-white',         // Sucesso/positivo
  red: 'bg-red-500 text-white',             // Erro/importante
  purple: 'bg-purple-500 text-white',       // Criativo/premium
  orange: 'bg-orange-500 text-white'        // Energia/atenção
} as const;

/**
 * Mapeamento de status para cores e ícones
 * Pequenos indicadores no canto do avatar
 */
const STATUS_CONFIG = {
  online: { color: 'bg-green-400', icon: '●', label: 'Online' },
  offline: { color: 'bg-gray-400', icon: '●', label: 'Offline' },
  away: { color: 'bg-yellow-400', icon: '●', label: 'Ausente' },
  busy: { color: 'bg-red-400', icon: '●', label: 'Ocupado' }
} as const;

// ================================================
// FUNÇÕES AUXILIARES
// ================================================

/**
 * Gera cor baseada no nome/iniciais para avatares únicos
 * Algoritmo simples que converte string em cor consistente
 * 
 * @param {string} input - Texto para gerar cor
 * @returns {keyof typeof COLOR_CLASSES} Cor correspondente
 */
function generateColorFromInitials(input: string): keyof typeof COLOR_CLASSES {
  const colors: (keyof typeof COLOR_CLASSES)[] = ['blue', 'green', 'purple', 'orange', 'red'];
  const hash = input.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0);
  return colors[hash % colors.length];
}

/**
 * Extrai iniciais de um nome completo
 * 
 * @param {string} name - Nome completo
 * @returns {string} Iniciais (máximo 2 caracteres)
 * 
 * @example
 * extractInitials("João Silva") // "JS"
 * extractInitials("Maria") // "MA"
 */
function extractInitials(name: string): string {
  return name
    .split(' ')
    .filter(word => word.length > 0)
    .slice(0, 2)
    .map(word => word[0])
    .join('')
    .toUpperCase();
}

// ================================================
// COMPONENTES AUXILIARES
// ================================================

/**
 * Componente para indicador de status
 * Pequeno círculo no canto inferior direito do avatar
 * 
 * @param {Object} props - Props do status
 * @param {string} status - Tipo do status
 * @param {string} size - Tamanho do avatar (para ajustar indicador)
 */
const StatusIndicator: React.FC<{ 
  status: NonNullable<AvatarProps['status']>; 
  size: NonNullable<AvatarProps['size']>;
}> = ({ status, size }) => {
  const config = STATUS_CONFIG[status];
  
  // Tamanho do indicador baseado no tamanho do avatar
  const indicatorSizes = {
    xs: 'h-2 w-2',
    sm: 'h-2 w-2',
    md: 'h-3 w-3',
    lg: 'h-4 w-4',
    xl: 'h-5 w-5'
  };

  return (
    <div 
      className={`
        absolute -bottom-0 -right-0 
        ${indicatorSizes[size]} 
        ${config.color} 
        rounded-full border-2 border-white
      `}
      title={config.label} // Tooltip informativo
      aria-label={`Status: ${config.label}`}
    >
      {/* Indicador visual de status */}
    </div>
  );
};

// ================================================
// COMPONENTE PRINCIPAL
// ================================================

/**
 * Componente Avatar Melhorado
 * 
 * Funcionalidades avançadas:
 * - Suporte a imagem com fallback para iniciais
 * - Múltiplos tamanhos (xs a xl)
 * - Múltiplas cores temáticas
 * - Indicador de status opcional
 * - Formato circular ou quadrado
 * - Geração automática de cor baseada nas iniciais
 * - Clicável com callback opcional
 * - Bordas opcionais
 * - Totalmente acessível
 * 
 * @param {AvatarProps} props - Propriedades do componente
 * @returns {JSX.Element} Avatar renderizado
 */
const Avatar: React.FC<AvatarProps> = ({
  initials = "ID", // Iniciais padrão
  size = 'md', // Tamanho padrão médio
  color, // Cor automática se não especificada
  shape = 'circle', // Formato padrão circular
  src, // Imagem opcional
  alt, // Texto alternativo da imagem
  status, // Status opcional
  bordered = false, // Sem borda por padrão
  className = '', // Classes extras
  onClick // Callback de clique opcional
}) => {
  
  // ================================================
  // LÓGICA DE COR AUTOMÁTICA
  // ================================================
  
  /**
   * Determina a cor final do avatar
   * Se não especificada, gera baseada nas iniciais
   */
  const finalColor = color || generateColorFromInitials(initials);

  // ================================================
  // CONSTRUÇÃO DE CLASSES CSS
  // ================================================
  
  /**
   * Classes base que sempre são aplicadas
   */
  const baseClasses = `
    ${SIZE_CLASSES[size]}
    ${shape === 'circle' ? 'rounded-full' : 'rounded-lg'}
    flex items-center justify-center
    font-bold
    transition-all duration-200
    ${onClick ? 'cursor-pointer hover:scale-105' : ''}
    ${bordered ? 'border-2 border-white shadow-lg' : ''}
  `;

  /**
   * Classes específicas para conteúdo (iniciais vs imagem)
   */
  const contentClasses = src 
    ? 'overflow-hidden' // Para imagem
    : COLOR_CLASSES[finalColor]; // Para iniciais

  /**
   * Classes finais combinadas
   */
  const finalClasses = `${baseClasses} ${contentClasses} ${className}`;

  // ================================================
  // HANDLERS DE EVENTOS
  // ================================================
  
  /**
   * Handler para clique no avatar
   * Executa callback se fornecido e se avatar é clicável
   */
  const handleClick = (): void => {
    if (onClick) {
      onClick();
    }
  };

  /**
   * Handler para erro no carregamento da imagem
   * Remove src para fazer fallback para iniciais
   */
  const handleImageError = (e: React.SyntheticEvent<HTMLImageElement>): void => {
    e.currentTarget.style.display = 'none';
  };

  // ================================================
  // RENDERIZAÇÃO
  // ================================================

  return (
    <div 
      className={`relative inline-block`}
      role={onClick ? 'button' : 'img'} // Role baseado em funcionalidade
      aria-label={
        src 
          ? alt || `Avatar com imagem` 
          : `Avatar com iniciais ${initials}`
      }
      tabIndex={onClick ? 0 : undefined} // Navegação por teclado se clicável
      onClick={handleClick}
      onKeyDown={(e) => {
        // Ativação por teclado (Enter ou Space)
        if (onClick && (e.key === 'Enter' || e.key === ' ')) {
          e.preventDefault();
          handleClick();
        }
      }}
    >
      {/* ============================================== */}
      {/* CONTAINER PRINCIPAL DO AVATAR */}
      {/* ============================================== */}
      
      <div className={finalClasses}>
        
        {/* RENDERIZAÇÃO CONDICIONAL: IMAGEM vs INICIAIS */}
        {src ? (
          // Se há URL de imagem, renderiza <img>
          <img
            src={src}
            alt={alt || `Avatar`}
            className={`
              w-full h-full object-cover
              ${shape === 'circle' ? 'rounded-full' : 'rounded-lg'}
            `}
            onError={handleImageError} // Fallback em caso de erro
          />
        ) : (
          // Se não há imagem, renderiza iniciais
          <span className="select-none">
            {initials}
          </span>
        )}
        
      </div>
      
      {/* ============================================== */}
      {/* INDICADOR DE STATUS (OPCIONAL) */}
      {/* ============================================== */}
      
      {status && (
        <StatusIndicator status={status} size={size} />
      )}
      
    </div>
  );
};

// ================================================
// EXPORTAÇÃO
// ================================================

export default Avatar;

// ================================================
// EXEMPLOS DE USO AVANÇADOS
// ================================================

/**
 * 🚀 EXEMPLOS DE USO DA VERSÃO MELHORADA:
 * 
 * // 1. AVATAR BÁSICO (igual à versão original)
 * <Avatar />
 * 
 * // 2. AVATAR COM IMAGEM
 * <Avatar 
 *   src="https://example.com/user.jpg"
 *   alt="Foto do usuário"
 *   size="lg"
 * />
 * 
 * // 3. AVATAR COM STATUS
 * <Avatar 
 *   initials="JS"
 *   status="online"
 *   size="md"
 * />
 * 
 * // 4. AVATAR CLICÁVEL
 * <Avatar 
 *   initials="AM"
 *   onClick={() => openUserProfile()}
 *   bordered={true}
 * />
 * 
 * // 5. AVATAR QUADRADO COLORIDO
 * <Avatar 
 *   initials="VL"
 *   shape="square"
 *   color="purple"
 *   size="xl"
 * />
 * 
 * // 6. LISTA DE AVATARES COM CORES AUTOMÁTICAS
 * {users.map(user => (
 *   <Avatar 
 *     key={user.id}
 *     initials={extractInitials(user.name)}
 *     size="sm"
 *     status={user.isOnline ? 'online' : 'offline'}
 *   />
 * ))}
 * 
 * // 7. AVATAR DE PERFIL COMPLETO
 * <Avatar 
 *   src={user.profilePicture}
 *   alt={`Foto de ${user.name}`}
 *   initials={extractInitials(user.name)}
 *   size="xl"
 *   status={user.status}
 *   bordered={true}
 *   onClick={() => setShowProfile(true)}
 *   className="shadow-xl"
 * />
 */

/**
 * 🎨 COMPARAÇÃO VISUAL DOS TAMANHOS:
 * 
 * XS (24px): 👤  - Para listas compactas
 * SM (32px): 👤  - Para headers/barras
 * MD (48px): 👤  - Uso geral padrão
 * LG (64px): 👤  - Destaque/perfis
 * XL (96px): 👤  - Páginas de perfil
 */

/**
 * 🌈 PALETA DE CORES DISPONÍVEIS:
 * 
 * gray   → Neutro/padrão
 * blue   → Profissional
 * green  → Sucesso/ativo
 * red    → Importante/erro
 * purple → Premium/criativo  
 * orange → Energia/atenção
 */