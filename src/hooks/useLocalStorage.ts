// src/hooks/useLocalStorage.ts
// Hook para salvar dados no navegador automaticamente
// Funciona como useState, mas os dados não são perdidos ao recarregar a página

import { useState, useEffect } from 'react';

/**
 * Hook que salva e carrega dados do localStorage automaticamente
 * Como um useState que persiste entre sessões do navegador
 * 
 * @param key - Nome da chave no localStorage (ex: 'tema', 'configuracoes')
 * @param initialValue - Valor padrão se não houver nada salvo
 * @returns [valor atual, função para mudar valor] - igual useState
 */
function useLocalStorage<T>(key: string, initialValue: T): [T, (value: T) => void] {
  
  // Estado para guardar o valor (como useState normal)
  const [storedValue, setStoredValue] = useState<T>(() => {
    // Esta função só roda na primeira vez (inicialização)
    try {
      // Tenta buscar o valor salvo no navegador
      const item = window.localStorage.getItem(key);
      
      // Se encontrou algo salvo, converte de texto para objeto
      // Se não encontrou, usa o valor inicial
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      // Se deu erro (localStorage bloqueado, JSON inválido, etc)
      console.error('Erro ao carregar do localStorage:', error);
      return initialValue; // Usa valor inicial como fallback
    }
  });

  // Salva no localStorage sempre que o valor mudar
  useEffect(() => {
    try {
      // Converte o valor para texto e salva no navegador
      window.localStorage.setItem(key, JSON.stringify(storedValue));
    } catch (error) {
      // Se deu erro ao salvar (localStorage cheio, etc)
      console.error('Erro ao salvar no localStorage:', error);
    }
  }, [key, storedValue]); // Roda quando a chave ou valor mudam

  // Retorna igual useState: [valor, função para mudar]
  return [storedValue, setStoredValue];
}

export default useLocalStorage;

// =====================================
// COMO USAR ESTE HOOK:
// =====================================

/**
 * 1. Básico - Como um useState que persiste:
 * 
 * function MeuComponente() {
 *   // Em vez de useState normal:
 *   // const [tema, setTema] = useState('claro');
 *   
 *   // Use useLocalStorage:
 *   const [tema, setTema] = useLocalStorage('tema-usuario', 'claro');
 *   
 *   return (
 *     <div>
 *       <p>Tema atual: {tema}</p>
 *       <button onClick={() => setTema(tema === 'claro' ? 'escuro' : 'claro')}>
 *         Trocar Tema
 *       </button>
 *     </div>
 *   );
 * }
 */

/**
 * 2. Com objetos complexos:
 * 
 * function Configuracoes() {
 *   const [config, setConfig] = useLocalStorage('app-config', {
 *     notificacoes: true,
 *     som: false,
 *     idioma: 'pt-br'
 *   });
 *   
 *   return (
 *     <div>
 *       <label>
 *         <input 
 *           type="checkbox"
 *           checked={config.notificacoes}
 *           onChange={(e) => setConfig({
 *             ...config,
 *             notificacoes: e.target.checked
 *           })}
 *         />
 *         Receber notificações
 *       </label>
 *     </div>
 *   );
 * }
 */

/**
 * 3. No AppContext (como está sendo usado):
 * 
 * function AppProvider({ children }) {
 *   // Salva o modo de tutoria escolhido
 *   const [currentMode, setCurrentMode] = useLocalStorage('tutor-mode', 'text');
 *   
 *   // Salva a preferência de tema
 *   const [isDarkMode, setIsDarkMode] = useLocalStorage('dark-mode', true);
 *   
 *   // Agora estes valores persistem entre sessões!
 * }
 */

/**
 * 4. Lista de favoritos que persiste:
 * 
 * function Favoritos() {
 *   const [favoritos, setFavoritos] = useLocalStorage('meus-favoritos', []);
 *   
 *   const adicionarFavorito = (item) => {
 *     setFavoritos([...favoritos, item]);
 *   };
 *   
 *   const removerFavorito = (id) => {
 *     setFavoritos(favoritos.filter(item => item.id !== id));
 *   };
 *   
 *   return (
 *     <div>
 *       <p>{favoritos.length} itens nos favoritos</p>
 *       {favoritos.map(item => (
 *         <div key={item.id}>
 *           {item.nome}
 *           <button onClick={() => removerFavorito(item.id)}>
 *             Remover
 *           </button>
 *         </div>
 *       ))}
 *     </div>
 *   );
 * }
 */

/**
 * 5. Histórico de pesquisas:
 * 
 * function BarraPesquisa() {
 *   const [historico, setHistorico] = useLocalStorage('historico-pesquisa', []);
 *   const [pesquisa, setPesquisa] = useState('');
 *   
 *   const buscar = () => {
 *     if (pesquisa && !historico.includes(pesquisa)) {
 *       // Adiciona no início e mantém só os últimos 10
 *       setHistorico([pesquisa, ...historico].slice(0, 10));
 *     }
 *   };
 *   
 *   return (
 *     <div>
 *       <input 
 *         value={pesquisa}
 *         onChange={(e) => setPesquisa(e.target.value)}
 *       />
 *       <button onClick={buscar}>Buscar</button>
 *       
 *       <div>
 *         <h4>Pesquisas recentes:</h4>
 *         {historico.map((item, index) => (
 *           <button key={index} onClick={() => setPesquisa(item)}>
 *             {item}
 *           </button>
 *         ))}
 *       </div>
 *     </div>
 *   );
 * }
 */

// =====================================
// VANTAGENS DESTE HOOK:
// =====================================

/**
 * ✅ PERSISTÊNCIA: Dados não se perdem ao recarregar página
 * ✅ AUTOMÁTICO: Salva e carrega automaticamente
 * ✅ SIMPLES: Interface igual ao useState
 * ✅ SEGURO: Trata erros automaticamente
 * ✅ FLEXÍVEL: Funciona com qualquer tipo de dado
 * ✅ TIPADO: TypeScript garante tipos corretos
 * 
 * SEM useLocalStorage (problemático):
 * - Dados perdidos a cada recarregamento
 * - Código manual para salvar/carregar
 * - Tratamento de erro repetitivo
 * - Estado inicial perdido
 * 
 * COM useLocalStorage (melhor):
 * - Persistência automática
 * - Interface familiar (useState)
 * - Tratamento de erro integrado
 * - Experiência do usuário melhor
 */

// =====================================
// DETALHES TÉCNICOS IMPORTANTES:
// =====================================

/**
 * 📝 O QUE ACONTECE INTERNAMENTE:
 * 
 * 1. PRIMEIRA VEZ:
 *    - Verifica se tem algo salvo no localStorage
 *    - Se sim: carrega e usa
 *    - Se não: usa valor inicial
 * 
 * 2. QUANDO MUDA O VALOR:
 *    - Atualiza o estado (re-renderiza componente)
 *    - Salva automaticamente no localStorage
 * 
 * 3. PRÓXIMA VEZ QUE ABRIR:
 *    - Carrega valor salvo automaticamente
 *    - Usuário continua de onde parou
 * 
 * 4. SE DER ERRO:
 *    - Usa valor inicial
 *    - Mostra erro no console
 *    - Aplicação continua funcionando
 */

/**
 * ⚠️ LIMITAÇÕES E CUIDADOS:
 * 
 * - localStorage só funciona no navegador (não no servidor)
 * - Limite de ~5-10MB por domínio
 * - Dados são strings (JSON.parse/stringify automático)
 * - Usuário pode limpar dados manualmente
 * - Modo privado pode bloquear localStorage
 * - Só salva dados simples (não funções, nem objetos complexos)
 */

/**
 * 🔧 CASOS DE USO IDEAIS:
 * 
 * ✅ BOM PARA:
 * - Preferências do usuário (tema, idioma)
 * - Estado de UI (sidebar aberta/fechada)
 * - Configurações da aplicação
 * - Histórico de ações
 * - Dados de formulário (rascunhos)
 * - Cache simples
 * 
 * ❌ NÃO USAR PARA:
 * - Dados sensíveis (senhas, tokens)
 * - Dados grandes (arquivos, imagens)
 * - Dados que mudam rapidamente
 * - Dados que precisam ser compartilhados entre usuários
 */