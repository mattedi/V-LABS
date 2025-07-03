// src/components/common/index.ts
// Arquivo de exportação centralizada para componentes comuns/reutilizáveis

/**
 * ================================================
 * CONCEITO: BARREL EXPORT PARA COMPONENTES COMUNS
 * ================================================
 * 
 * Esta pasta contém componentes que são:
 * - Reutilizáveis em múltiplas partes da aplicação
 * - Genéricos e sem lógica de negócio específica
 * - Básicos como botões, inputs, avatares, etc.
 * - Independentes de contexto específico
 * 
 * ESTRUTURA DA PASTA COMMON:
 * src/components/common/
 * ├── Avatar.tsx           ← Componente de avatar com iniciais/imagem
 * ├── Button.tsx           ← Botão reutilizável com variantes
 * ├── Input.tsx            ← Campo de entrada (futuro)
 * ├── Modal.tsx            ← Modal/popup (futuro)
 * ├── Spinner.tsx          ← Indicador de carregamento (futuro)
 * ├── Badge.tsx            ← Etiquetas/tags (futuro)
 * └── index.ts            ← Este arquivo (centralizador)
 * 
 * FILOSOFIA DOS COMPONENTES COMUNS:
 * - Design system consistency
 * - Reusabilidade máxima
 * - Props bem definidas
 * - Acessibilidade built-in
 * - Customização via props/classes
 */

// ================================================
// IMPORTAÇÕES DOS COMPONENTES LOCAIS
// ================================================

/**
 * Importa o componente Avatar
 * 
 * Avatar é responsável por:
 * - Exibir avatar circular ou quadrado
 * - Suporte a imagem com fallback para iniciais
 * - Múltiplos tamanhos (xs, sm, md, lg, xl)
 * - Múltiplas cores temáticas
 * - Indicador de status opcional
 * - Funcionalidade de clique opcional
 * - Acessibilidade completa
 */
import Avatar from './Avatar';

/**
 * Importa o componente Button
 * 
 * Button é responsável por:
 * - Botão reutilizável com múltiplas variantes
 * - Suporte a ícones
 * - Estados (disabled, loading, etc.)
 * - Tamanhos variados
 * - Tipos diferentes (primary, secondary, etc.)
 */
import Button from './Button';

// ================================================
// FUTURAS IMPORTAÇÕES (componentes planejados)
// ================================================

// Componentes que podem ser adicionados no futuro:

// import Input from './Input';               // Campo de entrada customizável
// import TextArea from './TextArea';         // Área de texto
// import Select from './Select';             // Dropdown/seletor
// import Checkbox from './Checkbox';         // Caixa de seleção
// import Radio from './Radio';               // Botão de rádio
// import Switch from './Switch';             // Interruptor on/off
// import Slider from './Slider';             // Controle deslizante
// import Modal from './Modal';               // Modal/popup
// import Dialog from './Dialog';             // Diálogo de confirmação
// import Tooltip from './Tooltip';           // Dica de ferramenta
// import Popover from './Popover';           // Popup informativo
// import Dropdown from './Dropdown';         // Menu dropdown
// import Spinner from './Spinner';           // Indicador de carregamento
// import Progress from './Progress';          // Barra de progresso
// import Badge from './Badge';               // Etiqueta/tag
// import Chip from './Chip';                 // Chip removível
// import Alert from './Alert';               // Mensagem de alerta
// import Toast from './Toast';               // Notificação temporária
// import Card from './Card';                 // Container de conteúdo
// import Divider from './Divider';           // Separador visual
// import Skeleton from './Skeleton';         // Placeholder de carregamento
// import Image from './Image';               // Imagem com lazy loading
// import Icon from './Icon';                 // Ícone customizável
// import Link from './Link';                 // Link estilizado
// import Text from './Text';                 // Texto com variantes
// import Heading from './Heading';           // Cabeçalho com níveis
// import Table from './Table';               // Tabela responsiva
// import Pagination from './Pagination';     // Paginação
// import Breadcrumb from './Breadcrumb';     // Migalhas de pão
// import Tabs from './Tabs';                 // Abas/guias
// import Accordion from './Accordion';       // Acordeão expansível
// import Collapsible from './Collapsible';   // Conteúdo colapsável

// ================================================
// RE-EXPORTAÇÕES (EXPORTS)
// ================================================

/**
 * Re-exporta Avatar como named export
 * 
 * Transforma: default export → named export
 * Permite: import { Avatar } from '../common'
 */
export { Avatar };

/**
 * Re-exporta Button como named export
 * 
 * Transforma: default export → named export
 * Permite: import { Button } from '../common'
 */
export { Button };

// ================================================
// FUTURAS RE-EXPORTAÇÕES
// ================================================

// Quando os componentes futuros forem criados, adicionar aqui:
// export { Input };
// export { TextArea };
// export { Select };
// export { Checkbox };
// export { Radio };
// export { Switch };
// export { Slider };
// export { Modal };
// export { Dialog };
// export { Tooltip };
// export { Popover };
// export { Dropdown };
// export { Spinner };
// export { Progress };
// export { Badge };
// export { Chip };
// export { Alert };
// export { Toast };
// export { Card };
// export { Divider };
// export { Skeleton };
// export { Image };
// export { Icon };
// export { Link };
// export { Text };
// export { Heading };
// export { Table };
// export { Pagination };
// export { Breadcrumb };
// export { Tabs };
// export { Accordion };
// export { Collapsible };

// ================================================
// EXPORTAÇÃO DE TIPOS (opcional)
// ================================================

/**
 * Se os componentes exportarem tipos/interfaces,
 * podemos re-exportá-los também para uso externo
 * 
 * Exemplos futuros:
 * export type { AvatarProps } from './Avatar';
 * export type { ButtonProps } from './Button';
 * export type { InputProps } from './Input';
 * export type { ModalProps } from './Modal';
 */

// ================================================
// EXEMPLOS DE USO DESTE ARQUIVO
// ================================================

/**
 * 🚀 COMO USAR EM OUTROS ARQUIVOS:
 * 
 * // ✅ DEPOIS (com este index.ts):
 * import { Avatar, Button } from '../components/common';
 * 
 * function UserCard() {
 *   return (
 *     <div>
 *       <Avatar initials="JS" size="lg" />
 *       <Button variant="primary">Editar Perfil</Button>
 *     </div>
 *   );
 * }
 * 
 * // ❌ ANTES (sem index.ts):
 * import Avatar from '../components/common/Avatar';
 * import Button from '../components/common/Button';
 * 
 * function UserCard() {
 *   return (
 *     <div>
 *       <Avatar initials="JS" size="lg" />
 *       <Button variant="primary">Editar Perfil</Button>
 *     </div>
 *   );
 * }
 * 
 * 📊 COMPARAÇÃO:
 * - Imports mais concisos
 * - Fácil adicionar novos componentes
 * - Estrutura escalável
 * - Padrão da indústria
 */

// ================================================
// ORGANIZAÇÃO POR CATEGORIAS (futuro)
// ================================================

/**
 * 📋 QUANDO HOUVER MUITOS COMPONENTES, ORGANIZAR POR CATEGORIA:
 * 
 * // FORMULÁRIOS
 * export { Input, TextArea, Select, Checkbox, Radio, Switch };
 * 
 * // NAVEGAÇÃO
 * export { Button, Link, Breadcrumb, Pagination, Tabs };
 * 
 * // FEEDBACK
 * export { Alert, Toast, Spinner, Progress, Badge };
 * 
 * // OVERLAY
 * export { Modal, Dialog, Tooltip, Popover, Dropdown };
 * 
 * // LAYOUT
 * export { Card, Divider, Skeleton };
 * 
 * // MÍDIA
 * export { Avatar, Image, Icon };
 * 
 * // TIPOGRAFIA
 * export { Text, Heading };
 * 
 * // DADOS
 * export { Table };
 * 
 * // INTERAÇÃO
 * export { Accordion, Collapsible, Slider };
 */

// ================================================
// INTEGRAÇÃO COM DESIGN SYSTEM
// ================================================

/**
 * 🎨 INTEGRAÇÃO COM DESIGN SYSTEM:
 * 
 * Este arquivo serve como ponte entre:
 * - Design tokens (cores, espaçamentos, tipografia)
 * - Componentes reutilizáveis
 * - Páginas e features específicas
 * 
 * ESTRUTURA HIERÁRQUICA:
 * tokens → common components → feature components → pages
 * 
 * EXEMPLO:
 * theme.colors.primary → Button.primary → UserCard → ProfilePage
 */

/**
 * 💡 DICAS DE ORGANIZAÇÃO:
 * 
 * 1. **MANTER COMPONENTES SIMPLES**: Sem lógica de negócio
 * 2. **PROPS CONSISTENTES**: Padrões similares entre componentes
 * 3. **DOCUMENTAÇÃO**: Cada componente bem documentado
 * 4. **TESTES**: Cobertura de teste para componentes críticos
 * 5. **STORYBOOK**: Catálogo visual dos componentes (futuro)
 * 6. **ACESSIBILIDADE**: Sempre considerar a11y
 * 7. **PERFORMANCE**: Lazy loading quando apropriado
 */