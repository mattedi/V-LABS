// src/components/HistoryList.tsx
import React from 'react';
import { useChatContext } from '../context/ChatContext';

const HistoryList: React.FC = () => {
  const { userHistory } = useChatContext();

  if (userHistory.length === 0) return null;

  return (
    <div className="mb-4 max-h-48 overflow-y-auto space-y-2">
      <h2 className="text-sm text-gray-400 font-medium">Histórico de Perguntas</h2>
      {userHistory.map((msg) => (
        <div
          key={msg.id}
          className="bg-gray-800 text-white p-2 rounded-md text-sm border border-gray-700"
        >
          {msg.text}
        </div>
      ))}
    </div>
  );
};

export default HistoryList;

