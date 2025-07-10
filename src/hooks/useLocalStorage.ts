// src/hooks/useLocalStorage.ts
// Hook para salvar dados no navegador automaticamente
// Funciona como useState, mas os dados não são perdidos ao recarregar a página
// Este hook permite que você salve e recupere dados do localStorage
// usando uma chave específica, e atualiza automaticamente o localStorage
// quando o valor muda. É útil para persistir configurações do usuário,
// preferências ou qualquer outro dado que você queira manter entre sessões do navegador.
  

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

// EXTENSÕES:
// - Adicionar suporte a tipos complexos (ex: objetos, arrays) com validação de schema.
// - Implementar debounce para evitar salvar muitas vezes seguidas.
// - Permitir customização de prefixo para evitar conflitos de chave.
// - Adicionar suporte a expiração de dados (ex: limpar após 1 dia).
// - Implementar sincronização com servidor para persistência em nuvem.
// - Adicionar suporte a múltiplos locais de armazenamento (ex: sessionStorage).
// - Implementar um sistema de notificações que informe o usuário sobre mudanças no localStorage.
// - Adicionar suporte a temas personalizados via localStorage.
// - Implementar um sistema de backup automático do localStorage em intervalos regulares.
// - Adicionar suporte a criptografia dos dados salvos para maior segurança.
// - Implementar um sistema de logs para rastrear alterações no localStorage.