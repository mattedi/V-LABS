// src/components/common/Button.tsx
// Componente de botão avançado com funcionalidades extras

// ================================================
// IMPORTAÇÕES
// ================================================
import React, { forwardRef } from 'react'; // React + forwardRef para refs

// ================================================
// INTERFACES E TIPOS
// ================================================

/**
 * Props do componente Button melhorado
 * 
 * Expandido com mais opções de customização mantendo compatibilidade
 * com a versão original através de valores padrão sensatos.
 * 
 * @interface ButtonProps
 */
interface ButtonProps {
  // ===== PROPS ORIGINAIS (mantidas para compatibilidade) =====
  children?: React.ReactNode; // ✅ Melhorado: tipagem mais específica
  icon?: React.ReactElement; // ✅ Melhorado: tipagem mais específica
  variant?: 'primary' | 'secondary' | 'icon' | 'danger' | 'success' | 'outline'; // ✅ Expandido
  onClick?: () => void; // ✅ Mantido igual
  className?: string; // ✅ Mantido igual
  type?: 'button' | 'submit' | 'reset'; // ✅ Mantido igual
  
  // ===== NOVAS FUNCIONALIDADES =====
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl'; // Múltiplos tamanhos
  disabled?: boolean; // Estado desabilitado
  loading?: boolean; // Estado de carregamento
  loadingText?: string; // Texto durante loading
  fullWidth?: boolean; // Largura total do container
  iconPosition?: 'left' | 'right'; // Posição do ícone
  ariaLabel?: string; // Label para acessibilidade
}

// ================================================
// CONFIGURAÇÕES E CONSTANTES
// ================================================

/**
 * Mapeamento de tamanhos para classes CSS
 * Define dimensões e proporções para cada tamanho
 */
const SIZE_CLASSES = {
  xs: 'px-2 py-1 text-xs h-6',        // Extra pequeno: 24px altura
  sm: 'px-3 py-1.5 text-sm h-8',      // Pequeno: 32px altura
  md: 'px-4 py-2 text-base h-10',     // Médio: 40px altura (padrão)
  lg: 'px-6 py-3 text-lg h-12',       // Grande: 48px altura
  xl: 'px-8 py-4 text-xl h-16'        // Extra grande: 64px altura
} as const;

/**
 * Mapeamento de variantes para classes CSS
 * Expandido com novas variantes mantendo as originais
 */
const VARIANT_CLASSES = {
  // ===== VARIANTES ORIGINAIS (mantidas) =====
  primary: 'bg-primary hover:bg-primary/80 text-white border border-transparent',
  secondary: 'bg-[#555] hover:bg-[#666] text-white border border-transparent',
  
  // ===== NOVAS VARIANTES =====
  danger: 'bg-red-500 hover:bg-red-600 text-white border border-transparent',
  success: 'bg-green-500 hover:bg-green-600 text-white border border-transparent',
  outline: 'bg-transparent hover:bg-gray-50 text-gray-700 border border-gray-300 hover:border-gray-400',
  
  // ===== VARIANTE ICON (especial - usa tamanhos próprios) =====
  icon: 'bg-[#555] hover:bg-[#666] text-white border border-transparent'
} as const;

/**
 * Classes especiais para variante icon baseadas no tamanho
 * A variante icon tem comportamento diferente (sempre quadrada)
 */
const ICON_SIZE_CLASSES = {
  xs: 'h-6 w-6 p-1',      // 24x24px
  sm: 'h-8 w-8 p-1.5',    // 32x32px
  md: 'h-10 w-10 p-2',    // 40x40px (padrão original)
  lg: 'h-12 w-12 p-2.5',  // 48x48px
  xl: 'h-16 w-16 p-3'     // 64x64px
} as const;

// ================================================
// COMPONENTES AUXILIARES
// ================================================

/**
 * Componente para spinner de loading
 * Pequena animação giratória para indicar carregamento
 * 
 * @param {Object} props - Props do spinner
 * @param {string} props.size - Tamanho do spinner baseado no botão
 */
const LoadingSpinner: React.FC<{ size: keyof typeof SIZE_CLASSES }> = ({ size }) => {
  // Tamanhos do spinner proporcionais ao botão
  const spinnerSizes = {
    xs: 'h-3 w-3',
    sm: 'h-3 w-3', 
    md: 'h-4 w-4',
    lg: 'h-5 w-5',
    xl: 'h-6 w-6'
  };

  return (
    <svg
      className={`animate-spin ${spinnerSizes[size]}`}
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
    >
      {/* Círculo de fundo (transparente) */}
      <circle
        className="opacity-25"
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        strokeWidth="4"
      />
      {/* Arco animado */}
      <path
        className="opacity-75"
        fill="currentColor"
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
      />
    </svg>
  );
};

// ================================================
// COMPONENTE PRINCIPAL
// ================================================

/**
 * Componente Button Melhorado
 * 
 * ✅ COMPATIBILIDADE TOTAL com versão original
 * ✅ Funcionalidades extras opcionais
 * ✅ Ref forwarding para integração avançada
 * ✅ Acessibilidade melhorada
 * ✅ Estados visuais aprimorados
 * 
 * Novas funcionalidades:
 * - 5 tamanhos diferentes (xs a xl)
 * - 6 variantes visuais (inclui danger, success, outline)
 * - Estado loading com spinner
 * - Estado disabled
 * - Largura total opcional
 * - Posição configurável do ícone
 * - Melhor tipagem TypeScript
 * - Ref forwarding
 * 
 * @param {ButtonProps} props - Propriedades do componente
 * @param {React.Ref} ref - Referência para o elemento button
 * @returns {JSX.Element} Botão renderizado
 */
const Button = forwardRef<HTMLButtonElement, ButtonProps>(({
  // ===== PROPS ORIGINAIS COM PADRÕES =====
  children,
  icon,
  variant = 'primary', // Mantém padrão original
  onClick,
  className = '',
  type = 'button',
  
  // ===== NOVAS PROPS COM PADRÕES =====
  size = 'md', // Tamanho padrão médio (compatível com original)
  disabled = false, // Por padrão habilitado
  loading = false, // Por padrão não carregando
  loadingText, // Texto opcional durante loading
  fullWidth = false, // Por padrão largura automática
  iconPosition = 'left', // Ícone à esquerda por padrão (mantém comportamento original)
  ariaLabel // Label de acessibilidade opcional
}, ref) => {
  
  // ================================================
  // LÓGICA DE ESTADO E COMPORTAMENTO
  // ================================================
  
  /**
   * Determina se o botão deve estar funcionalmente desabilitado
   * Combina prop disabled com estado loading
   */
  const isDisabled = disabled || loading;
  
  /**
   * Texto a ser exibido baseado no estado
   * Durante loading, pode mostrar texto alternativo
   */
  const displayText = loading && loadingText ? loadingText : children;
  
  /**
   * Determina se deve mostrar o ícone
   * Não mostra ícone original durante loading (spinner substitui)
   */
  const shouldShowIcon = icon && !loading;

  // ================================================
  // CONSTRUÇÃO DE CLASSES CSS
  // ================================================
  
  /**
   * Classes base aplicadas a todos os botões
   * Expandidas com novas funcionalidades
   */
  const baseClasses = `
    relative overflow-hidden
    flex items-center justify-center
    font-medium leading-none
    transition-all duration-200
    focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary/50
    disabled:opacity-50 disabled:cursor-not-allowed disabled:pointer-events-none
    ${fullWidth ? 'w-full' : ''}
  `;

  /**
   * Classes específicas da variante
   * Para variante icon, usa classes especiais
   */
  const variantClasses = variant === 'icon' 
    ? `${VARIANT_CLASSES.icon} rounded-full ${ICON_SIZE_CLASSES[size]}`
    : `${VARIANT_CLASSES[variant]} rounded-lg ${SIZE_CLASSES[size]}`;

  /**
   * Classes finais combinadas
   * Ordem importante para permitir sobrescrita
   */
  const finalClasses = `${baseClasses} ${variantClasses} ${className}`;

  // ================================================
  // HANDLERS DE EVENTOS
  // ================================================
  
  /**
   * Handler de clique que respeita estados disabled/loading
   * Só executa onClick se botão estiver habilitado
   */
  const handleClick = (): void => {
    if (!isDisabled && onClick) {
      onClick();
    }
  };

  // ================================================
  // RENDERIZAÇÃO
  // ================================================

  return (
    <button
      ref={ref} // Forwarded ref para acesso ao elemento DOM
      type={type}
      className={finalClasses}
      onClick={handleClick}
      disabled={isDisabled} // HTML disabled attribute
      aria-label={ariaLabel} // Acessibilidade
      aria-busy={loading} // Indica estado de carregamento para screen readers
    >
      {/* ============================================== */}
      {/* CONTEÚDO DO BOTÃO */}
      {/* ============================================== */}
      
      {/* LOADING SPINNER (quando loading = true) */}
      {loading && (
        <LoadingSpinner size={size} />
      )}
      
      {/* ÍCONE (posição left + não loading) */}
      {shouldShowIcon && iconPosition === 'left' && (
        <span className={displayText ? 'mr-2' : ''}>
          {icon}
        </span>
      )}
      
      {/* TEXTO/CHILDREN */}
      {displayText && (
        <span className={loading ? 'ml-2' : ''}>
          {displayText}
        </span>
      )}
      
      {/* ÍCONE (posição right + não loading) */}
      {shouldShowIcon && iconPosition === 'right' && (
        <span className={displayText ? 'ml-2' : ''}>
          {icon}
        </span>
      )}
      
    </button>
  );
});

// ================================================
// CONFIGURAÇÕES DO COMPONENTE
// ================================================

/**
 * Nome de display para debugging
 * Útil em React DevTools
 */
Button.displayName = 'Button';

// ================================================
// EXPORTAÇÃO
// ================================================

export default Button;

// ================================================
// EXEMPLOS DE USO AVANÇADOS
// ================================================

/**
 * 🚀 EXEMPLOS DA VERSÃO MELHORADA:
 * 
 * // 1. USO ORIGINAL (mantém compatibilidade total)
 * <Button>Clique aqui</Button>
 * <Button variant="secondary">Cancelar</Button>
 * <Button icon={<FiUser />} variant="icon" />
 * 
 * // 2. NOVOS TAMANHOS
 * <Button size="xs">Pequeno</Button>
 * <Button size="xl">Extra Grande</Button>
 * 
 * // 3. NOVAS VARIANTES
 * <Button variant="danger">Excluir</Button>
 * <Button variant="success">Confirmar</Button>
 * <Button variant="outline">Neutro</Button>
 * 
 * // 4. ESTADO LOADING
 * <Button loading={isSubmitting} loadingText="Salvando...">
 *   Salvar
 * </Button>
 * 
 * // 5. ESTADO DISABLED
 * <Button disabled={!isValid}>
 *   Enviar Formulário
 * </Button>
 * 
 * // 6. LARGURA COMPLETA
 * <Button fullWidth variant="primary">
 *   Botão de Largura Total
 * </Button>
 * 
 * // 7. ÍCONE À DIREITA
 * <Button icon={<FiArrowRight />} iconPosition="right">
 *   Próximo
 * </Button>
 * 
 * // 8. COM REF (para integração avançada)
 * const buttonRef = useRef<HTMLButtonElement>(null);
 * <Button ref={buttonRef}>Com Ref</Button>
 * 
 * // 9. ACESSIBILIDADE MELHORADA
 * <Button 
 *   variant="icon" 
 *   icon={<FiX />}
 *   ariaLabel="Fechar modal"
 * />
 * 
 * // 10. COMBINAÇÃO COMPLETA
 * <Button
 *   variant="primary"
 *   size="lg"
 *   icon={<FiSave />}
 *   loading={isSaving}
 *   loadingText="Salvando..."
 *   disabled={!isFormValid}
 *   fullWidth
 *   className="shadow-lg"
 *   onClick={handleSave}
 *   ariaLabel="Salvar documento"
 * >
 *   Salvar Documento
 * </Button>
 */

/**
 * 📊 COMPARAÇÃO DE TAMANHOS VISUAIS:
 * 
 * XS: [pequeno]     (h-6, 24px)
 * SM: [médio-peq]   (h-8, 32px)  
 * MD: [médio]       (h-10, 40px) ← Original
 * LG: [grande]      (h-12, 48px)
 * XL: [extra-grd]   (h-16, 64px)
 */

/**
 * 🎨 PALETA DE VARIANTES:
 * 
 * primary   → Azul (ações principais)
 * secondary → Cinza (ações secundárias)  
 * danger    → Vermelho (ações perigosas)
 * success   → Verde (confirmações)
 * outline   → Transparente com borda (neutro)
 * icon      → Compacto circular (ações rápidas)
 */

/**
 * 🔄 ESTADOS VISUAIS:
 * 
 * Normal    → Cores padrão
 * Hover     → Cores mais escuras/claras
 * Loading   → Spinner + texto opcional
 * Disabled  → Opacidade 50% + cursor blocked
 * Focus     → Ring azul para navegação por teclado
 */

// ================================================
// MIGRAÇÃO DA VERSÃO ORIGINAL
// ================================================

/**
 * 📈 GUIA DE MIGRAÇÃO:
 * 
 * A versão melhorada é 100% compatível com a original:
 * 
 * // ✅ ANTES (versão original):
 * <Button>Texto</Button>
 * <Button variant="secondary">Cancelar</Button>
 * <Button icon={<Icon />} variant="icon" />
 * 
 * // ✅ DEPOIS (funciona exatamente igual):
 * <Button>Texto</Button>
 * <Button variant="secondary">Cancelar</Button>  
 * <Button icon={<Icon />} variant="icon" />
 * 
 * // 🚀 PLUS (novas funcionalidades opcionais):
 * <Button loading={true}>Carregando...</Button>
 * <Button size="lg" variant="success">Grande Sucesso</Button>
 * <Button disabled fullWidth>Largura Total Desabilitado</Button>
 */