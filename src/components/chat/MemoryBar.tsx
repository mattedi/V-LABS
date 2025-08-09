// src/components/chat/MemoryBar.tsx
// src/components/chat/MemoryBar.tsx
import React, { useEffect, useState } from 'react';

type MemoriaItem = { id: string; texto: string; ts: number };
const STORAGE_KEY = 'vlabs_memoria_interacao';

function readStore(): MemoriaItem[] {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? (JSON.parse(raw) as MemoriaItem[]) : [];
  } catch {
    return [];
  }
}
function writeStore(items: MemoriaItem[]) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(items.slice(0, 100)));
  } catch {}
}

export default function MemoryBar() {
  const [items, setItems] = useState<MemoriaItem[]>(() => readStore());

  useEffect(() => {
    const handler = (e: Event) => {
      const detail = (e as CustomEvent).detail as { texto: string } | undefined;
      if (!detail?.texto) return;
      const novo: MemoriaItem = { id: crypto.randomUUID(), texto: detail.texto, ts: Date.now() };
      const next = [novo, ...readStore()].slice(0, 100);
      writeStore(next);
      setItems(next);
    };
    window.addEventListener('vlabs:memoria:add', handler as EventListener);
    return () => window.removeEventListener('vlabs:memoria:add', handler as EventListener);
  }, []);

  const removeItem = (id: string) => {
    const next = readStore().filter(i => i.id !== id);
    writeStore(next);
    setItems(next);
  };

  return (
    <div className="w-full bg-white/70 dark:bg-gray-800/60 border border-gray-200 dark:border-gray-700 rounded-md">
      {/* Cabeçalho opcional */}
      <div className="px-3 py-2 text-xs font-medium text-gray-600 dark:text-gray-300">
        Memória da interação
      </div>

      {/* LISTA COM SCROLL VERTICAL */}
      <div className="px-3 pb-2 max-h-40 overflow-y-auto space-y-2"> 
        {items.length === 0 ? (
          <span className="text-xs text-gray-500 dark:text-gray-400">
            Memória vazia. Suas últimas interações aparecerão aqui.
          </span>
        ) : (
          items.map(item => (
            <div
              key={item.id}
              title={new Date(item.ts).toLocaleString()}
              className="flex items-start justify-between gap-2 p-2 rounded-md border 
                         bg-gray-50/80 dark:bg-gray-900/50 border-gray-200 dark:border-gray-700"
            >
              <span className="text-xs leading-5 text-gray-800 dark:text-gray-200 break-words">
                {item.texto}
              </span>
              <button
                onClick={() => removeItem(item.id)}
                className="shrink-0 px-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                aria-label="Remover"
                title="Remover"
              >
                ×
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

